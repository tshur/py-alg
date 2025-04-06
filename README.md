# py-alg

Python algorithms repository with common algorithms (for learning).

## Usage

To actually import and use this package, you can start in the root directory.
Open a python3 interpreter, and try the following:

```python
>>> from package import sample
>>> sample.square(-3)
9
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

## venv

It is highly recommended to set up a virtual env to isolate the project setup
with your global system Python / packages.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

After initial setup, VSCode should automatically pick up the environment and
iniitalize future terminal sessions in the venv.

## unittest

To run all unittests across the projects, we can use `unittest` discovery:

```bash
python3 -m unittest discover -p "*_test.py" -v
```

Note: `-p "*_test.py"` is needed because the default format is `test*.py`. We
use `-v` (verbose), for now, but as the project grows it can be removed.
