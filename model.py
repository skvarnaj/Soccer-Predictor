from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
from os import path
import pandas as pd
import glob

# declare file paths
path = 'data_zip/archive'
csv_files = glob.glob(os.path.join(path, "*.csv"))

# functions
def prep_data():
    """Preps soccer game data for modeling
    """
    # put each csv as df into list
    li = []

    for filename in csv_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    # conact all df's together
    epl= pd.concat(li, axis=0, ignore_index=True)

    # keep only relevant columns
    epl = epl[['FTHG', 'FTAG', 'FTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']]
    
    # dropna values
    epl = epl.dropna(axis=0)

    # shuffle data
    epl = epl.sample(frac=1)

    return epl

def create_home_xg():
    """Creates xg for home team model
    """
    epl = prep_data()

    # set features
    y = epl.FTHG.astype('float')
    home_features = ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
    X = epl[home_features]

    train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)

    # random forest
    forest_model_home = RandomForestRegressor(n_estimators = 100, random_state=1)
    forest_model_home.fit(train_X, train_y)

    return forest_model_home

def create_away_xg():
    """Creates xg for away team model
    """
    epl = prep_data()

    # set features
    y = epl.FTAG.astype('float')
    away_features = ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
    X = epl[away_features]

    train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)

    # random forest
    forest_model_away = RandomForestRegressor(n_estimators = 100, random_state=1)
    forest_model_away.fit(train_X, train_y)

    return forest_model_away

def percent_model():
    """Creates win, loss, draw percentage model
    """
    epl = prep_data()

    y = epl.FTR
    features = ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
    X = epl[features]
    X = X.astype('float')

    train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)

    model = RandomForestClassifier(random_state=0)
    model.fit(train_X, train_y)
    #percent_model.predict_proba(val_X)

    return model

class Goals():
    """Predicts home and away xg from column inputs
    """
    def __init__(self):
        pass

    def predict_home_goals(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        forest_model_home = create_home_xg()
        yhat = forest_model_home.predict(row)
        yhat = float(yhat)
        return yhat
    
    def predict_away_goals(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        forest_model_away = create_away_xg()
        yhat = forest_model_away.predict(row)
        yhat = float(yhat)
        return yhat

class Percentages():
    """Predicts win, loss, draw precentage based on column inputs
    """
    def __init__(self):
        pass

    def home_percentage(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        perc_model = percent_model()
        yhat = perc_model.predict_proba(row)[0][2]
        yhat = 100*(float(yhat))
        yhat = round(yhat, 2)
        yhat = f'{yhat}%'
        return yhat
    
    def away_percentage(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        perc_model = percent_model()
        yhat = perc_model.predict_proba(row)[0][0]
        yhat = 100*(float(yhat))
        yhat = round(yhat, 2)
        yhat = f'{yhat}%'
        return yhat
    
    def draw_percentage(self, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR):
        row = [[HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR]]
        perc_model = percent_model()
        yhat = perc_model.predict_proba(row)[0][1]
        yhat = 100*(float(yhat))
        yhat = round(yhat, 2)
        yhat = f'{yhat}%'
        return yhat
    

# percent_model = percent_model()
#probs = pd.DataFrame(percent_model.predict_proba(val_X),
#                 index=val_X.index,
#                 columns=percent_model.classes_)

