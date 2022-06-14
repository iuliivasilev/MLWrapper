import pandas as pd
from flask import Flask, render_template, request, session, redirect
from waitress import serve

import datetime
import os
import random
import datasets
import forecast
import matplotlib.pyplot as plt

domain = '0.0.0.0'
app = Flask(__name__, static_url_path='/static')
app.secret_key = "test"


def save_function(func, name=""):
    plt.figure()
    img_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f") + '.png'
    img_path = os.path.join(os.path.dirname(__file__), "static", img_name).replace('/', '\\')
    relative_path = os.path.join("\\static", img_name).replace('/', '\\')
    for fn in func:
        plt.step(fn.x, fn(fn.x), where="post")

    plt.ylim(0, 1)
    plt.title(name)
    plt.savefig(img_path, format='png')
    return relative_path


def save_path_by_names():
    X_path, y_path, model_path = forecast.create_model(dataset_name=session['dataset_name'],
                                                       model_name=session['model_name'])
    session['X_path'] = X_path
    session['y_path'] = y_path
    session['model_path'] = model_path
    return


def init_session():
    session['dataset_name'] = 'PBC'
    session['model_name'] = 'CoxPH'
    return


@app.route('/', methods=['post', 'get'])
def main_form():
    init_session()
    return render_template("MainForm.html")


@app.route('/select', methods=['post', 'get'])
def select_form():
    kwargs = {
        'params':{
                  'models': ['CoxPH', 'KaplanMeier'],
                  'datasets': ['PBC', 'GBSG']
        }
    }
    if request.method == 'POST':
        if request.form['submit_button'] == 'submit':
            session['dataset_name'] = request.form.get('datasets')
            session['model_name'] = request.form.get('models')
            save_path_by_names()
    return render_template("SelectForm.html", **kwargs)


@app.route('/forecast', methods=['post', 'get'])
def forecast_form():
    kwargs = {
        'forecast': False
    }
    if request.method == 'POST':
        if request.form['submit_button'] == 'submit':
            if not('model_path' in session):
                save_path_by_names()
            number = request.form.get('number_observ')
            X = pd.read_csv(session['X_path'])
            y = pd.read_csv(session['y_path'])
            model = datasets.load_pickle(session['model_path'])
            X = X.iloc[[int(number)], :]
            y = y.iloc[int(number), :]

            kwargs['forecast'] = True
            kwargs['outcome'] = y['cens']
            kwargs['true_time'] = y['time']
            # kwargs['predict_time'] = -1*model.predict(X)
            kwargs['survival'] = save_function(model.predict_survival_function(X), "Survival")
            kwargs['hazard'] = save_function(model.predict_cumulative_hazard_function(X), "Hazard")
            print(kwargs)
    return render_template("ForecastForm.html", **kwargs)


if __name__ == '__main__':
    serve(app, host=domain, port=5000, threads=4, connection_limit=300)
