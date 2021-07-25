# Show a mnist image from dataset

import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist

(X_train, Y_train), (X_test, Y_test) = mnist.load_data()


# %matplotlib inline

def plot_single_sample():
    # pick a sample to plot
    sample = 111
    image = X_test[sample]
    # plot the sample
    fig = plt.figure
    plt.imshow(image, cmap='gray')
    plt.show()


def plot_multiple_samples(rows: int, columns: int):
    num = rows * columns
    images = X_train[:num]
    labels = Y_train[:num]

    # plot images
    fig, axes = plt.subplots(rows, columns, figsize=(1.5 * columns, 2 * rows))
    for i in range(num):
        ax = axes[i // columns, i % columns]
        ax.imshow(images[i], cmap='gray')
        ax.set_title('Number: {}'.format(labels[i]))

    plt.tight_layout()
    plt.show()


plot_single_sample()
plot_multiple_samples(10, 10)
