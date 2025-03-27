# Importing required modules
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

# Initializing FastAPI application
app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Renders the main interface page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Handeling document insertion form submission
@app.post("/insert", response_class=HTMLResponse)
async def insert_document(request: Request, text: str = Form(...)):
     # Sending the document to backend service
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://backend:9567/insert",
                json={"text": text}
            )
            result = response.json()
        except Exception as e:
            result = {"error": str(e)}
    # Returnning updated template with results
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

# Handleing document search form submission
@app.post("/get", response_class=HTMLResponse)
async def get_document(request: Request, text: str = Form(...)):
    async with httpx.AsyncClient() as client:
        try:
            # Query backend service
            response = await client.get(
                "http://backend:9567/get",
                params={"query": text}
            )
            result = response.json()
        except Exception as e:
            result = {"error": str(e)}
    # Returnning updated template with results  
    return templates.TemplateResponse("index.html", {"request": request, "result": result})