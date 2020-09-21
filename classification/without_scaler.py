import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from numpy.lib.npyio import load
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import accuracy_score, f1_score
from sklearn import tree


data = pd.read_csv("C:/Users/Smurf/Desktop/Engine/dataset/dataset.csv")

num_cols = [
    "Font-size",
    "Font-weight",
    "Word-same",
    "Line-height",
    "Color",
    "State-price",
]

# plot_box(data, num_cols)

print("\n")
X = data[num_cols]
y = data["Class"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

param_grid = {"max_depth": np.arange(1, 10), "criterion": ["entropy", "gini"]}

find_dept = GridSearchCV(DecisionTreeClassifier(), param_grid)
find_dept.fit(X_train, y_train)
find_dept.best_estimator_

print("Best max_dept:", find_dept.best_estimator_)

tree = DecisionTreeClassifier(max_depth=2)
tree.fit(X_train, y_train)
y_pred = tree.predict(X_test)

# print("X_Train, Y_Train", tree.score(X_train, y_train))
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))


# Export Model
import joblib

filename = "model.h5"
path_model = "C:/Users/Smurf/Desktop/Engine/model/"
joblib.dump(tree, path_model + filename)

# Load Model
loaded_model = joblib.load(path_model + filename)
result = loaded_model.score(X_test, y_test)
# print(loaded_model.predict(X_test))
# print("Result", result)
