from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["web"])

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request},
    )
