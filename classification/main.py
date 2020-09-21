import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import graphviz

from sklearn.tree import export_graphviz
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

# a = np.array(data)
# print("Numpy mean =", np.mean(a, axis=0))
# print("Numpy std =", np.std(a, axis=0))

# [Step] Preprocessing
# print(data)
# data.head()
# data.describe()

# print("[ Default ]")
# print(data.head(10))
# data[
#     ["Glucose_concentration", "Blood_pressure", "Triceps", "Insulin", "BMI", "Pedigree"]
# ] = data[
#     ["Glucose_concentration", "Blood_pressure", "Triceps", "Insulin", "BMI", "Pedigree"]
# ].replace(
#     0, np.NaN
# )
# print("\n")
# print("[ Reset 0 to NaN ]")
# print(data.head(10))
# print("\n")
# print(data.isnull().sum())
# # print(data[data['Pedigree'].isnull()])

# export csv check dataset
# df = pd.DataFrame(
#     data,
#     columns=[
#         "Number_prenant",
#         "Glucose_concentration",
#         "Blood_pressure",
#         "Triceps",
#         "Insulin",
#         "BMI",
#         "Pedigree",
#         "Age",
#         "Class",
#         "Group",
#     ],
# )
# df.to_csv(
#     r"C:\Users\Smurf\Desktop\Decision Tree\dataset\export_dataframe.csv",
#     index=False,
#     header=True,
# )

# data["Glucose_concentration"].fillna(data["Glucose_concentration"].mean(), inplace=True)
# data["Blood_pressure"].fillna(data["Blood_pressure"].mean(), inplace=True)
# data["Triceps"].fillna(data["Triceps"].median(), inplace=True)
# data["Insulin"].fillna(data["Insulin"].median(), inplace=True)
# data["BMI"].fillna(data["BMI"].median(), inplace=True)
# data["Pedigree"].fillna(data["Pedigree"].median(), inplace=True)
# print("\n")
# print(data.isnull().sum())


# def plot_box(data, cols, col_x="Class"):
#     for col in cols:
#         sns.set_style("whitegrid")
#         sns.boxplot(col_x, col, data=data)
#         plt.xlabel(col_x)  # Set text for the x axis
#         plt.ylabel(col)  # Set text for y axis
#         plt.show()


num_cols = [
    "Font-size",
    "Font-weight",
    "Word-same",
    "Line-height",
    "State-price",
]

# plot_box(data, num_cols)

print("\n")
X = data[num_cols]
y = data["Class"]

# scale = StandardScaler()

# Find mean and std [ z = (x-u) / s ]
# X = scale.fit_transform(X)

# print("[ Mean ]\n", f"{X.mean(axis=0)}\n")

# print("[ Standard ]\n", f"{X.std(axis=0)}\n")

# print(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

param_grid = {"max_depth": np.arange(1, 10), "criterion": ["entropy", "gini"]}

find_dept = GridSearchCV(DecisionTreeClassifier(), param_grid)
find_dept.fit(X_train, y_train)
find_dept.best_estimator_

print("Best max_dept:", find_dept.best_estimator_)

tree = DecisionTreeClassifier(max_depth=9)
tree.fit(X_train, y_train)
y_pred = tree.predict(X_test)

# print("X_Train, Y_Train", tree.score(X_train, y_train))
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))


export_graphviz(tree, out_file="mytree.dot")
with open("mytree.dot") as f:
    dot_graph = f.read()
graphviz.Source(dot_graph)
# print(graphviz.Source(export_graphviz(tree)).source)

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
