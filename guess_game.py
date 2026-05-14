from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = "secret123"


def reset_game():
    session["number"] = random.randint(1, 100)
    session["guesses"] = 0
    session["clicked"] = []


@app.route("/", methods=["GET", "POST"])
def home():

    # Initialize session
    if "number" not in session:
        reset_game()
        session["best_score"] = None

    message = ""
    show_name_input = False

    if request.method == "POST":

        # =========================
        # CASE 1: Guess button click
        # =========================
        if "guess" in request.form:

            guess = int(request.form["guess"])
            our_num = session["number"]

            session["guesses"] += 1

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

                # update best score
                best = session.get("best_score")
                if best is None or session["guesses"] < best:
                    session["best_score"] = session["guesses"]

                # ask name only first time ever
                if "player_name" not in session:
                    show_name_input = True
                else:
                    reset_game()

        # =========================
        # CASE 2: Name submission
        # =========================
        elif "name" in request.form:

            session["player_name"] = request.form["name"]

            reset_game()

            message = f"Welcome {session['player_name']}! New game started."

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
    reset_game()

    return render_template(
        "index.html",
        message=f"Welcome {session['player_name']}! New game started.",
        clicked=[],
        guesses=0,
        best=session.get("best_score"),
        show_name_input=False
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
