from flask import Flask, render_template, request
from model import Goals, Percentages, prep_data, create_home_xg, create_away_xg, percent_model
from model_shots import Goal
import io
import os
from flask import Response
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg
matplotlib.use('Agg')

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template("index.html", title = 'landing')

@app.route("/about", methods = ['GET', 'POST'])
def about():
    return render_template("about.html", title = 'about')

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    return render_template("contact.html", title = 'contact')

@app.route("/predictor", methods = ['GET', 'POST'])
def landing():
    return render_template('homestats.html', title = 'homestats')

@app.route('/homestats', methods = ['GET', 'POST'])
def homestats():
    return render_template('homestats.html', title = 'homestats')

@app.route("/temp", methods = ['GET', 'POST'])
def temp():
    return render_template('temp.html', title = 'temp')

@app.route("/preplot", methods = ['GET', 'POST'])
def cordplot():

    return render_template("cordplot.html", title = 'preplot')

@app.route("/plot", methods = ['GET', 'POST'])
def plot():
    form_data = request.form
    xcord = request.form.get('xcord')
    ycord = request.form.get('ycord')
    xcord = int(xcord)
    ycord = int(ycord)
    goal = Goal(xcord, ycord)
    percent = goal.is_goal()
    fig = goal.shot_chart()
    fig.savefig(os.path.join(app.root_path, 'static/myplot.png'),  pad_inches=0, dpi=300)

    return render_template("plot.html", title = 'plot', fig = fig, form_data = form_data, xcord=xcord, ycord=ycord, percent=percent)

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
    goals = Goals()
    percentages = Percentages()
    XG_home = goals.predict_home_goals(shotsh, shotsa, targeth, targeta, foulsh, foulsa, cornersh, cornersa,
                                        yellowh, yellowa, redh, reda)
    XG_away = goals.predict_away_goals(shotsh, shotsa, targeth, targeta, foulsh, foulsa, cornersh, cornersa,
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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)