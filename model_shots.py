from os import path
import pandas as pd
import requests
import seaborn as sns
import matplotlib
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
matplotlib.use('Agg')

# path and load data
DATA_DIR = '/Users/joeskvarna/Desktop/learn-to-code-soccer/data/'
shots = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

# create soccer field as the plot
map_img = mpimg.imread('./static/soccer_field.png')

# rescale axis to match soccer field dimensions
shots['x1'] = shots['x1'] * 1.2
shots['y1'] = shots['y1'] * .75

# clean
shots['goal'] = shots['goal'].astype('int')


# MODEL
# set up features and y
y = shots.goal
features = ['x1', 'y1', 'dist_ft']
X = shots[features]
y = y
X = X.astype('float32')

# Option later: make dummies for foot, etc.

# train model
train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)
model = RandomForestClassifier(random_state=0)
model.fit(train_X, train_y)
model.predict_proba(val_X)

# probability matrix
probs = pd.DataFrame(model.predict_proba(val_X),
                  index=val_X.index,
                  columns=model.classes_)
probs.head()



class Goal:
    # allows for plotting a set of defined x-y coordinates to 1) plot and 2) get percent chance of a goal
    def __init__(self, x1, y1):
        self.x = x1
        self.y = y1

    def is_goal(self):
        # returns percent chance coordinates result in goal
        dist_ft = ((120-self.x)*3) + ((abs(37.5-self.y))*3)
        row = [[self.x, self.y, dist_ft]]
        yhat = model.predict_proba(row)[0,1]
        y = yhat*100
        y = round(y, 2)
        y=f'{y}%'
        return y
    
    def shot_chart(self, **kwargs):
        # returns the plot of x-y and a note with percent chance of goal
        df = pd.DataFrame([[self.x, self.y]])
        df.columns = ['x1', 'y1']
        g = sns.relplot(data = df, x = 'x1', y = 'y1', kind = 'scatter', **kwargs)
        g.set(yticks=[], xticks=[], xlabel= self.is_goal(), ylabel=None)
        g.despine(left = True, bottom = True)
        for ax in g.fig.axes:
            ax.imshow(map_img, zorder=0, extent=[0,120,75,0])          
        return g

def ask():
    # asks user for x-y coordinates and performs Goal.shot_chart(x,y) defined above
    x = float(input('x value: '))
    y = float(input('y value: '))
    a = Goal(x,y)
    return a.shot_chart()