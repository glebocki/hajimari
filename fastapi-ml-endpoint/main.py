from typing import Optional

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel

import tensorflow as tf
from tensorflow import keras

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


class Predict(BaseModel):
    inputSamples: list[int]


@app.post("/api/ml/predict")
def ml_upload_img(number_image: UploadFile = File(...)):
    # input_samples = predict.inputSamples

    # TODO: Load once - Singleton, research Dependency Injection in FastApi
    # Loading model H5
    model: tf.keras.Model = keras.models.load_model("my_model.h5")

    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

    # train_labels = train_labels[:1000]
    # test_labels = test_labels[:1000]

    # Reside the image - what is the input format here?
    # train_images = train_images[:1000].reshape(-1, 28 * 28) / 255.0
    test_images = test_images[:1000].reshape(-1, 28 * 28) / 255.0

    input_samples = test_images

    predictions = model.predict(input_samples).shape

    return predictions



