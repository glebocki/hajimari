import io
import json
import os
import shutil
import zipfile
from typing import List

from fastapi import Response, UploadFile

from fastapi.templating import Jinja2Templates

from utils import slugify

from tensorflow import keras

import tensorflow as tf

templates = Jinja2Templates(directory="templates/ml")


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
    codeblocks_path = 'codeblocks/'

    def __init__(self):
        return

    def generate(self,
                 service_name: str,
                 model_type: str,
                 model_file: UploadFile
                 ):
        model_file_path: str = f'{self.codeblocks_path}{model_file.filename}'

        # save model file locally
        with open(model_file_path, 'wb') as buffer:
            shutil.copyfileobj(model_file.file, buffer)

        # add model to a config file
        config = {
            "model": {
                "name": model_file.filename
            }
        }
        self._save_config(config)

        model: tf.keras.Model = keras.models.load_model(model_file_path)

        model_config = model.get_config()
        # this one is undocumented in TF KERAS!!!
        batch_input_shape = model_config["layers"][0]["config"]["batch_input_shape"]

        input_dimensions = len(batch_input_shape) - 1

        # batch_input_shape
        input_payload = "float"
        # Generate payload dimensions. Example: List[List[float]]
        for i in range(0, input_dimensions + 1):
            input_payload = f'List[{input_payload}]'

        # Working templating
        tm = templates.get_template("main.py.j2")
        main_rendered = tm.render({"payload": input_payload})

        with open(f'{self.codeblocks_path}main.py', 'w') as text_file:
            text_file.write(main_rendered)

        # package files
        res: Response = zip_files([
            "run.sh",
            f'{self.codeblocks_path}README.md',
            f'{self.codeblocks_path}requirements.txt',
            f'{self.codeblocks_path}main.py',
            f'{self.codeblocks_path}config.json',
            model_file_path
        ], slugify(service_name))

        # clean up
        os.remove(model_file_path)

        return res

    def _save_config(self, config):
        with open(f'{self.codeblocks_path}/config.json', "w") as outfile:
            json.dump(config, outfile, indent=4, sort_keys=True)