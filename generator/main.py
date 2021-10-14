from typing import Optional, List

from fastapi import FastAPI, Response
from pydantic import BaseModel

import os
import zipfile
import io

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


def zipfiles(filenames: List[str]):
    zip_filename = "archive.zip"

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
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })

    return resp


@app.get("/image_from_id/")
async def image_from_id(image_id: int):
    return zipfiles(["README.md"])
