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
pip install python-sat[pblib,aiger] pysmt setuptools
pysmt-install --z3

## 