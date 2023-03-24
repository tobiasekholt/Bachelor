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

base_conda_cmd = [str(Path("C:/Users/nikla/anaconda3/Scripts/activate.bat")), 'base']

ngisopenapi_cmd = ["cmd.exe", "/k", "CALL", str(Path("C:/Users/nikla/anaconda3/Scripts/activate.bat")), 'base', '&&', 'CALL', str(Path("C:/Users/nikla/anaconda3/Scripts/conda.exe")), 'activate', 'venv', '&&', 'python', 'C:/Users/nikla/OneDrive/Skrivebord/Bachelor/ngisopenapi/demo.py', '&&', 'conda', 'deactivate']

kartAI_create_cmd = ["cmd.exe", "/k", "CALL", str(Path("C:/Users/nikla/anaconda3/Scripts/activate.bat")), 'base', '&&', 'CALL', str(Path("C:/Users/nikla/anaconda3/Scripts/conda.exe")), 'activate', 'gdal_env', '&&', 'C:/Users/nikla/OneDrive/Skrivebord/Bachelor/kartAI/kai.bat', 'create_training_data', '-n', 'small_test_area', '-c', 'C:/Users/nikla/OneDrive/Skrivebord/Bachelor/kartAI/config/dataset/kartai.json', '--region', 'C:/Users/nikla/OneDrive/Skrivebord/Bachelor/kartAI/training_data/regions/small_building_region.json', '&&', 'CALL', 'conda', 'deactivate', '&&', 'CALL', 'conda', 'deactivate']

kartAI_train_cmd = ["cmd.exe", "/k", "CALL", str(Path("C:/Users/nikla/anaconda3/Scripts/activate.bat")), 'base', '&&', 'CALL', str(Path("C:/Users/nikla/anaconda3/Scripts/conda.exe")), 'activate', 'gdal_env', '&&', 'C:/Users/nikla/OneDrive/Skrivebord/Bachelor/kartAI/kai.bat', 'train', '-dn', 'small_test_area', '-m', 'unet', '-cn', 'test_small_area_unet', '-c', 'C:/Users/nikla/OneDrive/Skrivebord/Bachelor/kartAI/config/ml_input_generator/ortofoto.json', '&&', 'CALL', 'conda', 'deactivate', '&&', 'CALL', 'conda', 'deactivate']


@app.post("/startTraining")
async def start_training():
    subprocess.Popen(base_conda_cmd)
    subprocess.Popen(ngisopenapi_cmd)
    subprocess.Popen(kartAI_create_cmd)
    subprocess.Popen(kartAI_train_cmd)
    
    return {"message": "Training started."}
