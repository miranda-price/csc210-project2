from flask import Flask, render_template
import json
import random

class Question:
    def __init__ (self, name, question, answer, options):
        self.name = name
        self.question = question
        self.answer = answer
        self.options = options
    def shuffle(self):
        newOrder = []
        for i in range(0, 4):
            x = self.options.pop(random.randrange(4-i))
            newOrder.append(x)
        self.options = newOrder
        
class Option:
    def __init__ (self, option, id):
        self.option = option
        self.id = id

def getData():
    f = open("questions.json")
    data = json.load(f)
    f.close()
    return data

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
    data = getData()
    historyQuestions = []
    devQuestions = []
    for i in range(len(data["history"])):
        question = data["history"]["q" + str(i+1)]
        options = [Option(question["answer"], "hq" + str(i+1) + "-1"), Option(question["wrong1"], "hq" + str(i+1) + "-1"), Option(question["wrong2"], "hq" + str(i+1) + "-1"), Option(question["wrong3"], "hq" + str(i+1) + "-1")]
        newQuestion = Question("hq" + str(i+1), question["question"], question["answer"], options)
        newQuestion.shuffle()
        historyQuestions.append(newQuestion)
    for i in range(len(data["development"])):
        question = data["development"]["q" + str(i+1)]
        options = [Option(question["answer"], "dq" + str(i+1) + "-1"), Option(question["wrong1"], "dq" + str(i+1) + "-1"), Option(question["wrong2"], "dq" + str(i+1) + "-1"), Option(question["wrong3"], "dq" + str(i+1) + "-1")]
        newQuestion = Question("hq" + str(i+1), question["question"], question["answer"], options)
        newQuestion.shuffle()
        devQuestions.append(newQuestion)
    for i in range(0, 4):
        historyQuestions.pop(random.randrange(8-i))
    for i in range(0, 6):
        devQuestions.pop(random.randrange(12-i))
    return(render_template("test.html", history = historyQuestions, dev = devQuestions))