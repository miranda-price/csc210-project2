from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def DisplayHome():
    return(render_template("index.html"))

@app.route('/learn')
def DisplayLearn():
    return(render_template("web-info.html"))

@app.route('/practice')
def DisplayPractice():
    return(render_template("practice.html"))

@app.route('/test')
def DisplayTest():
    return(render_template("test.html"))