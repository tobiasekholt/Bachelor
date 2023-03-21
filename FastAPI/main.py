from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Mount the different directories for static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/pages", StaticFiles(directory="static/pages"), name="pages")
app.mount("/resources", StaticFiles(directory="static/resources"), name="resources")
app.mount("/scripts", StaticFiles(directory="static/scripts"), name="scripts")

templates = Jinja2Templates(directory="static/pages")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/{file_name}", response_class=HTMLResponse)
async def read_page(request: Request, file_name: str):
    return templates.TemplateResponse(file_name, {"request": request})
