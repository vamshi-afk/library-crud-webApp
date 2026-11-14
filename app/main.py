from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import books, members, borrow
from app.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Library of Arch")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(books.router)
app.include_router(members.router)
app.include_router(borrow.router)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})
