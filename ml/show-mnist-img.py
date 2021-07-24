# Show a mnist image from dataset

from tensorflow.keras.datasets import mnist
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

import matplotlib.pyplot as plt
# %matplotlib inline

# pick a sample to plot
sample = 3
image = X_test[sample]
# plot the sample
fig = plt.figure
plt.imshow(image, cmap='gray')
plt.show()

# num_row = 10
# num_col = 10
#
# num = num_row * num_col
# images = X_train[:num]
# labels = Y_train[:num]
#
# # plot images
# fig, axes = plt.subplots(num_row, num_col, figsize=(1.5*num_col,2*num_row))
# for i in range(num):
#     ax = axes[i//num_col, i%num_col]
#     ax.imshow(images[i], cmap='gray')
#     ax.set_title('Label: {}'.format(labels[i]))
# plt.tight_layout()
# plt.show()

