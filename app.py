from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from model import Forest, Percentages
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
    forest = Forest()
    percentages = Percentages()
    XG_home = forest.predict_home_goals(shotsh, shotsa, targeth, targeta, foulsh, foulsa, cornersh, cornersa,
                                        yellowh, yellowa, redh, reda)
    XG_away = forest.predict_away_goals(shotsh, shotsa, targeth, targeta, foulsh, foulsa, cornersh, cornersa,
                                        yellowh, yellowa, redh, reda)
    home_win_percentage = percentages.home_percentage(shotsh, shotsa, targeth, targeta, foulsh, foulsa, cornersh, cornersa,
                                        yellowh, yellowa, redh, reda)
    away_win_percentage = percentages.away_percentage(shotsh, shotsa, targeth, targeta, foulsh, foulsa, cornersh, cornersa,
                                        yellowh, yellowa, redh, reda)
    draw_percentage = percentages.draw_percentage(shotsh, shotsa, targeth, targeta, foulsh, foulsa, cornersh, cornersa,
                                        yellowh, yellowa, redh, reda)

    return render_template('prediction.html', form_data = form_data, targeth = targeth, shotsh = shotsh, foulsh = foulsh,
    cornersh = cornersh, yellowh = yellowh, redh = redh, targeta = targeta, shotsa = shotsa, foulsa = foulsa,
    cornersa = cornersa, yellowa = yellowa, reda = reda, XG_home = XG_home, XG_away = XG_away, percentages = percentages,
    home_win_percentage = home_win_percentage, away_win_percentage = away_win_percentage, draw_percentage = draw_percentage)

@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template('homestats.html', title = 'homestats')

@app.route('/homestats', methods = ['GET', 'POST'])
def homestats():
    return render_template('homestats.html', title = 'homestats')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)