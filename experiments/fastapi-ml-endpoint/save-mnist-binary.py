import json

import tensorflow as tf
from numpy import ndarray


def save_to_file():
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

    test_images = test_images[:2]  # take first
    # each image is a 2d 28 by 28 array of 0-255
    reshape = test_images.reshape(-1, 28 * 28)  # reshape from 2d to 1d array

    """
    RGB (Red, Green, Blue) are 8 bit each.
    The range for each individual colour is 0-255 (as 2^8 = 256 possibilities).
    The combination range is 256*256*256.
    
    By dividing by 255, the 0-255 range can be described with a 0.0-1.0 range 
    where 0.0 means 0 (0x00) and 1.0 means 255 (0xFF).
    """
    test_images: ndarray = reshape / 255.0  # divides all elements by 255 float

    test_images_list = test_images.tolist()

    with open('data.json', 'w') as f:
        json.dump(test_images_list, f)


if __name__ == '__main__':
    save_to_file()
