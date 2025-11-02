# Autoguess without Sage

A standalone implementation of the Autoguess tool that does not require SageMath. This script parses connection and algebraic relations, builds and solves the corresponding Macaulay matrix, and outputs the results.

> **Note:** This implementation is heavily inspired from the original [autoguess](https://github.com/hadipourh/autoguess.git) project, and follows the same directory and file structure.


## Prerequisites

Before using this tool, ensure you have the following installed on your system:

- **Minizinc**
- **Z3**: It is the default SMT solver  
- **setuptools**: For packaging support.

### Python dependencies

All the following code are tested on python version [3.12.6](https://www.python.org/downloads/release/python-3126/).

Create a virtual environment in python.
```bash
python3 -m venv myenv
source myenv/bin/activate
```

Install the required Python packages via `pip`:

```bash
# 1. Core package manager fix (usually already present)
pip install --upgrade pip setuptools wheel

# 2. Install MiniZinc Python interface
pip install minizinc

# 3. Install PySAT with optional solvers
pip install 'python-sat[pblib,aiger]'

# 4. Install PySMT
pip install pysmt
pysmt-install --z3   # Still needed separately to install Z3 backend


# 5. Galois includes numpy, so no need to install numpy separately
pip install galois
```

### Defaults

- cp solver: gecode [comes with minizinc]
- sat solver: cadical153 [possibly with pysat]
- smt solver: z3



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
Preprocessing phase was started - 2025-11-01 00:29:08.364541
Number of algebraic equations: 7
Number of algebraic variables: 4
Number of algebraic monomials: 11
Spectrum of degrees: [2]
Macaulay matrix was generated in full matrixspace of 7 by 11 sparse matrices over finite field of size 2
Gaussian elimination started - 2025-11-01 00:29:08.870502
#Dependent variables: 7
#Free variables: 3
Gaussian elimination was finished after 0.2548 seconds
Result written to temp/macaulay_basis_f589f77fd1ad8bf0de119507f00cfe.txt in 0.0002 seconds
Preprocessing phase was finished after 0.8152 seconds
Number of guessed variables is set to be at most 10
Generating the CP model ...
CP model was generated after 0.01 seconds
Solving the CP model with cp-sat ...
Solving process was finished after 0.31 seconds
Number of guesses: 2
Number of known variables in the final state: 10 out of 10
The following 2 variable(s) are guessed: 
X4, RKKK13 (represents: X2 * X4)
```

You can choose specific solver also e.g. cbc (coin-bc)
```bash
python3 autoguess.py --inputfile ciphers/Example4/algebraic_relations.txt --solver cp --cpsolver cbc --maxsteps 10 --preprocess 1 --D 2
```
### Terminal output

```bash
OR Tools is available
Preprocessing phase was started - 2025-11-01 00:32:39.110815
Number of algebraic equations: 7
Number of algebraic variables: 4
Number of algebraic monomials: 11
Spectrum of degrees: [2]
Macaulay matrix was generated in full matrixspace of 7 by 11 sparse matrices over finite field of size 2
Gaussian elimination started - 2025-11-01 00:32:39.446340
#Dependent variables: 7
#Free variables: 3
Gaussian elimination was finished after 0.2443 seconds
Result written to temp/macaulay_basis_d29165f9726d47fb001886e495d8ba.txt in 0.0002 seconds
Preprocessing phase was finished after 0.6315 seconds
Number of guessed variables is set to be at most 10
Generating the CP model ...
CP model was generated after 0.01 seconds
Solving the CP model with cp-sat ...
Solving process was finished after 0.31 seconds
Number of guesses: 2
Number of known variables in the final state: 10 out of 10
The following 2 variable(s) are guessed:
X4, PNEM13 (represents: X2 * X4)
```

The available cp solvers depends on the installation. Extra solvers you have to install.

### SAT

```bash
python3 autoguess.py --inputfile ciphers/Example4/algebraic_relations.txt --solver sat --maxguess 1 --maxsteps 5 --preprocess 1 --D 3
```

### Terminal output

```bash
Preprocessing phase was started - 2025-11-01 00:31:41.505979
Number of algebraic equations: 7
Number of algebraic variables: 4
Number of algebraic monomials: 11
Spectrum of degrees: [2]
Macaulay matrix was generated in full matrixspace of 35 by 15 sparse matrices over finite field of size 2
Gaussian elimination started - 2025-11-01 00:31:41.872879
#Dependent variables: 13
#Free variables: 1
Gaussian elimination was finished after 0.2504 seconds
Result written to temp/macaulay_basis_b9524db9f1e0f58b6bb9ad0c3f96d1.txt in 0.0002 seconds
Preprocessing phase was finished after 0.6717 seconds
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

### PRESENT80

### CP

```bash
python3 autoguess.py --inputfile ciphers/PRESENT/relationfile.txt --solver cp --preprocess 1 --D 2 --maxguess 60 --maxsteps 10
```

### Terminal output
```bash
OR Tools is available
Preprocessing phase started - 2025-07-29 05:44:31.168201
Macaulay matrix was generated in full matrixspace of 1976 by 2152 sparse matrices over finite field of size 2
Gaussian elimination started - 2025-07-29 05:44:33.512416
#Dependent variables: 1976
#Free variables: 176
Gaussian elimination was finished after 1.7483 seconds
Result written to temp/macaulay_basis_219a8f4708c96ebb44cd37b4bd335a.txt in 0.9473 seconds
Preprocessing phase finished after 5.3408 seconds
Generating the CP model ...
CP model was generated after 476.22 seconds
Solving the CP model with cp-sat ...
Solving process was finished after 33.31 seconds
Number of guesses: 60
Number of known variables in the final state: 1391 out of 2160
The following 60 variable(s) are guessed:
k_26_0, k_26_2, k_5_23, k_6_67, k_7_5, k_7_7, k_7_13, k_7_72, k_8_8, k_8_9, k_8_10, k_8_23, k_12_12, k_12_76, k_13_11, k_13_48, k_13_49, k_14_28, k_14_65, k_15_14, k_15_46, k_15_50, k_15_51, k_15_73, k_16_10, k_16_13, k_16_74, k_17_6, k_17_58, k_18_29, k_18_49, k_19_35, k_19_66, k_20_50, k_21_37, k_21_71, k_21_77, k_22_31, k_22_41, k_22_48, k_22_53, k_23_10, k_23_37, k_23_49, k_23_52, k_23_57, k_23_58, k_23_73, k_24_13, k_24_20, k_24_24, k_24_37, k_24_39, k_24_52, k_24_78, k_25_9, k_25_38, k_26_59, k_26_60, k_26_61
```


### To Do
- Gröbner basis method is not supported.
- The preprocessing phase for long systems is quite a bit slow (e.g. in the PRESENT)


