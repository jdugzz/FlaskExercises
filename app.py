from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    return render_template('base.html', survey=satisfaction_survey)

@app.route('/start', methods=["POST"])
def start():
    responses.clear()
    return redirect('/questions/0')

@app.route("/answer", methods=['POST'])
def question_handle():
    choice = request.form['choices']
    responses.append(choice)
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/finished')
    if len(responses) > len(satisfaction_survey.questions):
        responses.pop()
        return redirect('/finished')
    return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:num>')
def question_page(num):
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/finished')
    if num != len(responses):
        flash('Quit tampering with the URL bucko')
        return redirect(f'/questions/{len(responses)}')
    question = satisfaction_survey.questions[num]
    return render_template('question.html',question_num = num, question = question)

@app.route('/finished')
def finished():
    return render_template('finished.html', responses=responses)
