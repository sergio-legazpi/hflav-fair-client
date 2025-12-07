# hflav-python-library

To run this project you firstly must create a virtual environment and install all the dependencies inside:

1. `python -m venv .venv`
2. `source .venv/bin/activate`

To install all the dependencies (including tests):
- `pip install ".[test]"`

And only dev dependencies:
- `pip install .`

## Tests

To launch all the tests:

- `pytest tests`

To launch a specific test:

- `pytest tests/test.py`

And to check the coverage:

- `pytest --cov=hflav_zenodo.module`

Where module is a specific module.

e.g: `pytest --cov=hflav_zenodo.source`