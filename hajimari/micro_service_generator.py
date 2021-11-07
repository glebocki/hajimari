import io
import os
import zipfile
import shutil
from typing import List

from fastapi import Response, UploadFile

from utils import slugify


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


class MicroServiceGenerator:

    def __init__(self):
        return

    def generate(self, service_name: str,
                 model_type: str,
                 model_file: UploadFile
                 ):
        model_file_path: str = f'codeblocks/{model_file.filename}'

        # save file locally
        with open(model_file_path, 'wb') as buffer:
            shutil.copyfileobj(model_file.file, buffer)

        # package files
        res: Response = zip_files([
            "run.sh",
            "codeblocks/README.md",
            "codeblocks/requirements.txt",
            "codeblocks/main.py",
            model_file_path
        ], slugify(service_name))

        # clean up
        os.remove(model_file_path)
    
        return res
