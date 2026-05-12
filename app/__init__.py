from flask import *
import os
import json
import sqlite3
import random
import urllib

app = Flask(__name__)

app.secret_key = "er34546;'546;'3;'3453453kl345l;45k34905uidkldg593495io;dfop"

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DBC = DB.cursor()

DBC.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, reviews TEXT, bio TEXT, favorites TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")


@app.route("/")
def main():
    file = open("Data/card_info.csv")
    data = file.read().replace("\n", "\\n")
    
    return render_template("jstest.html", testingtesting = data)
    # return "<title>Senioritis</title>\n<h1>Got This Working</h1>\n<br>\n<br>\n<p>yay</p>"

@app.route("/encyclopedia")
def encyclopedia():
    file=open("Data/cards.csv")
    data=file.read()
    print (data)
    return render_template("encyclopedia.html", data=data)

@app.route("/logout")
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
      return redirect(url_for('homepage'))
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

    c.execute("INSERT INTO users VALUES (?, ?, ?, NULL, NULL, NULL)",
    (username, password, reviews))

    db.commit()
    db.close()

    session['username'] = username
    if 'rated_games' not in session:
        session['rated_games']=[]
    session.permanent=True
    return redirect(("/"))

if __name__ == "__main__":
    app.debug=True
    app.run()
