from typing import List

from fastapi import FastAPI, Response, Request, Form
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
def generate(service_name=Form(...)) -> Response:
    return zip_files(["README.md"], slugify(service_name))


def slugify(value: str):
    # TODO: normalize filename
    return value


def zip_files(filenames: List[str], zip_filename: str = "archive") -> Response:
    # zip_filename = "archive.zip"
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")

    for filePath in filenames:
        # Calculate path for file in zip
        fdir, filename = os.path.split(filePath)
        # Add file, at correct path
        zf.write(filePath, filename)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename + ".zip"}'
    })

    return resp
