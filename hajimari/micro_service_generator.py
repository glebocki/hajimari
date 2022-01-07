import io
import json
import os
import shutil
import zipfile
from typing import List

import tensorflow as tf
from fastapi import Response, UploadFile
from fastapi.templating import Jinja2Templates
from tensorflow import keras

from utils import slugify

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
    CODEBLOCKS_PATH = 'codeblocks/'

    def __init__(self):
        return

    def generate(self,
                 service_name: str,
                 model_type: str,
                 model_file: UploadFile
                 ):
        model_file_path: str = f'{self.CODEBLOCKS_PATH}{model_file.filename}'

        # Save model file locally
        self._save_model(model_file, model_file_path)

        # Add model to config file
        config = {
            "model": {
                "name": model_file.filename
            }
        }
        self._save_config(config)

        input_dimensions = self._get_model_input_dimensions(model_file_path)
        input_payload = self._generate_payload_shape(input_dimensions, 'float')
        self._render_and_save_main(input_payload)

        # Package files for the response
        res: Response = zip_files([
            f'{self.CODEBLOCKS_PATH}README.md',
            f'{self.CODEBLOCKS_PATH}requirements.txt',
            f'{self.CODEBLOCKS_PATH}main.py',
            f'{self.CODEBLOCKS_PATH}config.json',
            model_file_path
        ], slugify(service_name))

        # Clean up
        os.remove(model_file_path)

        return res

    def _save_config(self, config):
        with open(f'{self.CODEBLOCKS_PATH}/config.json', "w") as outfile:
            json.dump(config, outfile, indent=4, sort_keys=True)

    def _render_and_save_main(self, input_payload: str):
        tm = templates.get_template("main.py.j2")
        main_rendered = tm.render({"payload": input_payload})

        with open(f'{self.CODEBLOCKS_PATH}main.py', 'w') as text_file:
            text_file.write(main_rendered)

    @staticmethod
    def _generate_payload_shape(dimensions: int, base_type: str):
        """Generate payload dimensions. Example: List[List[float]]."""
        input_payload = base_type
        for i in range(0, dimensions + 1):
            input_payload = f'List[{input_payload}]'
        return input_payload

    @staticmethod
    def _get_model_input_dimensions(model_file_path: str):
        model: tf.keras.Model = keras.models.load_model(model_file_path)
        model_config = model.get_config()
        # This is undocumented in Tensorflow API
        batch_input_shape = model_config["layers"][0]["config"]["batch_input_shape"]
        input_dimensions = len(batch_input_shape) - 1
        return input_dimensions

    @staticmethod
    def _save_model(model_file, model_file_path):
        with open(model_file_path, 'wb') as buffer:
            shutil.copyfileobj(model_file.file, buffer)
