from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from opensearchpy import OpenSearch
import requests


OPENSEARCH_HOST = ""
OPENSEARCH_PORT = 9200

OPENSEARCH_USERNAME = ""
OPENSEARCH_PWD = ""

# OpenSearch client setup
client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PWD),
    use_ssl = False,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

# FastAPI application
app = FastAPI(title="OpenSearch FastAPI Interface")

origins = ['null']         
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class IndexRequest(BaseModel):
    index_name: str
    index_definition: dict  # JSON structure for index settings and mappings

class DocumentRequest(BaseModel):
    index_name: str
    asset_id: str
    asset_content: dict

class SearchQueryRequest(BaseModel):
    index_name: str
    search_query: dict

class HybridSearchRequest(BaseModel):
    index_name: str
    pipeline_name: str
    search_query: dict  # The usual OpenSearch query DSL


@app.get("/")
async def root():
    return {"message": "Welcome to the OpenSearch FastAPI Interface!"}

@app.post("/addIndex")
async def add_index(request: IndexRequest):
    """
    Add a new index with a custom definition.
    """
    try:
        # Check if index already exists
        if client.indices.exists(index=request.index_name):
            raise HTTPException(
                status_code=400, detail=f"Index '{request.index_name}' already exists."
            )

        # Create index with custom definition
        response = client.indices.create(
            index=request.index_name, body=request.index_definition
        )
        return {"message": f"Index '{request.index_name}' created successfully.", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/addDocument")
async def add_document(request: DocumentRequest):
    try:
        if client.indices.exists(index=request.index_name):
            response = client.index(index=request.index_name, id=request.asset_id, body=request.asset_content)
            return {
                "message": f"Document added to index '{request.index_name}'", 
                "response": response
            }
        else:
            raise HTTPException(status_code=400, detail=f"Index '{request.index_name}' does not exist")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/searchOld")
async def search(request: SearchQueryRequest):
    try:
        if not client.indices.exists(index=request.index_name):
            raise HTTPException(status_code=404, detail=f"Index '{request.index_name}' not found.")
        
        response = client.search(index=request.index_name, body={"query": request.search_query})
        return {"message": "Search completed.", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/search")
async def search(request: SearchQueryRequest):
    try:
        if not client.indices.exists(index=request.index_name):
            raise HTTPException(status_code=404, detail=f"Index '{request.index_name}' not found.")
        
        response = client.search(index=request.index_name, body=request.search_query)
        return {"message": "Search completed.", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/hybridSearch")
async def hybrid_search(request: HybridSearchRequest):
    """
    Run a search using a custom search pipeline, e.g., 'nlp-search-pipeline' to do hybrid queries.
    """
    try:
        index_exists = client.indices.exists(index=request.index_name)
        if not index_exists:
            raise HTTPException(
                status_code=404, 
                detail=f"Index '{request.index_name}' not found."
            )
        
        # Construct the request body for the search pipeline
        """
        payload = {
            "query": request.search_query
        }
        """

        hybrid_search_url = f"http://{OPENSEARCH_HOST}:{OPENSEARCH_PORT}/{request.index_name}/_search?search_pipeline={request.pipeline_name}"

        response = requests.get(hybrid_search_url, json=request.search_query, auth=(OPENSEARCH_USERNAME, OPENSEARCH_PWD))
        
        return {"message": "Pipeline search completed.", "response": response.json()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/deleteIndex/{index_name}")
async def delete_index(index_name: str):
    try:
        if not client.indices.exists(index=index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found.")
        
        response = client.indices.delete(index=index_name)
        return {"message": f"Index '{index_name}' deleted successfully.", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
