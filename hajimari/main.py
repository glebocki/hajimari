import os

import uvicorn
from fastapi import FastAPI, Response, Request, File, Form, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from micro_service_generator import MicroServiceGenerator

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
    if not service_name:
        raise HTTPException(400, detail="Parameter service name must not be empty")

    extension = os.path.splitext(ml_model.filename)[1]
    if extension != ".h5" or ml_model.content_type != "application/octet-stream":
        raise HTTPException(400, detail="Invalid file type")

    return MicroServiceGenerator().generate(service_name, model_type, ml_model)


if __name__ == "__main__":
    uvicorn.run(app,
                host="127.0.0.1",
                port=8000)
