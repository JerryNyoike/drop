# feature extractoring and preprocessing data
import librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import pathlib
import csv

# Preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

#Keras
import keras
from keras import models
from keras import layers

import warnings
warnings.filterwarnings('ignore')

import joblib


# Extracting music and features
# 
# Dataset
# 
# We use [GTZAN genre collection](http://marsyasweb.appspot.com/download/data_sets/) dataset for classification. 
# <br>
# <br>
# The dataset consists of 10 genres i.e
#  * Blues
#  * Classical
#  * Country
#  * Disco
#  * Hiphop
#  * Jazz
#  * Metal
#  * Pop
#  * Reggae
#  * Rock
#  
# Each genre contains 100 songs. Total dataset: 1000 songs

# ## Extracting features from Spectrogram
# The features are extracted from the GTZAN Dataset audio files
# There were originally 30 songs but inorder to increase the size of the 
# dataset they were further split into 3sec audio files each.
# The features were then extracted using librosa into a csv file
# The extracted features were:
# * Mel-frequency cepstral coefficients (MFCC)(20 in number)
# * Spectral Centroid,
# * Zero Crossing Rate
# * Chroma Frequencies
# * Spectral Roll-off.

# header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
# for i in range(1, 21):
#     header += f' mfcc{i}'
# header = header.split()

# with open('beat_data.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(header)

# genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
# for filename in os.listdir(f'D:/Projects/Python/flask/projects/drop/app/static/uploads/beats/previews/'):
#     songname = f'D:/Projects/Python/flask/projects/drop/app/static/uploads/beats/previews/{filename}'
#     y, sr = librosa.load(songname, mono=True, duration=30)
#     chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
#     rmse = librosa.feature.rms(y=y)
#     spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
#     spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
#     rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
#     zcr = librosa.feature.zero_crossing_rate(y)
#     mfcc = librosa.feature.mfcc(y=y, sr=sr)
#     to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'    
#     for e in mfcc:
#         to_append += f' {np.mean(e)}'
#     file = open('beat_data.csv', 'a', newline='')
#     with file:
#         writer = csv.writer(file)
#         writer.writerow(to_append.split())


# Analysing the Data in Pandas
data = pd.read_csv('GTZAN/features_3_sec.csv')

# Dropping unneccesary columns
data = data.drop(['filename'],axis=1)
data = data.drop(['length'],axis=1)
data = data.drop(['chroma_stft_var'],axis=1)
data = data.drop(['rms_var'],axis=1)
data = data.drop(['spectral_centroid_var'],axis=1)
data = data.drop(['spectral_bandwidth_var'],axis=1)
data = data.drop(['rolloff_var'],axis=1)
data = data.drop(['zero_crossing_rate_var'], axis=1)
data = data.drop(['harmony_mean'], axis=1)
data = data.drop(['harmony_var'], axis=1)
data = data.drop(['perceptr_mean'], axis=1)
data = data.drop(['perceptr_var'], axis=1)
data = data.drop(['mfcc1_var'], axis=1)
data = data.drop(['mfcc2_var'], axis=1)
data = data.drop(['mfcc3_var'], axis=1)
data = data.drop(['mfcc4_var'], axis=1)
data = data.drop(['mfcc5_var'], axis=1)
data = data.drop(['mfcc6_var'], axis=1)
data = data.drop(['mfcc7_var'], axis=1)
data = data.drop(['mfcc8_var'], axis=1)
data = data.drop(['mfcc9_var'], axis=1)
data = data.drop(['mfcc10_var'], axis=1)
data = data.drop(['mfcc11_var'], axis=1)
data = data.drop(['mfcc12_var'], axis=1)
data = data.drop(['mfcc13_var'], axis=1)
data = data.drop(['mfcc14_var'], axis=1)
data = data.drop(['mfcc15_var'], axis=1)
data = data.drop(['mfcc16_var'], axis=1)
data = data.drop(['mfcc17_var'], axis=1)
data = data.drop(['mfcc18_var'], axis=1)
data = data.drop(['mfcc19_var'], axis=1)
data = data.drop(['mfcc20_var'], axis=1)

# Encoding the Labels
genre_list = data.iloc[:, -1]
encoder = LabelEncoder()
y = encoder.fit_transform(genre_list)

# Scaling the Feature columns
scaler = StandardScaler()
X = scaler.fit_transform(np.array(data.iloc[:, :-1], dtype = float))

# Dividing data into training and Testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Classification with Keras
# Building our Network
model = models.Sequential()
model.add(layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)))

model.add(layers.Dense(128, activation='relu'))

model.add(layers.Dense(64, activation='relu'))

model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train,
                    y_train,
                    epochs=20,
                    batch_size=128)

test_loss, test_acc = model.evaluate(X_test,y_test)

print('test_acc: ',test_acc)

x_val = X_train[:200]
partial_x_train = X_train[200:]

y_val = y_train[:200]
partial_y_train = y_train[200:]

model = models.Sequential()
model.add(layers.Dense(512, activation='relu', input_shape=(X_train.shape[1],)))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(partial_x_train,
          partial_y_train,
          epochs=30,
          batch_size=512,
          validation_data=(x_val, y_val))
          
results = model.evaluate(X_test, y_test)
print(results)

# Predictions on Test Data
predictions = model.predict(X_test)
print(predictions)
print(np.sum(predictions[0]))
print(np.argmax(predictions[0]))

# Saving the model to memory
model.save('./model/cnn/')

# forest = RandomForestClassifier(n_estimators=100, max_depth= 5)
# forest.fit(X_train, y_train)
# print(forest.score(X_test, y_test)) 

# pred = forest.predict(X_test)
# print(confusion_matrix(y_test, pred))
# print(classification_report(y_test, pred))

# joblib.dump(forest, "./model/forest/random_forest.joblib")