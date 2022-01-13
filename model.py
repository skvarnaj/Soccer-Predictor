import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error
import glob
import os
from os import path

path = 'data_zip/archive'
path_relative = '/Users/joeskvarna/Desktop/Soccer_Predictor/data_zip/archive'
csv_files = glob.glob(os.path.join(path_relative, "*.csv"))

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
#dropna
epl = epl.dropna(axis=0)

#models

#Home Goals
y = epl.FTHG
home_features = ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
X = epl[home_features]
y = y.astype('float32')
X = X.astype('float32')

train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)

#random forest
forest_model_home = RandomForestRegressor(n_estimators = 100, random_state=1)
forest_model_home.fit(train_X, train_y)

HG_preds = forest_model_home.predict(val_X)

#Away Goals
y = epl.FTAG
away_features = ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
X = epl[away_features]
y = y.astype('float32')
X = X.astype('float32')

train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)

#random forest
forest_model_away = RandomForestRegressor(n_estimators = 100, random_state=1)
forest_model_away.fit(train_X, train_y)

#class to call forest predictors for expected home and away goals
class Forest():

    def __init__(self):
        pass

    def predict_home_goals(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        yhat = forest_model_home.predict(row)
        yhat = float(yhat)
        return yhat
    
    def predict_away_goals(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        yhat = forest_model_away.predict(row)
        yhat = float(yhat)
        return yhat

#win loss draw percentage
#create dummy variables
epl
epl['FTD'] = (epl['FTR'] == 'D').astype('int')
epl['FTHW'] = (epl['FTR'] == 'H').astype('int')
epl['FTAW'] = (epl['FTR'] == 'A').astype('int')
epl.head()

#home win percentage
y = epl.FTHW
features = ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
X = epl[features]
y = y.astype('float32')
X = X.astype('float32')

train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)

reg_model_home = RandomForestRegressor(random_state=0)
reg_model_home.fit(train_X, train_y)

#away win percentage
y = epl.FTAW
features = ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
X = epl[features]
y = y.astype('float32')
X = X.astype('float32')

train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)

reg_model_away = RandomForestRegressor(random_state=0)
reg_model_away.fit(train_X, train_y)

#draw percentage
y = epl.FTD
features = ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
X = epl[features]
y = y.astype('float32')
X = X.astype('float32')

train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)

reg_model_draw = RandomForestRegressor(random_state=0)
reg_model_draw.fit(train_X, train_y)


#class for win percentages
class Percentages():
    
    def __init__(self):
        pass
    
    def home_win_percentage(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        yhat = reg_model_home.predict(row)
        yhat = 100*(float(yhat))
        yhat = f'{yhat}%'
        return yhat
        
    def away_win_percentage(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        yhat = reg_model_away.predict(row)
        yhat = 100*(float(yhat))
        yhat = f'{yhat}%'
        return yhat
           
    def draw_percentage(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        yhat = reg_model_draw.predict(row)
        yhat = 100*(float(yhat))
        yhat = f'{yhat}%'
        return yhat







