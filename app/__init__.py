from flask import *

app = Flask(__name__)

app.secret_key = "er34546;'546;'3;'3453453kl345l;45k34905uidkldg593495io;dfop"

@app.route("/")
def main():
    return render_template("jstest.html")
    # return "<title>Senioritis</title>\n<h1>Got This Working</h1>\n<br>\n<br>\n<p>yay</p>"
    
    
if __name__ == "__main__":
    app.run()