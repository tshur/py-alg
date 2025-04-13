# py-alg

Python data structures & algorithms repository (for learning).

## Usage

To actually import and use this package, you can start in the root directory.
Open a python3 interpreter, and try the following:

```python
>>> from dsa.reduce import reduce
>>> reduce([1, 2, 3, 4, 5])
15
```

## Setup

This repo assumes you have a modern Python 3+ version installed. The repo is set
up to work with VS Code. Default settings and extensions are recommended to use
across the projects.

This includes:

- Python language server
- Python Black Formatter
- Python linting using Ruff
- Python strict type checking using pylance + mypy
- Testing using pytest + plugins

### venv

It is highly recommended to set up a virtual env to isolate the project setup
from your global system Python / packages. We install the core project
dependencies, and the set of test dependencies to enable testing commands.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e .[test]
```

After initial setup, VSCode should automatically pick up the environment and
iniitalize future terminal sessions in the venv.

## Testing

### pytest

To test code in "watch" mode, try the following command (re-runs only affected
tests):

```bash
ptw . --clear --doctest-modules --testmon
```

To run pytest for all files, including doctests on modules, and collect test
coverage reports:

```bash
pytest --doctest-modules --cov=dsa --cov-report xml:coverage.xml
```

To run pytest with the python debugger for debugging failed tests, run the
following (optionally set breakpoints to debug non-failures):

```bash
pytest --doctest-modules --pdb
```

In the python debugger, there are many useful commands to inspect the stack,
variables, and such. Some starter commands (more at [pdb reference](https://docs.python.org/3/library/pdb.html#debugger-commands)):

```
l  # List the code around the current line (e.g., breakpoint).
p my_variable  # Print the given variable with its value at the current line.
q  # Quit.
```

## Packaging

To build the project for packaging / distribution, you can run the following:

```bash
python3 -m build
```
