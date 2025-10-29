import os
from flask import Flask, request, render_template
from app.mailer import send_email

# Указываем путь до templates, который на уровень выше
app = Flask(__name__)


@app.route("/")
def form():
    return render_template("form.html")

@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    if send_email(name, email, message):
        return render_template("success.html"), 200
    else:
        return render_template("error.html"), 400

if __name__ == "__main__":
    app.run(debug=True)
