The api folder holds full api http-based integration tests, authored by AI.
The schemathesis folder holds the automated generated tests.

To get started, install a virtual environment and install the requirements:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the api tests, run:
```bash
pytest api
```

