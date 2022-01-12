from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from forms import HomeStats, AwayStats
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b43e4b51d4f030a6f240c4bf5e41bcf5'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
#db = SQLAlchemy(app)

#class Todo(db.Model):
   # id = db.Column(db.Integer, primary_key = True)
    #content = db.Column(db.String(200), nullable = False)

@app.route('/prediction',  methods = ['GET', 'POST'])
def prediction():
    return render_template('prediction.html')

@app.route("/", methods = ['GET', 'POST'])
def index():
    form = HomeStats()
    if form.validate_on_submit:
        flash('Thanks for submitting')
        #return redirect(url_for('prediction'))
    return render_template('homestats.html', title = 'homestats', form = form)

@app.route('/homestats', methods = ['GET', 'POST'])
def homestats():
    form = HomeStats()
    return render_template('homestats.html', title = 'homestats', form = form)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)