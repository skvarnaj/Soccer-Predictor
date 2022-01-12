import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import glob
import os
from os import path

path = 'data_zip/archive'
csv_files = glob.glob(os.path.join(path, "*.csv"))

#concatenate files to one file
li = []

for filename in csv_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

epl= pd.concat(li, axis=0, ignore_index=True)

#clean
if len(epl.columns) > 50: 
    epl= epl.iloc[:, 1:23]
#drop referee, HomeTeam, AwayTeam columns
if 'HomeTeam' in epl.columns:
    epl.drop(['HomeTeam'], axis = 1, inplace = True)
if 'AwayTeam' in epl.columns:
    epl.drop(['AwayTeam'], axis = 1, inplace = True)
if 'Referee' in epl.columns:
    epl.drop(['Referee'], axis = 1, inplace = True)
#shuffle df rows and eliminate Halftime metrics
epl = epl.sample(frac=1)
epl = epl[['FTHG', 'FTAG', 'FTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']]

#models
epl = epl.dropna(axis=0)
y = epl.FTHG
epl_features = ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
X = epl[epl_features]
y = y.astype('float32')
X = X.astype('float32')

train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)

#random forest
forest_model = RandomForestRegressor(n_estimators = 100, random_state=1)
forest_model.fit(train_X, train_y)

HG_preds = forest_model.predict(val_X)

class Forest():

    def __init__(self):
        pass

    def predict_home_goals_forest(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        yhat = forest_model.predict(row)
        yhat = float(yhat)
        return yhat