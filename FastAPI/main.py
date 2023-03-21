from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import subprocess

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

@app.get("/favicon.ico")
async def favicon():
    return

@app.get("/pages/order.html")
async def read_order():
    file_name = "order.html"
    return templates.TemplateResponse(file_name, {"request": request})

@app.post("/startTraining")
async def startTraining():
    subprocess.call(['cmd.exe', '/c', 'cd ngisopenapi && conda activate venv && python demo.py && conda deactivate && cd ..'])
    subprocess.call(['cmd.exe', '/c', 'cd kartAI && conda activate gdal_env && kai.bat create_training_data -n small_test_area -c config/dataset/kartai.json --region training_data/regions/small_building_region.json && conda deactivate && cd ..'])
    subprocess.call(['cmd.exe', '/c', 'cd kartAI && conda activate gdal_env && kai.bat train -dn small_test_area -m unet -cn test_small_area_unet -c config/ml_input_generator/ortofoto.json'])
    return {"message": "Training started!"}

