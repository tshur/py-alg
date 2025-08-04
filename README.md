# dsap: Data Structures & Algorithms & Practice

Python data structures & algorithms repository (for learning).

## Usage

_Note: Requires installation first!_

To actually import and use this package, you can start in the root directory.
Open a `python3` interpreter, and try the following:

```python
>>> from dsap.sort import heap_sort
>>> heap_sort([5, 1, 3, 2, 4])
[1, 2, 3, 4, 5]
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
- ...a few more! (check `.vscode/extensions.json`)

### venv

It is highly recommended to set up a virtual env to isolate the project setup
from your global system Python / packages. We install the core project
dependencies, and the set of test dependencies to enable testing commands.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install ".[test]"
```

After initial setup, VSCode should automatically pick up the environment and
iniitalize future terminal sessions in the venv.

## Testing

_Note: Tests are written in a separate (but parallel structure) `tests/`
directory._

### pytest

Recommended: To test code in "watch" mode, try the following command (re-runs
only affected tests):

```bash
ptw . --clear --doctest-modules --testmon
```

To run pytest for all files, including doctests on modules:

```bash
pytest --doctest-modules
```

To collect test coverage reports (# of lines covered by tests):

```bash
pytest --cov=src --cov=examples --cov-report=term-missing:skip-covered --cov-report xml:coverage.xml
```

To run pytest with the python debugger for debugging failed tests, run the
following (optionally set breakpoints to debug non-failures):

```bash
pytest --doctest-modules --pdb
```

In the python debugger, there are many useful commands to inspect the stack,
variables, and such. Some starter commands (more at
[pdb reference](https://docs.python.org/3/library/pdb.html#debugger-commands)):

```bash
l              # List the code around the current line (e.g., breakpoint).
p my_variable  # Print the given variable with its value at the current line.
q              # Quit.
```

## Packaging

To build the project for packaging / distribution, you can run the following:

```bash
python3 -m build
```

### Test PyPi

To deploy the package to Test PyPi, follow
[these instructions](https://packaging.python.org/en/latest/tutorials/packaging-projects/),
make sure to update the version number, and then run the commands:

```bash
rm -r dist/
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```

To install the package locally from TestPyPi, you can do the following:

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps dsap
```

```python
>>> from dsap.sort import heap_sort
>>> heap_sort([5, 1, 3, 2, 4])
[1, 2, 3, 4, 5]
```

### Production PyPi

To deploy the package to PyPi, follow
[these instructions](https://packaging.python.org/en/latest/tutorials/packaging-projects/),
make sure to update the version number, and then run the commands:

```bash
rm -r dist/
python3 -m build
python3 -m twine upload dist/*
```

To install the package locally from PyPi, you can do the following:

```bash
python3 -m pip install dsap
```

```python
>>> from dsap.sort import heap_sort
>>> heap_sort([5, 1, 3, 2, 4])
[1, 2, 3, 4, 5]
```
