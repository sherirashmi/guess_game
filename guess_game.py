from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = "secret123"


@app.route("/", methods=["GET", "POST"])
def home():

    # Initialize game state
    if "number" not in session:
        session["number"] = random.randint(1, 100)
        session["guesses"] = 0
        session["clicked"] = []
        session["best_score"] = None

    message = ""
    show_name_input = False

    if request.method == "POST":

        guess = int(request.form["guess"])
        our_num = session["number"]

        # track guesses
        session["guesses"] += 1

        # track clicked buttons
        clicked = session.get("clicked", [])
        if guess not in clicked:
            clicked.append(guess)
        session["clicked"] = clicked

        if guess < our_num:
            message = "Guess a higher number"

        elif guess > our_num:
            message = "Guess a lower number"

        else:
            message = f"You guessed it right in {session['guesses']} tries!"

            # best score logic
            best = session.get("best_score")
            if best is None or session["guesses"] < best:
                session["best_score"] = session["guesses"]

            # ask name if first win ever
            if "player_name" not in session:
                show_name_input = True
            else:
                show_name_input = False

    return render_template(
        "index.html",
        message=message,
        clicked=session.get("clicked", []),
        guesses=session.get("guesses", 0),
        best=session.get("best_score"),
        show_name_input=show_name_input
    )


@app.route("/save_name", methods=["POST"])
def save_name():
    session["player_name"] = request.form["name"]

    # reset game after saving name
    session["number"] = random.randint(1, 100)
    session["guesses"] = 0
    session["clicked"] = []

    return render_template("index.html",
                           message=f"Welcome {session['player_name']}! New game started.",
                           clicked=[],
                           guesses=0,
                           best=session.get("best_score"),
                           show_name_input=False)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
