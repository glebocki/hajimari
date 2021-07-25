# Loads a mnist H5 model
# Pick a few of the numbers from data set and try to predict what number the represent.

import os

import tensorflow as tf
from tensorflow import keras

import numpy as np


def main():
    # Loading model H5
    model: tf.keras.Model = keras.models.load_model("mnist_model.h5")

    # Re-evaluate the model

    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

    train_labels = train_labels[:1000]
    test_labels = test_labels[:1000]

    train_images = train_images[:1000].reshape(-1, 28 * 28) / 255.0
    test_images = test_images[:1000].reshape(-1, 28 * 28) / 255.0

    # Evaluate the restored model
    loss, acc = model.evaluate(test_images, test_labels, verbose=2)
    print("Restored model, accuracy: {:5.2f}%".format(100 * acc))

    print(model.predict(test_images).shape)
    # print(model.predict(test_images))

    x_test = test_images
    x_imgs_to_be_predicted = x_test[:3]
    y_pred = model.predict(x_imgs_to_be_predicted)

    print_predicted_labels(y_pred)


def print_predicted_labels(predictions):
    """
    Printing the predicted labels
    """
    print("Predictions: ", predictions)
    print("###")
    print("Prediction 0: ", predictions[0])
    # print(predictions[1])

    class_names = ["0", "1", "2", "3", "4",
                   "5", "6", "7", "8", "9"]
    print("=============")
    print_prediction_statistics(class_names, predictions)

    print("\nHuman readable predictions")
    for i in range(3):
        print(class_names[np.argmax(predictions[i])], " ", end='')


def print_prediction_statistics(class_names, predictions):
    for i in range(10):
        print(" ", class_names[i], "        ", end='')
    print()
    for p in range(3):
        for i in range(10):
            print(predictions[p][i], " ", end='')
        print()


if __name__ == '__main__':
    main()