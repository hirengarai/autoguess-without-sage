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

pip install python-sat[pblib,aiger] pysmt setuptools
pysmt-install --z3

### Example 1

### CP
```bash
python3 autoguess.py --inputfile ciphers/Example1/relationfile.txt --solver cp --maxsteps 5

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