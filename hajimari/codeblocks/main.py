from typing import List

import numpy as np
import tensorflow as tf
import uvicorn
from fastapi import FastAPI
from numpy import ndarray
from tensorflow import keras

app = FastAPI()

class_names = ["0", "1", "2", "3", "4",
               "5", "6", "7", "8", "9"]

# TODO: Load once - Singleton, research Dependency Injection in FastApi
# Loading model H5
try:
    model: tf.keras.Model = keras.models.load_model("mnist_model.h5")
except OSError:
    print("Oops! Could not load Machine Learning model. Make sure it is in the same directory as the service.")
    raise


@app.post("/api/ml/predict")
def ml_upload_img(payload: List[List[float]]):
    predict_input = np.array(payload)

    # PREDICT
    predictions: ndarray = model.predict(predict_input)

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
        answers.append(answer)
    return answers


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
