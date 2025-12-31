import argparse
import time

import numpy as np
import galois


def make_binary_matrix(rows: int, cols: int, density: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    if density >= 1.0:
        return rng.integers(0, 2, size=(rows, cols), dtype=np.uint8)
    mask = rng.random((rows, cols)) < density
    return mask.astype(np.uint8)


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark galois GF(2) RREF")
    parser.add_argument("--rows", type=int, default=1024)
    parser.add_argument("--cols", type=int, default=1024)
    parser.add_argument("--density", type=float, default=0.1, help="Fraction of 1s in the matrix")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    mat = make_binary_matrix(args.rows, args.cols, args.density, args.seed)
    gf = galois.GF(2)
    a = gf(mat)

    start = time.perf_counter()
    rref_out = a.row_reduce()
    elapsed = time.perf_counter() - start

    # Handle multiple galois versions: row_reduce may return (rref, pivots)
    rref = rref_out[0] if isinstance(rref_out, tuple) else rref_out

    # Derive rank from non-zero rows to avoid version-specific APIs
    arr = np.asarray(rref)
    rank = int(np.count_nonzero(np.any(arr != 0, axis=1)))

    print(f"galois row_reduce: {args.rows}x{args.cols}, density={args.density}")
    print(f"rank={rank}, elapsed_s={elapsed:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
