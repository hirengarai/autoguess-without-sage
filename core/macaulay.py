



import time
import sys
from datetime import datetime
from argparse import ArgumentParser, RawTextHelpFormatter
from itertools import combinations

from sympy import sympify, expand, Pow, GF, Poly, total_degree
import numpy as np
# sys.path.insert(0, "/home/tools/autoguess/venv/lib/python3.11/site-packages")
import galois
from gf2poly import parse, GF2Poly
sys.setrecursionlimit(10000)

def safe_total_degree(expr, variables):
    expr = expr.expand()
    terms = expr.as_ordered_terms()
    max_deg = 0
    for t in terms:
        deg = sum(t.as_poly(variables).degree_list()) if t.has(*variables) else 0
        max_deg = max(max_deg, deg)
    return max_deg

class Macaulay:
    """
    Given a set of Boolean polynomials (in text form) and integer D,
    this class:
      1. Parses them into GF2Poly objects
      2. (Optionally) performs Macaulay lifting up to degree D
      3. Builds the coefficient matrix and computes its RREF over GF(2)
      4. Writes the resulting relations to an output file
    """
    count = 0

    def __init__(self, inputfile, outputfile, D=2, term_ordering='deglex'):
        Macaulay.count += 1
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.D = D
        self.term_ordering = term_ordering
        self.algebraize_input_polynomials()
    
    def algebraize_input_polynomials(self):
        """
        Converts the given polynomials in string format to a list of boolean polynomials of type PolynomialSequence
        """
        t0 = time.time()
        try:
            with open(self.inputfile, 'r') as equations_file:
                string_polynomials = equations_file.read().splitlines()
        except IOError:
            print('%s is not accessible!' %self.inputfile)
            sys.exit()
        
        self.symbolic_polynomials = [sympify(item) for item in string_polynomials]
        syms = {sym for p in self.symbolic_polynomials for sym in p.free_symbols}
        
        self.symbolic_variables = sorted(syms, key=lambda s: s.name, reverse=True)
        # print(self.symbolic_variables)
        elapsed = time.time() - t0
        print(f'Algebrize input polynomials done in {elapsed:.4f} seconds')
        # print("The %d variables are %s" % (len(self.symbolic_variables), self.symbolic_variables))
        # return symbolic_polynomials, symbolic_variables
    
    def build_macaulay_polynomials(self):
        """
        Constructs the Macaulay polynomials with degree at most D corresponding to the given boolean polynomial sequence
        """
        self.macaulay_polynomials = []
        t0 = time.time()
        nvars = len(self.symbolic_variables)

        # for f in self.symbolic_polynomials:
        #     print("f =", f)
        #     print("type(f) =", type(f))
        # 1. compute each polynomial’s degree
        # degrees = [
        #     f.as_poly(*self.symbolic_variables).total_degree()
        #     for f in self.symbolic_polynomials
        # ]
        degrees = [safe_total_degree(f, self.symbolic_variables) for f in self.symbolic_polynomials]
        degree_spectrum = sorted(set(degrees))

        
        print('Number of algebraic equations:', len(self.symbolic_polynomials))
        print('Number of algebraic variables:', nvars)
        print('Number of algebraic monomials:',
            len({ exp
                    for f in self.symbolic_polynomials
                    for exp in f.as_poly(*self.symbolic_variables).monoms() }))
        print('Spectrum of degrees:', degree_spectrum)
        # collect all the monomials of highest degree d
        multiplied_monomials = {}
        for d in degree_spectrum:
            if d < self.D:
                mons = []
                r = self.D - d
                for k in range(r + 1):
                    for idxs in combinations(range(nvars), k):
                        m = 1
                        for i in idxs:
                            m *= self.symbolic_variables[i]
                        mons.append(m)     
                multiplied_monomials[d] = mons
            else:
                multiplied_monomials[d] = [1]
                
        # 3. form the Macaulay list
        for f, d in zip(self.symbolic_polynomials, degrees):
            f_poly = parse(str(f))         
            for m in multiplied_monomials[d]:
                m_mono = parse(str(m))     
                product = m_mono * f_poly   
                self.macaulay_polynomials.append(product)
        
        print(f"Build macaulay polynomials done in {time.time() - t0:.4f} seconds")
    
    
    def build_macaulay_matrix(self):
        """
        Generates the Macaulay matrix
        """
        t0 = time.time()
        
        # 1. Optional Macaulay lift if system is nonlinear
        degrees = [f.as_poly(*self.symbolic_variables).total_degree()
                for f in self.symbolic_polynomials]
        if max(degrees) > 1:
            min_deg = min(degrees)
            if self.D < min_deg:
                self.D = min_deg
            self.build_macaulay_polynomials()
        else:
            print("All polynomials are linear, skipping Macaulay lifting")
            self.macaulay_polynomials = self.symbolic_polynomials

        # 2. Collect & order all monomials (exponent‑tuples) in graded‑lex order
        exps = set()
        for f in self.macaulay_polynomials:
            f_sym = sympify(str(f))
            p = Poly(f_sym, *self.symbolic_variables, domain = GF(2))
            exps.update(p.monoms())

        # graded‑lex: first by total degree, then by the tuple
        self.mons = sorted(exps, key=lambda exp: (sum(exp), exp), reverse=True)
        # for item in self.mons:
        #     print(item)
        
        col_index = {exp: i for i, exp in enumerate(self.mons)}
        
        # 3. Build a dense 0/1 NumPy array of shape (n_rows, n_cols)
        n_rows, n_cols = len(self.macaulay_polynomials), len(self.mons)
        A = np.zeros((n_rows, n_cols), dtype=np.uint8)
        for i, f in enumerate(self.macaulay_polynomials):
            f_sym = sympify(str(f))
            p = Poly(f_sym, *self.symbolic_variables, domain = GF(2))
            for exp, coeff in zip(p.monoms(), p.coeffs()):
                if coeff & 1:
                    A[i, col_index[exp]] = 1
        self.macaulay_matrix = A
        
        elapsed = time.time() - t0
        print(f"Macaulay matrix was generated in {elapsed:.4f} seconds")
        print(f"The matrix is of dimension: {n_rows}×{n_cols} over GF(2)")   

    def gaussian_elimination(self):
        """
        Perform RREF on GF(2) matrix using galois, and manually compute pivots.
        """
        t0 = time.time()
        GF2 = galois.GF(2)
        A = GF2(self.macaulay_matrix)
        
        self.R = A.row_reduce()
        
        # convert to numpy to inspect bit patterns
        R_np = np.array(self.R, dtype=np.uint8)

        pivots = [int(np.nonzero(R_np[i])[0][0])
                for i in range(R_np.shape[0])
                if R_np[i].any()]
        
        def is_constant(mono):
            return all(e == 0 for e in mono)
        

        # Exclude constant monomial from free/dependent count
        self.dependent = [m for j, m in enumerate(self.mons) if j in pivots and not is_constant(m)]
        self.free = [m for j, m in enumerate(self.mons) if j not in pivots and not is_constant(m)]

                # self.dependent = [self.mons[j] for j in pivots]
                # self.free = [self.mons[j] for j in range(self.macaulay_matrix.shape[1]) if j not in pivots]

        elapsed = time.time() - t0
        print(f"#Dependent variables: {len(self.dependent)}")
        print(f"#Free variables: {len(self.free)}")
        print(f"Gaussian elimination was finished after {elapsed:.4f} seconds")
    
    def write_result(self):
        """
        Writes the derived Boolean equations into the output file and prints them to the terminal.
        """

        t0 = time.time()
        try:
            with open(self.outputfile, 'w') as f:
                rows = np.array(self.R, dtype=np.uint8)
                for row in rows:
                    terms = []
                    for j, bit in enumerate(row):
                        if bit:
                            # self.mons[j] is a tuple of exponents like (0, 1, 0, 1)
                            mono = self.mons[j]
                            if sum(mono) == 0:
                                terms.append('1')
                            else:
                                # Convert to variable names like x2*x4
                                var_list = [str(self.symbolic_variables[i]) for i, e in enumerate(mono) if e == 1]
                                terms.append('*'.join(var_list))
                    if terms:
                        equation = ' + '.join(terms)
                        f.write(equation + '\n')
                        # print(equation)
        except IOError:
            print(f"Error: cannot write to {self.outputfile}")
            sys.exit(1)

        print(f"Result was written into {self.outputfile} after {time.time() - t0:.4f} seconds")
    
