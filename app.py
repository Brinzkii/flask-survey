from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "survey"

debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def show_start():
    title = satisfaction_survey.title
    rules = satisfaction_survey.instructions
    # questions = []

    # for question in satisfaction_survey.questions:
    #     questions.append(question.question)

    return render_template("start.html", title=title, rules=rules)


@app.route("/create_session", methods=["POST"])
def create_session():
    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions/<num>")
def show_question(num):
    q_num = int(num)

    if q_num > len(satisfaction_survey.questions) - 1:
        data = session["responses"]
        data.append(responses)
        session["responses"] = data
        return redirect("/thanks")
    elif q_num != len(responses):
        flash("Please complete the questions in order!")
        return redirect(f"/questions/{len(responses)}")
    else:
        question = satisfaction_survey.questions[q_num].question
        choices = Question(question).choices

        return render_template(
            "question.html", question=question, choices=choices, num=q_num
        )


@app.route("/answer/<num>", methods=["POST"])
def log_answer(num):
    answer = list(request.form)
    responses.append(answer[0])

    return redirect(f"/questions/{num}")


@app.route("/thanks")
def show_thanks():
    return render_template("thanks.html")
