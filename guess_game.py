from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/", methods=["GET", "POST"])
def home():

    if "number" not in session:
        session["number"] = random.randint(1, 100)

    message = ""

    if request.method == "POST":

        guess = int(request.form["guess"])
        our_num = session["number"]

        if guess < our_num:
            message = "Guess a higher number"

        elif guess > our_num:
            message = "Guess a lower number"

        else:
            message = "You guessed it right!"

            # Start new game
            session["number"] = random.randint(1, 100)

    return render_template("index.html", message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
