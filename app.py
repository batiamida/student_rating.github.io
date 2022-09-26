from flask import Flask, redirect, url_for
from waitress import serve

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect('/hey', code=200)

@app.route('/api/v1/hello-world-27')
def lab_func():
    return "Hello world 27"


serve(app, port=8080)
