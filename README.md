# dsap: Data Structures & Algorithms & Practice

Python data structures & algorithms repository (for learning).

_For developers or contributors, please see CONTRIBUTING.md._

## Usage

To install this project, run the following commands. We recommend first
preparing a virtual python environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

To actually install this package:

```bash
pip install dsap
```

To verify the installation, open a `python3` interpreter, and try the following:

```python
>>> from dsap.sort import heap_sort
>>> heap_sort([5, 1, 3, 2, 4])
[1, 2, 3, 4, 5]
```

Congrats! Now, you can use the `dsap` library in your code!

For documentation, see the docstrings within each module. Each data structure
and algorithm is thoroughly documented and tested.

## Contributing

We welcome creating new issues and PRs to improve this library. Please read the
CONTRIBUTING.md file, first! Thank you ~
