# ---------------------------------------------------------------------
# gf2poly.py   —  minimal Boolean-polynomial engine (pure Python)
# ---------------------------------------------------------------------
import re
from typing import FrozenSet, Iterable, Set
import numpy as np
import numba as nb

@nb.njit(parallel=True)
def rref_gf2_uint64(mat):
    """
    In‐place RREF of a GF(2) matrix whose rows are packed into uint64 words.
    Returns the rank (# of pivots).
    """
    m, nwords = mat.shape
    pivot = 0
    # Loop over each bit‐column
    for col in range(nwords * 64):
        w, b = divmod(col, 64)
        # Find a row ≥ pivot with a 1 in (w,b)
        for i in range(pivot, m):
            if (mat[i, w] >> b) & 1:
                # swap rows i <-> pivot
                mat[pivot], mat[i] = mat[i].copy(), mat[pivot].copy()
                break
        else:
            continue  # no pivot in this column
        # Eliminate this bit from all other rows
        for i in nb.prange(m):
            if i != pivot and ((mat[i, w] >> b) & 1):
                mat[i, :] ^= mat[pivot, :]
        pivot += 1
        if pivot == m:
            break
    return pivot



# ---- core object ----------------------------------------------------
class GF2Poly:
    """
    Polynomial over GF(2) with idempotent variables (x² = x).

    Internal form:  a set of monomials;
    each monomial is a frozenset of variable names.
    """
    # def __init__(self, monomials: Iterable[FrozenSet[str]] = ()):
    #     self.monomials: Set[FrozenSet[str]] = set(monomials)
    
    def __init__(self, monomials=()):
        self.monomials = set(monomials)

    # XOR  (addition mod 2)  -----------------------------------------
    def __xor__(self, other: "GF2Poly") -> "GF2Poly":
        return GF2Poly(self.monomials ^ other.monomials)

    __add__ = __xor__          # allow p + q as shorthand

    # multiplication  -----------------------------------------------
    # def __mul__(self, other: "GF2Poly") -> "GF2Poly":
    #     out: Set[FrozenSet[str]] = set()
    #     for m1 in self.monomials:
    #         for m2 in other.monomials:
    #             new = frozenset(m1 | m2)          # idempotent merge
    #             # toggle presence (coefficients are 0/1)
    #             if new in out:
    #                 out.remove(new)
    #             else:
    #                 out.add(new)
    #     return GF2Poly(out)
    
    def __mul__(self, other: "GF2Poly") -> "GF2Poly":
        out = set()
        for m1 in self.monomials:
            for m2 in other.monomials:
                merged = frozenset(m1 | m2)
                out.symmetric_difference_update({merged})
        return GF2Poly(out)

    # pretty-print ----------------------------------------------------
    def __bool__(self):        # truth value (is zero?)
        return bool(self.monomials)

    def __str__(self):
        if not self:
            return "0"
        def key(mon):          # sort: fewest vars first, then lexicographically
            return (len(mon), tuple(sorted(mon)))
        parts = []
        for mon in sorted(self.monomials, key=key):
            parts.append("*".join(sorted(mon)) or "1")
        return " + ".join(parts)

    __repr__ = __str__

# ---- helpers to build constants / variables -------------------------
def var(name: str) -> GF2Poly:
    return GF2Poly([frozenset([name])])

def const(bit: int) -> GF2Poly:
    return GF2Poly([frozenset()]) if bit & 1 else GF2Poly()

# ---------------------------------------------------------------------
# very small parser  (handles ^, *, +, parentheses, numbers 0/1)
# ---------------------------------------------------------------------
_token = re.compile(r'\s*([A-Za-z_]\w*|\d+|\^|\*|\+|\(|\))')

def parse(text: str) -> GF2Poly:
    """Return a GF2Poly for an expression like 'x*(x^4 + 1)'."""
    toks = [t for t in _token.findall(text) if t.strip()]
    # print(toks)
    pos = 0
    
    
    def nexttok():               # current token or None
        return toks[pos] if pos < len(toks) else None

    def parse_sum():
        nonlocal pos
        poly = parse_prod()
        while nexttok() == '+':
            pos += 1
            poly = poly + parse_prod()
        return poly

    def parse_prod():
        nonlocal pos
        term = GF2Poly([frozenset()])          # multiplicative identity
        while True:
            t = nexttok()
            if t is None or t in '+)':
                break
            if t == '(':
                pos += 1
                factor = parse_sum()
                if nexttok() != ')': raise SyntaxError("missing ')'")
                pos += 1
            else:                              # variable or number
                name = t
                pos += 1
                if nexttok() == '^':           # skip exponent entirely
                    pos += 2                   # drop “^ <number>”
                factor = const(int(name)) if name.isdigit() else var(name)
            term = term * factor
            if nexttok() == '*': pos += 1      # consume the '*'
        return term

    result = parse_sum()
    if pos != len(toks):
        raise SyntaxError("junk at end of expression")
    return result