from flask import *
import os
import json
import sqlite3
import random
import urllib


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
    atkDesc TEXT
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
    if "username" not in session:
        return redirect(url_for("loginhtml"))
    else:
        return redirect(url_for("profile"))

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
        return redirect(url_for("encyclopedia"))

    if(check_deck[0] == ";"):
        check_deck = check_deck[1::]


    deck_arr = check_deck.split(";");
    if(len(deck_arr) != 8):
        return redirect(url_for("encyclopedia"))
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
        print(user)
    else:
        return(redirect(url_for('login')))

    with sqlite3.connect(DB_NAME) as db:
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (session["username"],))
        user = c.fetchone()
        print(user)
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

@app.route("/encyclopedia")
def encyclopedia():
    file=open("Data/cards.csv")
    data=file.read().replace("\n","\\n")
    return render_template("encyclopedia.html", data=data)

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
    if(deck.count(str(card_id))<2 and deck.count(";")< MAX_DECK_SIZE):
        deck+=";"+card_id
        print(deck)
        c.execute("UPDATE users SET deck1=? where username=?",(deck,username,))
        db.commit()
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
    deck=deck.replace(f";{card_id}","",1)
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
    if(deck.count(str(card_id))<2 and deck.count(";")< MAX_DECK_SIZE):
        deck+=";"+card_id
        c.execute("UPDATE users SET deck2=? where username=?",(deck,username,))
        db.commit()
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
    deck=deck.replace(f";{card_id}","",1)
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


@app.route("/switch")
def switch():
    db=sqlite3.connect(DB_NAME)
    c=db.cursor()
    username=session["username"]
    c.execute("SELECT * FROM users where username=?;",(username,))
    deck=c.fetchall()
    deck1=deck[0][5]
    deck2=deck[0][4]
    c.execute("UPDATE users SET deck1=? where username=?",(deck1,username,))
    c.execute("UPDATE users SET deck2=? where username=?",(deck2,username,))
    db.commit()
    db.close()
    return redirect(url_for("profile"))

@app.route("/logout", methods=["GET","POST"])

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

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, '', '', NULL)",
    (username, password, reviews, "/static/profilepic/pic1.png"))

    db.commit()
    db.close()

    session['username'] = username
    session.permanent=True
    return redirect(("/"))

if __name__ == "__main__":
    app.debug=True
    app.run()
