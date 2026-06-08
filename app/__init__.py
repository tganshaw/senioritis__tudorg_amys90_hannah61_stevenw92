from flask import *
import os
import json
import sqlite3
import random
import urllib
import csv


MAX_DECK_SIZE = 8
NUM_CARDS = 25

app = Flask(__name__)

app.secret_key = "er34546;'546;'3;'3453453kl345l;45k34905uidkldg593495io;dfop"

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DBC = DB.cursor()

DBC.execute("""CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT,
    bio TEXT,
    img TEXT,
    deck1 TEXT,
    deck2 TEXT,
    numWins INT,
    gamesPlayed INT,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);""")

DBC.execute("""CREATE TABLE IF NOT EXISTS all_cards(
    cardId INTEGER,
    name TEXT,
    health INTEGER,
    attack INTEGER,
    defense INTEGER,
    speed INTEGER,
    atkName TEXT,
    atkDesc TEXT,
    numWins INT,
    gamesPlayed INT
);""")

DBC.execute("""CREATE TABLE IF NOT EXISTS game_cards(
    gameId INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    name TEXT,
    health INTEGER,
    attack INTEGER,
    defense INTEGER,
    speed INTEGER,
    atkName TEXT,
    atkDesc TEXT,
    FOREIGN KEY (atkName, atkDesc) REFERENCES all_cards(atkName, atkDesc)
);""")

DBC.execute("""CREATE TABLE IF NOT EXISTS games(
    deck TEXT,
    num_turns INT,
    state TEXT,
    username TEXT
    );""")

with open('Data/cards.csv', 'r') as f:
    d = f.read().replace("/n", "")[:-1]
    new_d = []
    for i in d.split("\n")[1:]:
        new_d.append(i.split(","))
    #print(new_d)

dval=new_d[0]
DBC.execute("INSERT INTO all_cards(cardId, name, health, attack, defense, speed, atkName, atkDesc) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (int(dval[0]), dval[1], int(dval[2]), int(dval[3]), int(dval[4]), int(dval[5]), dval[6], dval[7]))
#DBC.execute("INSERT OR IGNORE INTO all_cards(cardId, name, health, attack, defense, speed, atkName, atkDesc) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (int(dval[0]), dval[1], int(dval[2]), int(dval[3]), int(dval[4]), int(dval[5]), dval[6], dval[7]))

DB.close()

@app.route("/favicon.ico")
def favicon():
    return send_file("favicon.ico")

@app.route("/")
def main():
    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    if "username" not in session:
        return redirect(url_for("loginhtml"))
    username=session["username"]
    c.execute("SELECT * FROM users where username=?;",(username,))
    deck=c.fetchall()
    if deck==None:
        return redirect(url_for("loginhtml"))
    else:
        return redirect(url_for("home"))

@app.route("/game")
def game():
    if 'username' not in session:
        return redirect(url_for("loginhtml"))

    check_deck = ""
    with sqlite3.connect(DB_NAME) as db:
        c = db.cursor()
        c.execute("SELECT deck1 FROM users WHERE username = ?", (session["username"],))
        check_deck = c.fetchone()

        if check_deck is not None:
            check_deck = check_deck[0]
        else:
            check_deck = ""

    if check_deck == "":
        return encyclopedia(error="Missing deck. Please add 8 cards.")
        #return render_template("encyclopedia.html", error="Missing deck. Please add 8 cards.")

    if(check_deck[0] == ";"):
        check_deck = check_deck[1::]


    deck_arr = check_deck.split(";");
    if(len(deck_arr) != 8):
        num = len(deck_arr)
        if (num == 7):
            return encyclopedia(error=f"Current deck is incomplete. You need to add {(8-num)} more card.")
        return encyclopedia(error=f"Current deck is incomplete. You need to add {(8-num)} more cards.")
        #return redirect(url_for("encyclopedia.html", error=f"Current deck is incomplete. You need to add {(8-num)} more cards."))
    random.shuffle(deck_arr)
    check_deck = ";".join(deck_arr)

    opp_deck = ""
    opp_deck_arr = []
    for i in range(0,8):
        opp_deck_arr.append(str(random.randint(0, NUM_CARDS - 1)))

    opp_deck = ";".join(opp_deck_arr)
    file = open("Data/cards.csv")
    data = file.read().replace("\n", "\\n")

    hardmode = 0
    if "hard" in request.args:
        hardmode = 20
    return render_template("jstest.html", testingtesting = data, user_deck = check_deck, opp_deck = opp_deck, hard_mode = hardmode)

@app.route("/encyclopedia")
def encyclopedia(error=""):
    file=open("Data/cards.csv")
    data=file.read().replace("\n","\\n")
    return render_template("encyclopedia.html", data=data, error=error)

@app.route("/win")
def win():
    return render_template("win.html")

@app.route("/lose")
def lose():
    return render_template("lose.html")

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    profile_icons = [
        "/static/profilepic/pic1.png",
        "/static/profilepic/pic2.png",
        "/static/profilepic/pic3.png",
        "/static/profilepic/pic4.png",
        "/static/profilepic/pic5.png"
    ]
    if 'username' in session:
        user = session["username"]
    else:
        user = ""

    with sqlite3.connect(DB_NAME) as db:
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (session["username"],))
        user = c.fetchone()
        deck1=user[4]
        deck2=user[5]

        if user is None:
            session.pop("username")
            return redirect(url_for('login'))

        if request.method == 'POST' and 'profile_icon' in request.form:
            icon = request.form.get("profile_icon")
            print(f"\n{icon}\n")
            c.execute("UPDATE users SET img = ? WHERE username = ?", (icon, session["username"]))
            db.commit()
            return redirect(url_for('profile'))
    sprite = user[3]

    file=open("Data/cards.csv")
    data = file.read().replace("\n", "\\n")
    return render_template("profile.html",profile_icons=profile_icons, user=user[0], sprite=sprite,data=data,deck1=deck1,deck2=deck2)

