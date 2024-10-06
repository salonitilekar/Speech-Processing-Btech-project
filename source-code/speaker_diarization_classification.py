import IPython.display as ipd
# % pylab inline
import os
import pandas as pd
import librosa
import glob 
import librosa.display
import random

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from keras.utils.np_utils import to_categorical

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from tensorflow.keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics 

from sklearn.datasets import make_regression
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.model_selection import train_test_split, GridSearchCV

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout 
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor

from keras.callbacks import EarlyStopping

from keras import regularizers

from sklearn.preprocessing import LabelEncoder

from datetime import datetime

import os

#list the files
filelist = (r"D:\train-clean-100.tar\LibriSpeech\train-clean-100\male")
#read them into pandas
print(filelist)

file1 = pd.read_excel (r'C:\Users\stile\Desktop\male\male.xlsx')
df_male = pd.DataFrame(file1)
print(df_male.head())

print("-------------------------------------------------")

file2 = pd.read_excel (r'C:\Users\stile\Desktop\female\female.xlsx')
df_female = pd.DataFrame(file2)
print(df_female.head())

print("-------------------------------------------------")

df_both = pd.concat([df_male, df_female], ignore_index=True)
print(df_both)

df_train = df_both[:7214]
df_validation = df_both[7215:9276]
df_test = df_both[9277:10307]

