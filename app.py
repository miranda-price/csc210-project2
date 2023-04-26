import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.types import Integer, String
from flask_login import login_required, UserMixin, LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
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

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    subject = db.Column(db.String(50), unique=False, nullable=False)
    message = db.Column(db.String(5000), nullable=False)

    def __repr__(self):
        return f"Name : {self.name}, Email: {self.email}"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    
db.create_all()

connection = sqlite3.connect('database.db')

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def DisplayHome():
    return(render_template("index.html"))

@app.route('/learn')
def DisplayLearn():
    return(render_template("web-info.html"))

@app.route('/practice')
def DisplayPractice():
    return(render_template("practice.html"))

@app.route('/feedback')
def feedbackform():
    return render_template('contact.html')

@app.route('/sendmessage')
@login_required
def editinv():
    return render_template('sendmessage.html', name=current_user.name)

@app.route("/responses", methods=["GET", "POST"])
def inventory():
    cursor = connection.execute("SELECT * from response ")
    data = cursor.fetchall()
    return render_template("responses.html", data=data)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    # check to make sure login info is right
    email = request.form.get('email')
    password = request.form.get('pwd')
    remember = True if request.form.get('rem') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    return redirect(url_for('sendmessage'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    # adds user to db
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('pwd')

    user = User.query.filter_by(email=email).first()

    if user:
        return redirect(url_for('signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

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
        newQuestion = Question("dq" + str(i+1), question["question"], question["answer"], options)
        newQuestion.shuffle()
        devQuestions.append(newQuestion)
    for i in range(0, 4):
        historyQuestions.pop(random.randrange(8-i))
    for i in range(0, 6):
        devQuestions.pop(random.randrange(12-i))
    return(render_template("test.html", history = historyQuestions, dev = devQuestions))
