# Contributing Guidelines

Thank you for your interest in helping out with this project. The focus of this
project is to improve learning on data structures and algorithms (and Python).

We welcome all contributions and hope that you are learning as much as we are!

## Full Workflow

This section should take you through the most basic steps to create, send, and
merge a PR to the project!

### 0. (one time) Cloning and setting up your workspace

Clone the repository, pull the latest changes, and follow these instructions to
install the development environment.

You should get all the recommended VSCode extensions and workspace settings
(like auto-format), see `.vscode/extensions.json`.

Cloning the repo:

```bash
git clone git@github.com:tshur/py-alg.git
cd py-alg
```

Installing dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[test]"
```

Verifying tests are passing:

```bash
pytest --doctest-modules
```

And all lines of code are covered by tests.

```bash
pytest                                   \
  --cov=src --cov=examples               \
  --cov-report=term-missing:skip-covered \
  --cov-report xml:coverage.xml
```

As a last check, you can verify the package is installed in the python
interpreter (run `python3` in command-line):

```python
>>> from dsap.sort import heap_sort
>>> heap_sort([5, 1, 3, 2, 4])
[1, 2, 3, 4, 5]
```

### 1. (optional) Create a new issue

_Optional: At this point, you could create and self-assign a new GitHub Issue
for the changes you plan to make. You can make it a title-only issue, or add
more detailed plans in the description._

The benefit is that you will "mark" the changes you intend to make, so others
don't try to make the same changes!

### 1. Create a new feature branch

You should have a branch to store your work. Then, to merge into main you can
open a PR (pull request) which can be reviewed before merging to production.

**Branch naming:** We can use the format: `${USER}/${FEATURE}` to name branches.

Possible steps:

```bash
cd py-alg                               # Work at root project directory.
git checkout main                       # Switch to the main branch.
git pull                                # Make sure that main is up-to-date.
git checkout -b tshur/add-contributing  # Create (and switch to) a new branch.
git status                              # Verify that you are on the new branch.
```

### 2. Commit your changes

Once you make your changes in your code editor, commit them to your branch.

Make sure tests are passing, and strive for 100% test coverage! You can "watch"
modified files and run tests automatically with the following command:

```bash
ptw . --clear --doctest-modules --testmon
```

Possible steps to create your commit:

```bash
git status                 # You should see the pending changes on your branch.
git add --all              # Stage all untracked files.
git status                 # Check all changes are staged.
git commit -m "Add docs."  # Commit files with a one-line message.
git status                 # See there are no more un-committed changes.
git push                   # Push your committed changes to GitHub / remote.
```

### 3. Open a PR to merge your changes into main

At this point, your changes should be ready for review. You should have checked
your changes for style, consistency, clean code, and tests should be passing.

It is OK to write tests in a follow-up, but ideally you add some version of
testing in a separate commit within the same PR.

You can typically open a pull request on
[github.com](https://github.com/tshur/py-alg/pulls). Usually, when you push a
commit, a handy quick-link to opening a PR will be in the terminal.

### 4. Request review

Assign reviewers to look at your code before merging the PR. You can also attach
a helpful description, link issues, add a screenshot, or whatever you think will
be helpful for reviewers.

### 5. Merging a PR to main

At this point, your PR should be reviewed and good-to-go. We want to make it a
part of the main branch. There can be a couple of complications.

**_Note: Do not click "Merge Pull Request". Instead, we prefer clicking the
drop-down and doing either "Rebase and Merge" or "Squash and Merge"._**

Simple method (no complications):

1. On github.com, viewing your pull request, click the button to "sync changes"
2. Next, "Rebase and Merge" (stack your changes into multiple commits on main)

Handling merge conflicts:

1. If the above option doesn't work, you likely have unresolved conflicts with
   the latest changes in the `main` branch.
2. My typical workflow is to go back to VSCode and fix these manually, then
   return to github.com to merge to main via the "Simple method".

Sample commands:

```bash
git checkout tshur/add-contributing  # Ensure we are on our branch.
git status                           # Verify no pending changes.

git pull --rebase origin main        # Start rebasing new changes from main.
# Here, resolve any merge conflicts within the VSCode source control editor.
git push --force-with-lease          # Force push our manually updated branch.
```

After these changes, you should be good to return to github.com and merge!

## Testing

It is good to write unit tests for any code you add to the repository. You
should ensure that all tests are passing before sending a PR for review.

Ideally, unit testing at a minimum has 100% code coverage (meaning every line of
code is exercised by at least one test). Check the `README` for how to measure
code coverage. Also, there is an extension you can enable to view which lines
are actually covered by tests in the gutter
(`ryanluker.vscode-coverage-gutters`).

## AI Usage

It is our current opinion that heavy AI use would deter from maximal learning,
and is generally discouraged. You are welcome to use AI as a learning tool, but
we ultimately prefer hand-crafted, homemade code (for now?).

Remember, the goal is not to quickly reach any end-state... the goal is the
process itself! Part of this means making mistakes and learning from them.
Sometimes, it is also best to implement an un-optimized version first, then send
another PR to improve it with a different approach.

We hope that you can learn a lot of new things (like we have!) from contributing
to this repository (productionization, testing, generic typing, algorithms,
optimization, git collaboration, critical thinking, problem solving, and more).

## Code Style

This repository follows the
[Google Style Guide for Python](https://google.github.io/styleguide/pyguide.html).
You are not expected to thoroughly read this style guide. One option is to send
PRs for review with your best effort for a consistent style, and we will help
you align with the repository style guide (sometimes, this means nit-picky
comments; sorry!).

Note: there is an auto-formatter extension recommended for VSCode (and enabled
in project settings). If you use this formatter, you will be 95% of the way
there!

## Community Guidelines

Please be respectful, courteous, and compassionate. We all want to grow and
improve, let's learn together!

## Releasing

_Note: The production release process is reserved for code owners of the repo.
Feel free to build a distribution and release it to Test PyPi for learning!_

To build the project for packaging / distribution, you can run the following:

```bash
pip install ".[release]"
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