@app.route("/home")
def home():
    return render_template("homepage.html", user=session["username"])

@app.route("/card/<card_id>", methods=["GET","POST"])
def card(card_id):
    file=open("Data/cards.csv")
    data = file.read().replace("\n", "\\n")
    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    username=session["username"]
    c.execute("SELECT * FROM users where username=?",(username,))
    temp=c.fetchall()
    deck1=(temp[0][4])
    deck2=(temp[0][5])
    return render_template("card.html",data=data,deck1=deck1,deck2=deck2,card_id=int(card_id))

@app.route("/addDeck1/<card_id>")
def addD1(card_id):
    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    username=session["username"]
    c.execute("SELECT * FROM users where username=?;",(username,))
    deck=c.fetchall()
    deck=deck[0][4]
    if deck is None:
        deck = ""
    deck=deck.split(";")

    if(deck.count(str(card_id))<2 and deck.count(";")< MAX_DECK_SIZE):
        deck=";".join(deck)
        print("hi")
        deck+=";"+card_id
        c.execute("UPDATE users SET deck1=? where username=?",(deck,username,))
        db.commit()
    else:
        deck=";".join(deck)
        print("no")

    db.close()
    return redirect(url_for("card",card_id=card_id))


@app.route("/removeDeck1/<card_id>")
def rmD1(card_id):
    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    username=session["username"]
    c.execute("SELECT * FROM users where username=?;",(username,))
    deck=c.fetchall()
    deck=deck[0][4]
    deck=deck.split(";")
    if str(card_id) in deck:
        deck.remove(str(card_id))
    deck=";".join(deck)
    print(deck)
    c.execute("UPDATE users SET deck1=? where username=?",(deck,username,))
    db.commit()
    db.close()
    return redirect(url_for("card",card_id=card_id))

@app.route("/addDeck2/<card_id>")
def addD2(card_id):
    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    username=session["username"]
    c.execute("SELECT * FROM users where username=?;",(username,))
    deck=c.fetchall()
    deck=deck[0][5]
    deck=deck.split(";")

    if(deck.count(str(card_id))<2 and deck.count(";")< MAX_DECK_SIZE):
        deck=";".join(deck)
        print("hi")
        deck+=";"+card_id
        c.execute("UPDATE users SET deck2=? where username=?",(deck,username,))
        db.commit()
    else:
        deck=";".join(deck)
        print("no")
    db.close()
    return redirect(url_for("card",card_id=card_id))


@app.route("/removeDeck2/<card_id>")
def rmD2(card_id):
    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    username=session["username"]
    c.execute("SELECT * FROM users where username=?;",(username,))
    deck=c.fetchall()
    deck=deck[0][5]
    deck=deck.split(";")
    if str(card_id) in deck:
        deck.remove(str(card_id))
    deck=";".join(deck)
    print(deck)
    c.execute("UPDATE users SET deck2=? where username=?",(deck,username,))
    db.commit()
    db.close()
    return redirect(url_for("card",card_id=card_id))

@app.route("/clearDeck1")
def cD1():
    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    username=session["username"]
    c.execute("UPDATE users SET deck1=? where username=?",("",username,))
    db.commit()
    db.close()
    return redirect(url_for("profile"))

@app.route("/clearDeck2")
def cD2():
    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    username=session["username"]
    c.execute("UPDATE users SET deck2=? where username=?",("",username,))
    db.commit()
    db.close()
    return redirect(url_for("profile"))

