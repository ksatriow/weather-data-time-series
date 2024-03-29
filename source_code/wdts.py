# -*- coding: utf-8 -*-
"""ML Intermediate Submission II.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i08EaIeaP0E4VQQcc8Tyxns6keQiqzsb
"""

import numpy as np
    import pandas as pd
    from keras.layers import Dense, LSTM
    import matplotlib.pyplot as plt
    import tensorflow as tf

data_train = pd.read_csv('austin_weather_new.csv')
    data_train.head()

len(data_train)
data_train.shape[0]
len(data_train.index)

data_train.dtypes

data_train['TempHighF'] = data_train.TempHighF.astype(float)
data_train['TempAvgF'] = data_train.TempAvgF.astype(float)
data_train['TempLowF'] = data_train.TempLowF.astype(float)
data_train['DewPointHighF'] = data_train.DewPointHighF.astype(float)
data_train['DewPointAvgF'] = data_train.DewPointAvgF.astype(float)
data_train['DewPointLowF'] = data_train.DewPointLowF.astype(float)
data_train['HumidityHighPercent'] = data_train.HumidityHighPercent.astype(float)
data_train['HumidityAvgPercent'] = data_train.HumidityAvgPercent.astype(float)
data_train['HumidityLowPercent'] = data_train.HumidityLowPercent.astype(float)
data_train.dtypes

data_train.isnull().sum()

dates = data_train['Date'].values
    temp  = data_train['TempAvgF'].values
    dew  = data_train['DewPointAvgF'].values 
    hum  = data_train['HumidityAvgPercent'].values
    
    plt.figure(figsize=(8,5))
    plt.plot(dates, temp)
    plt.title('Rataan Suhu',
              fontsize=20);

    plt.figure(figsize=(8,5))
    plt.plot(dates, dew)
    plt.title('Rataan Dew',
              fontsize=20);

    plt.figure(figsize=(8,5))
    plt.plot(dates, hum)
    plt.title('Rataan Lembab',
              fontsize=20);

def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
        series = tf.expand_dims(series, axis=-1)
        ds = tf.data.Dataset.from_tensor_slices(series)
        ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
        ds = ds.flat_map(lambda w: w.batch(window_size + 1))
        ds = ds.shuffle(shuffle_buffer)
        ds = ds.map(lambda w: (w[:-1], w[1:]))
        return ds.batch(batch_size).prefetch(1)

"""**Model sequential dan Learning Rate pada Optimizer**"""

train_set = windowed_dataset(temp, window_size=60, batch_size=100, shuffle_buffer=1000)
    model = tf.keras.models.Sequential([
      tf.keras.layers.LSTM(60, return_sequences=True),
      tf.keras.layers.LSTM(60),
      tf.keras.layers.Dense(30, activation="relu"),
      tf.keras.layers.Dense(10, activation="relu"),
      tf.keras.layers.Dense(1),
    ])

"""**Training MAE**"""

optimizer = tf.keras.optimizers.SGD(lr=1.0000e-04, momentum=0.9)
    model.compile(loss=tf.keras.losses.Huber(),
                  optimizer = optimizer,
                  metrics=["mae"])
    history = model.fit(train_set,epochs=100)