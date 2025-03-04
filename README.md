# OpenSearch FastAPI Interface
FastAPI Python interface for OpenSearch

This repository provides a FastAPI-based interface to interact with an OpenSearch cluster. The API supports various functionalities such as index creation, document addition, search queries, and hybrid search through custom pipelines.

## Features

- Create an OpenSearch index with a custom definition
- Add documents to an existing index
- Perform search queries using OpenSearch DSL
- Execute hybrid search queries using custom pipelines
- Delete an OpenSearch index
- CORS enabled for API access

## Prerequisites

Ensure you have the following dependencies installed:

- Python 3.8+
- FastAPI
- OpenSearch Python client (`opensearch-py`)
- Pydantic
- Requests

## Configuration

Modify the following environment variables in `main.py` to match your OpenSearch setup:

```python
OPENSEARCH_HOST = "your-opensearch-host"
OPENSEARCH_PORT = 9200
OPENSEARCH_USERNAME = "your-username"
OPENSEARCH_PWD = "your-password"
```

## Running the Application

To start the FastAPI application, run:

Local running for tests:
```sh
uvicorn main_server:app --host 0.0.0.0 --port 8000
```

Background running for effective server deployment:
```sh
nohup uvicorn main_server:app --host 0.0.0.0 --port 8000 &
```

## API Endpoints

### Root Endpoint

- `GET /` - Returns a welcome message.

### Index Management

- `POST /addIndex` - Create an OpenSearch index.
- `DELETE /deleteIndex/{index_name}` - Delete an OpenSearch index.

### Document Management

- `POST /addDocument` - Add a document to an index.

### Search Operations

- `POST /search` - Perform a search using OpenSearch DSL.
- `POST /hybridSearch` - Execute a hybrid search using a custom pipeline.

## License

This project is licensed under the MIT License.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss the changes.

## Contact

For issues or inquiries, please contact [francesco.palmese@lutech.it].

