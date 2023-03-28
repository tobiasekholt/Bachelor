import os
import subprocess
import shutil
import smtplib
import ssl
import zipfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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

@app.get("/get_files")
async def get_files():
    folder_path = r"C:/Users/nikla/OneDrive/Skrivebord/Bachelor/Bachelor/kartAI/training_data/OrtofotoWMS/3857_563000.0_6623000.0_100.0_100.0/512"
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return {"files": files}

@app.post("/send_zip_file")
async def send_zip_file(request: Request):
    # Extract email from request
    email = await request.json()

    # Get the absolute path of the training data folder
    training_data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'KartAI', 'training_data', 'OrtofotoWMS'))

    # Create a zip file
    zipf = zipfile.ZipFile("OrtofotoWMS.zip", "w", zipfile.ZIP_DEFLATED)

    # Add all the .tif files in the training data folder to the zip file
    for file_name in os.listdir(training_data_folder):
        if file_name.endswith(".tif"):
            file_path = os.path.join(training_data_folder, file_name)
            zipf.write(file_path, file_name)

    # Close the zip file
    zipf.close()

    # Send the email with the zip file as an attachment
    message = Mail(
        from_email="example@sendgrid.com",
        to_emails=email["email"],
        subject="Training data",
        html_content="<strong>Here is the training data you requested</strong>"
    )

    with open("OrtofotoWMS.zip", "rb") as f:
        attachment = f.read()

    encoded_file = base64.b64encode(attachment).decode()

    attachedFile = {
        "content": encoded_file,
        "type": "application/zip",
        "filename": "OrtofotoWMS.zip",
        "disposition": "attachment"
    }

    message.attachment = attachedFile

    try:
        sg = SendGridAPIClient("API_KEY")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    # Delete the zip file
    os.remove("OrtofotoWMS.zip")

    return {"message": "Email sent successfully"}