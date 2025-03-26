import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split,GridSearchCV
from preprocessing import Preprocessing
from models import XgBoost

df_test = pd.read_csv("hour.csv")

df_train, df_predict = train_test_split(df_test, test_size=0.2, random_state=42)
# ----------------- pre processing dati
preproc = Preprocessing()
df_train_encod  = preproc.transform_data(df_train, "train")
# preproc.save("training/preprocessing.pkl")
#
# #load
# preproc = Preprocessing.load("training/preprocessing.pkl")
df_test_encod = preproc.transform_data(df_predict, "predict")
df_test = df_test_encod.copy()
df_test_encod.drop(columns=["cnt"], inplace=True)
# ------------------- stima griglia
param_grid = {
    'n_estimators': [400],
    'max_depth': [7],
    'learning_rate': [0.05],
    "min_child_weight": [65],
    "subsample": [0.7],
    "colsample_bynode": [0.7],
    "reg_lambda": [0.5],
}
columns = [
    "mean_fit_time", "std_fit_time", "mean_score_time", "std_score_time",
    "param_colsample_bynode", "param_learning_rate", "param_max_depth",
    "param_min_child_weight", "param_n_estimators", "param_reg_lambda",
    "param_subsample", "params", "split0_test_score", "split1_test_score",
    "split2_test_score", "mean_test_score", "std_test_score", "rank_test_score",
    "split0_train_score", "split1_train_score", "split2_train_score",
    "mean_train_score", "std_train_score"
]

# you must change file patch and file name
XgBoost.grid_search(df_train_encod, target_col="cnt", grid_params=param_grid, file_path=r"C:\Users\loverdegiulio\Desktop", file_name="risultati.xlsx", metrics=columns)

# #train dataset
params = {
'n_estimators': 400,
'max_depth': 7,
'learning_rate': 0.05,
"min_child_weight": 75,
"subsample": 0.75,
"colsample_bynode": 0.7,
"reg_lambda": 0.5}

model = XgBoost(params)
model.train(df_train_encod, target_col="cnt", test_size=0.2, random_state=42)
#model.save("training/xgboost_model.pkl")
#
#
# # Ricarico da file pkl
# loaded_model = XgBoost.load("training/xgboost_model.pkl")
predicted = model.predict(df_test_encod)


#test with df
#rmse
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
rmse = np.sqrt(mean_squared_error(df_test["cnt"], predicted))
mae = mean_absolute_error(df_test["cnt"], predicted)

