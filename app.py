from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRETSHTUFF"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

session_key = 'responses'

@app.route('/')
def home_page():
    return render_template('base.html', survey=satisfaction_survey)

@app.route('/start', methods=["POST"])
def start():
    session[session_key] = []
    return redirect('/questions/0')

@app.route("/answer", methods=['POST'])
def question_handle():
    choice = request.form['choices'] 
    responses = session[session_key] 
    responses.append(choice) 
    session[session_key] = responses 
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/finished')
    if len(responses) > len(satisfaction_survey.questions):
        return redirect('/finished')
    return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:num>')
def question_page(num):
    responses = session.get(session_key)
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/finished')
    if num != len(responses):
        flash('Quit tampering with the URL bucko')
        return redirect(f'/questions/{len(responses)}')
    question = satisfaction_survey.questions[num]
    return render_template('question.html',question_num = num, question = question)

@app.route('/finished')
def finished():
    responses = session.get(session_key)
    return render_template('finished.html')
