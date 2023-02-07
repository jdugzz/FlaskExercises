from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    return render_template('base.html', satisfaction_survey=satisfaction_survey)

@app.route('/start', methods=['POST'])
def start():
    responses = []
    return redirect('/questions/0')

@app.route("/answer", methods=['POST'])
def question_handle():
    choice = request.form.get['choices']
    responses.append(choice)
    return redirect(f'/questions/0')

@app.route('/questions/<int:num>', methods=['POST'])
def question_page(num):
    question = satisfaction_survey.questions[num]
    return render_template('question.html',question_num = num, question = question)
