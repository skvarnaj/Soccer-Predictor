from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from forms import HomeStats, AwayStats
from flask_bootstrap import Bootstrap
app = Flask(__name__)

app.config['SECRET_KEY'] = 'b43e4b51d4f030a6f240c4bf5e41bcf5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

@app.route('/prediction',  methods = ['GET', 'POST'])
def prediction():
    form_data = request.form
    targeth = request.form.get('targeth')
    shotsh = request.form.get('shotsh')
    foulsh = request.form.get('foulsh')
    cornersh = request.form.get('cornersh')
    yellowh = request.form.get('yellowh')
    redh = request.form.get('redh')
    targeta = request.form.get('targeta')
    shotsa = request.form.get('shotsa')
    foulsa = request.form.get('foulsa')
    cornersa = request.form.get('cornersa')
    yellowa = request.form.get('yellowa')
    reda = request.form.get('reda')

    return render_template('prediction.html', form_data = form_data, targeth = targeth, shotsh = shotsh, foulsh = foulsh,
    cornersh = cornersh, yellowh = yellowh, redh = redh, targeta = targeta, shotsa = shotsa, foulsa = foulsa,
    cornersa = cornersa, yellowa = yellowa, reda = reda)

@app.route("/", methods = ['GET', 'POST'])
def index():
    form = HomeStats()
    return render_template('homestats.html', title = 'homestats', form = form)

@app.route('/homestats', methods = ['GET', 'POST'])
def homestats():
    form = HomeStats()
    return render_template('homestats.html', title = 'homestats', form = form)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)