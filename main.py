import pandas as pd
from flask import Flask, render_template, request, session, redirect

from time import strftime
import os
import random, string
import datasets
import forecast
import matplotlib.pyplot as plt

domain = '0.0.0.0'
app = Flask(__name__, static_url_path='/static')
app.secret_key = "test"


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


def save_function(func):
    plt.figure() #strftime("%m%d%Y_%H%M%S")
    name_file = randomword(10) + '.png'
    path_file = os.path.join(os.path.dirname(__file__), "static", name_file).replace('/', '\\')
    shared_path = os.path.join("\\static", name_file).replace('/', '\\')
    for fn in func:
        plt.step(fn.x, fn(fn.x), where="post")

    plt.ylim(0, 1)
    plt.savefig(path_file, format='png')
    return shared_path

@app.route('/', methods=['post', 'get'])
def main_form():
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
            X_path, y_path, model_path = forecast.create_model(dataset_name=request.form.get('datasets'),
                                                               model_name=request.form.get('models'))
            session['X'] = X_path
            session['y'] = y_path
            session['model'] = model_path
        print(session)
    return render_template("SelectForm.html", **kwargs)


@app.route('/forecast', methods=['post', 'get'])
def forecast_form():
    kwargs = {
        'forecast': False
    }
    if request.method == 'POST':
        if request.form['submit_button'] == 'submit':
            number = request.form.get('number_observ')
            print(number)
            X = pd.read_csv(session['X'])
            y = pd.read_csv(session['y'])
            model = datasets.load_pickle(session['model'])
            X = X.iloc[[int(number)], :]

            kwargs['forecast'] = True
            kwargs['predict_time'] = -1*model.predict(X)
            kwargs['survival'] = save_function(model.predict_survival_function(X))
            kwargs['hazard'] = save_function(model.predict_cumulative_hazard_function(X))
            print(kwargs)
    return render_template("ForecastForm.html", **kwargs)


# class MainForm(MethodView):
#
#     def __init__(self):
#         session['a'] = random.randint(1, 10)
#         print("HI")
#
#     def get(self):
#         print(session['a'])
#         return render_template("MainForm.html")
#
#     def post(self):
#         print(session['a'])
#         return request.form
#
# app.add_url_rule('/', view_func = MainForm.as_view('main_form'))

if __name__ == '__main__':
    app.run()
