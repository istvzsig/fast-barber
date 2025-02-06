from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from api import api_router

app = FastAPI()

templates = Jinja2Templates(directory=str(
    Path(__file__).resolve().parent / "templates"))

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
