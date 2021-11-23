from typing import List

import numpy as np
import tensorflow as tf
from fastapi import FastAPI
from numpy import ndarray
from tensorflow import keras

app = FastAPI()

class_names = ["0", "1", "2", "3", "4",
               "5", "6", "7", "8", "9"]


@app.post("/api/ml/predict")
def ml_upload_img(payload: List[List[float]]):
    input = np.array(payload)

    # TODO: Load once - Singleton, research Dependency Injection in FastApi
    # Loading model H5
    model: tf.keras.Model = keras.models.load_model("mnist_model.h5")

    # PREDICT
    predictions: ndarray = model.predict(input)

    predictions_list: list = predictions.tolist()
    return {
        "classNames": class_names,
        "humanReadable": human_readable_answers(predictions_list),
        "predictions": predictions_list
    }


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
