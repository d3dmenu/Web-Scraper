# Export Model
import joblib
from numpy.lib.npyio import load
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, f1_score

data = pd.read_csv("C:/Users/Smurf/Desktop/Engine/model/datatest.csv")
filename = "model.h5"
path_model = "C:/Users/Smurf/Desktop/Engine/model/"


# [Font-size, Font-weight, Word-same, Line-height, State-price]
data = [[22, 500, 6, 18.4, 0], [14, 300, 0, 18, 0], [21, 400, 2, 20.8, 0]]


# Preprocessing
# scale = StandardScaler()
# data = scale.fit_transform(data)

# Load Model
loaded_model = joblib.load(path_model + filename)
print(loaded_model.predict(data))
