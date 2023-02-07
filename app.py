from flask import Flask, request, render_template, redirect, flash, jsonify
from surveys import Question, Survey, satisfaction_survey
app = Flask(__name__)

responses = []

@app.route('/')
def home_page():
    return render_template('base.html',satisfaction_survey=satisfaction_survey)

@app.route('/start', methods=["POST"])
def start():
    responses = []
    return redirect('/questions/0')

@app.route('/questions/<int:num>', methods=['POST'])
def question_page(num):
    question = satisfaction_survey.questions[num]
    return render_template('question.html',question_num = num, question = question)

@app.route("/answer", methods=["POST"])
def question_handle():
    choice = request.form.get['choices']
    responses.append(choice)
    return redirect(f'/questions/0')
