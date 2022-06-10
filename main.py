from flask import Flask, render_template, request, jsonify

domain = '0.0.0.0'
app = Flask(__name__)

@app.route('/', methods=['post', 'get'])
def main_form():
    if request.method == 'POST':
        return request.form
    return render_template("MainForm.html")


if __name__ == '__main__':
    app.run()