@app.route("/send_stats")
def send_stats():
    if "state" not in request.args or "num_turns" not in request.args or "deck" not in request.args or "username" not in session:
        return redirect("/")
    state = request.args["state"]
    num_turns = request.args["num_turns"]
    deck = request.args["deck"]
    username = session["username"]
    print(f"{state} in {num_turns} turns with {deck}")

    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    c.execute("INSERT INTO games VALUES (?, ?, ?, ?);", (deck, num_turns, state, session["username"]))
    db.commit()
    db.close()

    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    c.execute("SELECT numWins, gamesPlayed FROM users WHERE username = ?;", (username, ))
    fetch = c.fetchall()
    if fetch is not None:
        fetch = fetch[0]

    numWins = fetch[0]
    gamesPlayed = fetch[1]

    gamesPlayed+= 1
    if state == "win":
        numWins += 1

    c.execute("UPDATE users SET numWins = ?, gamesPlayed = ? WHERE username = ?;", (numWins, gamesPlayed, username, ))
    db.commit()
    db.close()

    split_deck = deck.split(",")
    for card in split_deck:
        db=sqlite3.connect(DB_NAME)
        c=db.cursor()
        c.execute("SELECT numWins, gamesPlayed FROM all_cards WHERE cardId = ?;", (card, ))
        fetch = c.fetchall()
        if fetch is not None:
            fetch = fetch[0]

        numWins = fetch[0]
        gamesPlayed = fetch[1]

        gamesPlayed+= 1
        if state == "win":
            numWins += 1

        c.execute("UPDATE all_cards SET numWins = ?, gamesPlayed = ? WHERE cardId = ?;", (numWins, gamesPlayed, card, ))
        db.commit()
        db.close()


    # add to game database
    # on leaderboard page, show top useres by winrate
    return "stats logged"

@app.route("/leaderboard")
def leaderboard():
    if "username" not in session:
        return redirect("/")

    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    c.execute("SELECT * FROM games;")
    fetch = c.fetchall()


    game_arr = []
    if fetch is None:
        game_arr = "No Games Finished Yet"
    else:
        for game in fetch:
            this_game = {}
            deck = game[0].split(",")
            this_game["deck"] = deck
            this_game["turns"] = game[1]
            this_game["state"] = game[2]
            this_game["player"] = game[3]
            game_arr.append(this_game)

    card_list = []
    with open("Data/cards.csv", "r") as f:
        data = csv.DictReader(f)
        for row in data:
            card_list.append(row)

    card_dict = {}
    for game in game_arr:
        print(game)
        if game["state"] == "win":
            game_state = 1
        else:
            game_state = 0

        game_card_arr = []
        for card in game["deck"]:
            if card not in game_card_arr:
                game_card_arr.append(card)
        print(game_card_arr)
        for card in game_card_arr:
            if card_list[int(card)]["name"] not in card_dict:
                card_dict[card_list[int(card)]["name"]] = game_state
            else:
                card_dict[card_list[int(card)]["name"]] += game_state

    card_dict = dict(sorted(card_dict.items(), key=lambda item: item[1], reverse=True))

    cards_list = ""
    for card in card_dict:
        cards_list += f"{card}: {card_dict[card]}<br>"

    ## getting users with most wins

    user_dict = {}
    for game in game_arr:
        if game["state"] == "win":
            game_state = 1
        else:
            game_state = 0
        if game["player"] not in user_dict:
            user_dict[game["player"]] = game_state
        else:
            user_dict[game["player"]] += game_state

    user_dict = dict(sorted(user_dict.items(), key=lambda item: item[1], reverse=True))
    users_list = ""
    for user in user_dict:
        users_list += f"{user}: {user_dict[user]}<br>"

    return render_template("leaderboard.html", cards_list = cards_list, users_list = users_list)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/login.html")
def loginhtml():
    if 'username' in session:
        return redirect("/")
    return render_template("login.html")

@app.route("/register.html")
def registerhtml():
    if 'username' in session:
        return redirect("/")
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
  if 'username' in session:
      return redirect("/")
  if request.method == 'POST':
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
      return render_template('login.html', error="Please enter both username and password")

    db = sqlite3.connect(DB_NAME)
    c = db.cursor()
    c.execute("SELECT username, password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    db.close()

    if not user or user[1] != password:
      text = "Login failed. Invalid username or password."
      return render_template('login.html', error=text)

    session['username'] = username
    return redirect('/')

  return render_template('login.html', error="")

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form.get("username", "").strip()
    # email = request.form.get("email", "").strip() why would we need an email
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")
    reviews=""
    if not username or not password or not confirm:
      return render_template("register.html", error="All fields are required!")

    if password != confirm:
      return render_template("register.html", error="Passwords do not match!")

    db = sqlite3.connect(DB_NAME)
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
      db.close()
      return render_template("register.html", error="Username already taken!")

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, '', '', 0, 0, NULL);",
    (username, password, reviews, "/static/profilepic/pic1.png"))

    db.commit()
    db.close()

    session['username'] = username
    session.permanent=True
    return redirect(("/"))

if __name__ == "__main__":
    app.debug=True
    app.run()
