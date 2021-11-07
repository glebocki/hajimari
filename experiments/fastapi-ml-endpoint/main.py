from typing import Optional

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel

import tensorflow as tf
from tensorflow import keras

import numpy as np

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
    model: tf.keras.Model = keras.models.load_model("mnist_model.h5")

    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

    # train_labels = train_labels[:1000]
    # test_labels = test_labels[:1000]

    # Reside the image - what is the input format here?
    # train_images = train_images[:1000].reshape(-1, 28 * 28) / 255.0
    # print(test_images[:1000])
    test_images = test_images[:1000].reshape(-1, 28 * 28) / 255.0

    input_samples = test_images
    print(input_samples)

    print(model.predict(input_samples))

    predictions = model.predict(input_samples)

    answers = human_readable_answers(predictions)

    return answers


def human_readable_answers(predictions):
    """
    Turn predictions into Human readable answers
    """
    answers = []
    class_names = ["0", "1", "2", "3", "4",
                   "5", "6", "7", "8", "9"]
    for i in range(1000):
        argmax = np.argmax(predictions[i])
        answer = class_names[argmax]
        print(answer)
        answers.append(answer)
    return answers
