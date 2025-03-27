# Importing required libraries
from fastapi import FastAPI
from elasticsearch import Elasticsearch
import os
import uuid
import requests
from bs4 import BeautifulSoup

# Initializing FastAPI application
app = FastAPI()

es_host = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
es_port = os.getenv("ELASTICSEARCH_PORT", "9567")
es = Elasticsearch([f"http://{es_host}:{es_port}"])

INDEX_NAME = "documents"  # Name of the Elasticsearch index

# Fetching and extracting paragraphs from a Wikipedia page
def fetch_wikipedia_paragraphs(url, num_paragraphs):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = []
    # Selecting paragraphs from Wikipedia's main content div
    for p in soup.select('div.mw-parser-output > p'):
        text = p.get_text().strip()
        if text:
            paragraphs.append(text)
            if len(paragraphs) >= num_paragraphs:
                break
    return paragraphs

# Createing Elasticsearch index if it doesn't exist and seeding initial data
def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "id": {"type": "keyword"},
                        "text": {"type": "text"}
                    }
                }
            }
        )
# Checking document count
    count = es.count(index=INDEX_NAME)['count']
    if count < 4:
         # Fetching first 4 paragraphs from India's Wikipedia page
        paragraphs = fetch_wikipedia_paragraphs("https://en.wikipedia.org/wiki/India", 4)
        # Inserting paragraphs into Elasticsearch
        for p in paragraphs:
            doc_id = uuid.uuid4().hex
            es.index(
                index=INDEX_NAME,
                id=doc_id,
                body={
                    "id": doc_id,
                    "text": p
                }
            )

create_index()

# Api Endpoints
@app.get("/get")
async def get_best_document(query: str):
    # Geting endpoint to retrieve best matching document
    body = {
        "query": {
            "match": {
                "text": query
            }
        },
        "size": 1,
        "sort": [{"_score": {"order": "desc"}}]
    }
    # Executing search
    res = es.search(index=INDEX_NAME, body=body)
    if res['hits']['hits']:
        return res['hits']['hits'][0]['_source'] # Returnning the best match
    return {"error": "No documents found"}

@app.post("/insert")
async def insert_document(document: dict):
    # POST endpoint to insert new document
    doc_id = uuid.uuid4().hex
    # Index document in Elasticsearch
    res = es.index(
        index=INDEX_NAME,
        id=doc_id,
        body={
            "id": doc_id,
            "text": document.get("text", "")
        }
    )
    return {"id": doc_id, "result": "created"}