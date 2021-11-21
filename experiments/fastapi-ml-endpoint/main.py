from typing import Optional, List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel
import matplotlib.pyplot as plt
from numpy import ndarray

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


class_names = ["0", "1", "2", "3", "4",
               "5", "6", "7", "8", "9"]


@app.post("/api/ml/predict")
def ml_upload_img(payload: List[List[float]]):
    foo = np.array(payload)
    print("foo")
    print(foo)

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
    test_images = test_images[:1]
    reshape = test_images.reshape(-1, 28 * 28)
    print("reshape")
    print(reshape)

    """
RGB (Red, Green, Blue) are 8 bit each.
The range for each individual colour is 0-255 (as 2^8 = 256 possibilities).
The combination range is 256*256*256.

By dividing by 255, the 0-255 range can be described with a 0.0-1.0 range where 0.0 means 0 (0x00) and 1.0 means 255 (0xFF).
    """
    test_images = reshape / 255.0  # divides all elements
    print(test_images)

    input_samples = test_images

    # PREDICT
    predictions: ndarray = model.predict(foo)
    # predictions: ndarray = model.predict(input_samples)

    predictions_list: list = predictions.tolist()
    print(type(predictions_list))
    print(predictions_list)
    return {
        "classNames": class_names,
        "humanReadable": human_readable_answers(predictions_list),
        "predictions": predictions_list
    }

    # answers = human_readable_answers(predictions)
    # return answers


def human_readable_answers(predictions):
    """
    Turn predictions into Human readable answers
    """
    answers = []

    for i in range(len(predictions)):
        argmax = np.argmax(predictions[i])
        answer = class_names[argmax]
        print(answer)
        answers.append(answer)
    return answers
