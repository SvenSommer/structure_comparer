# Structure Comparer Service

Install all dependencies and the project itself as an editable dependency

```bash
pip install --editable .
```

Run all tests with

```bash
pytest
```

Start the server from this directory

```bash
PROJECTS_DIR=../projects python src/server.py
```

The server will be available at `localhost:5000`. The OpenAPI specification is available with the route `/spec`.
