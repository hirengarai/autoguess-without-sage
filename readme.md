# Autoguess without Sage

A standalone implementation of the Autoguess tool that does not require SageMath. This script parses connection and algebraic relations, builds and solves the corresponding Macaulay matrix, and outputs the results.

> **Note:** This implementation is heavily inspired from the original [autoguess](https://github.com/hadipourh/autoguess.git) project, and follows the same directory and file structure.


## Prerequisites

Before using this tool, ensure you have the following installed on your system:

- **Minizinc**: A constraint solver used for solving the Macaulay matrix system.  
- **Z3**: The Z3 SMT solver for efficient constraint solving.  
- **Python 3.6+**: The script is written for Python 3.  
- **setuptools**: For packaging support.

### Python dependencies

Install the required Python packages via `pip`:

```bash
pip install minizinc

pip install 'python-sat[pblib,aiger]' 

pip pysmt 

pip install setuptools

pysmt-install --z3

pip install sympy

pip install numpy

pip install galois
```
### Example 1

### CP
```bash
python3 autoguess.py --inputfile ciphers/Example1/relationfile.txt --solver cp --maxsteps 5
```
### Terminal output

```bash
OR Tools is available
Number of guessed variables is set to be at most 7
Generating the CP model ...
CP model was generated after 0.00 seconds
Solving the CP model with cp-sat ...
Solving process was finished after 0.36 seconds
Number of guesses: 2
Number of known variables in the final state: 7 out of 7
The following 2 variable(s) are guessed:
v, u
```

### SAT

```bash
python3 autoguess.py --inputfile ciphers/Example1/relationfile.txt --solver sat --maxguess 2 --maxsteps 5
```
### Terminal output

```bash
Generating the SAT model ...
SAT model was generated after 0.00 seconds

Solving with cadical153 ...
Time used by SAT solver: 0.00 seconds
Number of guesses: 2
Number of known variables in the final state: 7 out of 7
The following 2 variable(s) are guessed:
x, s
```

You can choose specific solver also e.g. glucose3
```bash
python3 autoguess.py --inputfile ciphers/Example1/relationfile.txt --solver sat --satsolver glucose3 --maxguess 2 --maxsteps 5
```
### Terminal output

```bash
Generating the SAT model ...
SAT model was generated after 0.00 seconds

Solving with glucose3 ...
Time used by SAT solver: 0.00 seconds
Number of guesses: 2
Number of known variables in the final state: 7 out of 7
The following 2 variable(s) are guessed:
x, s
```

### SMT

```bash
python3 autoguess.py --inputfile ciphers/Example1/relationfile.txt --solver smt --maxguess 2 --maxsteps 5
```
### Terminal output

```bash
Generating the SMT model ...
SMT model was generated after 0.01 seconds
Checking the satisfiability of the constructed SMT model using z3 ...
Checking was finished after 0.00 seconds
Number of guesses: 2
Number of known variables in the final state: 7 out of 7
The following 2 variable(s) are guessed:
s, v
```

### Example 4

### CP

```bash
python3 autoguess.py --inputfile ciphers/Example4/algebraic_relations.txt --solver cp --maxsteps 10 --preprocess 1 --D 2
```

### Terminal output

```bash
OR Tools is available
Preprocessing phase was started - 2025-07-25 21:51:59.918078
Algebrize input polynomials done in 0.0138 seconds
The 4 variables are [X4, X3, X2, X1]
Number of algebraic equations: 7
Number of algebraic variables: 4
Number of algebraic monomials: 11
Spectrum of degrees: [2]
Build macaulay polynomials done in 0.0023 seconds
Macaulay matrix was generated in 0.0067 seconds
The matrix is of dimension: 7×11 over GF(2)
#Dependent variables: 7
#Free variables: 3
Gaussian elimination was finished after 0.2342 seconds
Result was written into temp/macaulay_basis_0c540ac5b7d8ddf5ac0b2908dcdc51.txt after 0.0002 seconds
Preprocessing phase was finished after 0.7222 seconds
Number of guessed variables is set to be at most 10
Generating the CP model ...
CP model was generated after 0.00 seconds
Solving the CP model with cp-sat ...
Solving process was finished after 0.35 seconds
Number of guesses: 2
Number of known variables in the final state: 10 out of 10
The following 2 variable(s) are guessed:
X2, VLAK01
```

You can choose specific solver also e.g. cbc (coin-bc)
```bash
python3 autoguess.py --inputfile ciphers/Example4/algebraic_relations.txt --solver cp --cpsolver cbc --maxsteps 10 --preprocess 1 --D 2
```
### Terminal output

```bash
OR Tools is available
Preprocessing phase was started - 2025-07-25 22:54:32.651040
Algebrize input polynomials done in 0.0139 seconds
The 4 variables are [X4, X3, X2, X1]
Number of algebraic equations: 7
Number of algebraic variables: 4
Number of algebraic monomials: 11
Spectrum of degrees: [2]
Build macaulay polynomials done in 0.0024 seconds
Macaulay matrix was generated in 0.0070 seconds
The matrix is of dimension: 7×11 over GF(2)
#Dependent variables: 7
#Free variables: 3
Gaussian elimination was finished after 0.2562 seconds
Result was written into temp/macaulay_basis_2cc116aa956a34b857c3eaea3bbb4d.txt after 0.0002 seconds
Preprocessing phase was finished after 0.9287 seconds
Number of guessed variables is set to be at most 10
Generating the CP model ...
CP model was generated after 0.00 seconds
Solving the CP model with cbc ...
Solving process was finished after 3.73 seconds
Number of guesses: 2
Number of known variables in the final state: 10 out of 10
The following 2 variable(s) are guessed:
X4, X2
```

The available cp solvers depends on the installation. Extra solvers you have to install.

### SAT

```bash
python3 autoguess.py --inputfile ciphers/Example4/algebraic_relations.txt --solver sat --maxguess 1 --maxsteps 5 --preprocess 1 --D 3
```

### Terminal output

```bash
Preprocessing phase was started - 2025-07-25 23:01:09.528164
Algebrize input polynomials done in 0.0145 seconds
Number of algebraic equations: 7
Number of algebraic variables: 4
Number of algebraic monomials: 11
Spectrum of degrees: [2]
Build macaulay polynomials done in 0.0025 seconds
Macaulay matrix was generated in 0.0208 seconds
The matrix is of dimension: 35×15 over GF(2)
#Dependent variables: 13
#Free variables: 1
Gaussian elimination was finished after 0.2457 seconds
Result was written into temp/macaulay_basis_f4641b999ca9bebe2058028be7a8ad.txt after 0.0002 seconds
Preprocessing phase was finished after 0.9527 seconds
Generating the SAT model ...
SAT model was generated after 0.00 seconds

Solving with cadical153 ...
Time used by SAT solver: 0.00 seconds
Number of guesses: 1
Number of known variables in the final state: 14 out of 14
The following 1 variable(s) are guessed:
X3
```

### SMT

```bash
python3 autoguess.py --inputfile ciphers/Example4/algebraic_relations.txt --solver smt --maxguess 1 --maxsteps 5 --preprocess 1 --D 3
```

### Terminal output

```bash
Preprocessing phase was started - 2025-07-25 23:03:44.792831
Algebrize input polynomials done in 0.0146 seconds
Number of algebraic equations: 7
Number of algebraic variables: 4
Number of algebraic monomials: 11
Spectrum of degrees: [2]
Build macaulay polynomials done in 0.0027 seconds
Macaulay matrix was generated in 0.0210 seconds
The matrix is of dimension: 35×15 over GF(2)
#Dependent variables: 13
#Free variables: 1
Gaussian elimination was finished after 0.2645 seconds
Result was written into temp/macaulay_basis_175aa65b3c3f0671d0216d01722934.txt after 0.0002 seconds
Preprocessing phase was finished after 0.9653 seconds
Generating the SMT model ...
SMT model was generated after 0.02 seconds
Checking the satisfiability of the constructed SMT model using z3 ...
Checking was finished after 0.01 seconds
Number of guesses: 1
Number of known variables in the final state: 14 out of 14
The following 1 variable(s) are guessed:
X3
```


