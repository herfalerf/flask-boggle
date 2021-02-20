from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "majorkey"

# Make a function to create HTML board
@app.route('/')
def index():
    """Show Home Screen"""

    return render_template("home.html")

@app.route('/boggle')
def game_board():
    """Show New Game Board"""

    new_board = boggle_game.make_board()
    session['game_board'] = new_board




    return render_template("game_board.html")

@app.route('/guess')
def handle_guess():
    """ Take post request and pass to guess check function """
    
    word = request.args["word"]
    board = session["game_board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
