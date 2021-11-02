from typing import List

from fastapi import FastAPI, Response, Request, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
import zipfile
import io

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate(service_name: str = Form(...),
                   model_type: str = Form(...),
                   ml_model: UploadFile = File(...)) -> Response:
    print("Service Name: " + service_name)
    print("Model Type: " + model_type)
    print("Model file: " + ml_model.filename)
    return zip_files(["README.md"], slugify(service_name))


def slugify(value: str):
    # TODO: normalize filename
    return value


def zip_files(file_names: List[str], zip_filename: str = "archive") -> Response:
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")

    for file_path in file_names:
        # Calculate path for file in zip
        file_dir, filename = os.path.split(file_path)
        # Add file, at correct path
        zf.write(file_path, filename)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename + ".zip"}'
    })

    return resp