def loadparameters(args):
    """
    Get parameters from the argument list and inputfile.
    """
    params = {'inputfile':'ex4.txt','outputfile':'macaulay_basis.txt','D':2,
              "term_ordering": 'deglex'}
    if args.inputfile: params['inputfile']=args.inputfile[0]
    if args.outputfile: params['outputfile']=args.outputfile[0]
    if args.D: params['D']=args.D[0]
    if args.term_ordering: params["term_ordering"] = args.term_ordering[0]
    
    
    return params


def main():
    """
    Parse the arguments and start the request functionality with the provided parameters.
    """
    parser = ArgumentParser(description="This tool computes the Macaulay matrix with degree D,"
                                        " given a system of boolean polynomials and"
                                        " a positive integer D",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i','--inputfile', nargs=1, help="Use an input file in plaintext format to read the relations from.")
    parser.add_argument('-o','--outputfile', nargs=1, help="Use an output file to write the output into it.")
    parser.add_argument('-D','--D', nargs=1, type=int, help="A positive integer as the degree of Macaulay matrix.")
    parser.add_argument('-t', '--term_ordering', nargs=1, type=str, help="A term ordering such as deglex or degrevlex.")
    
    args = parser.parse_args()
    params = loadparameters(args)
    macaulay = Macaulay(inputfile=params['inputfile'], outputfile=params['outputfile'], D=params['D'], term_ordering=params['term_ordering'])
    macaulay.build_macaulay_matrix()
    macaulay.gaussian_elimination()
    macaulay.write_result()

if __name__ == '__main__':
    main()    
    