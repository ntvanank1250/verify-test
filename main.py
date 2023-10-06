from fastapi import FastAPI,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from verify_api import verify

app = FastAPI()
app.include_router(verify.router)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# engine = database.engine

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)

# uvicorn main:app --reload --port 8080