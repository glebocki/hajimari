import tensorflow as tf
from tensorflow import keras


def save_to_file():
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
    test_images[0]
    file = open("sample.jpg", "wb")
    file.write(test_images[0])
    file.close()


save_to_file()

if __name__ == '__main__':
    save_to_file()
