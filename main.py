from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Import the API router
from api import api_router

app = FastAPI()

# Templates setup
templates = Jinja2Templates(directory=str(
    Path(__file__).resolve().parent / "templates"))

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the API routers
app.include_router(api_router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
