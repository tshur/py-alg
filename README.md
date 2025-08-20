# dsap: Data Structures & Algorithms & Practice

Python data structures & algorithms repository (for learning).

_For developers or contributors, please see CONTRIBUTING.md._

## Usage

Commands are given with the `uv` tool [docs](https://docs.astral.sh/uv/).

### Quick Run

For testing the package _without_ creating a new project structure, try the
following:

```bash
uv run --with dsap --no-project -- python
```

```python
>>> from dsap.sort import heap_sort
>>> heap_sort([5, 1, 3, 2, 4])
[1, 2, 3, 4, 5]
```

### Project Setup

To install this project, run the following commands. We recommend first
preparing a virtual python environment.

```bash
uv init example
cd example
```

To actually install this package (or, `pip install dsap`):

```bash
uv add dsap
```

To verify the installation, open a `python3` interpreter, and try the following:

```bash
uv run python
```

```python
>>> from dsap.sort import heap_sort
>>> heap_sort([5, 1, 3, 2, 4])
[1, 2, 3, 4, 5]
```

Congrats! Now, you can use the `dsap` library in your code!

## Documentation

For documentation, see the docstrings within each module. Each data structure
and algorithm is thoroughly documented and tested.

## Contributing

We welcome creating new issues and PRs to improve this library. Please read the
CONTRIBUTING.md file, first! Thank you ~
