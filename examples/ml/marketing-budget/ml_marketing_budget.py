import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# tf.logging.set_verbosity(tf.logging.ERROR)
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

mar_budget    = np.array([60, 80,  100  , 30, 50, 20, 90,  10],  dtype=float)
subs_gained = np.array([160, 200, 240, 100, 140, 80, 220, 60],  dtype=float)

for i,c in enumerate(mar_budget):
  print("{} Market budget = {} new subscribers gained".format(c, subs_gained[i]))

plt.scatter(mar_budget, subs_gained)
plt.xlim(0,120)
plt.ylim(0,260)
plt.xlabel('Marketing Budget(in thousand of Dollars)')
plt.ylabel('Subscribers Gained(in thousand)')
plt.show()


X_train, X_test, y_train, y_test = train_test_split(mar_budget,subs_gained,random_state=42, 
                                                    train_size=0.8, test_size=0.2)

layer_0 = tf.keras.layers.Dense(units=1, input_shape=[1])

model = tf.keras.Sequential([layer_0])

# model = tf.keras.Sequential([
#   tf.keras.layers.Dense(units=1, input_shape=[1])
# ])

model.compile(loss='mean_squared_error',
              optimizer=tf.keras.optimizers.Adam(0.1))

trained_model = model.fit(X_train, y_train, epochs=1000, verbose=False)
print("Finished training the model")

plt.xlabel('Epoch Number')
plt.ylabel("Loss Magnitude")
plt.plot(trained_model.history['loss'])

print(model.predict([80.0]))

y_pred = model.predict(X_test)
print('Actual Values\tPredicted Values')
print(y_test,'   ',y_pred.reshape(1,-1))

print(r2_score(y_test,y_pred))

model.save("marketing-budget-model.h5")