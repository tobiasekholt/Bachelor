import subprocess
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Response

app = FastAPI()

# Mount the different directories for static files
static_dirs = ["static", "static/resources", "static/scripts"]
for dir_name in static_dirs:
    app.mount(f"/{dir_name}", StaticFiles(directory=dir_name), name=dir_name)

templates = Jinja2Templates(directory="static/pages")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/{page}.html", response_class=HTMLResponse)
async def read_page(request: Request, page: str):
    return templates.TemplateResponse(f"{page}.html", {"request": request})

@app.get("/favicon.ico")
async def favicon():
    return Response(content="", media_type="image/x-icon")

@app.post("/startTraining")
async def start_training():
    subprocess.call(['python', 'start.py'])
    return {"message": "Training process started successfully"}
