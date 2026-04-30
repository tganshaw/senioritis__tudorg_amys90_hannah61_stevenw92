from flask import *

app = Flask(__name__)

@app.route("/")
def main():
    return "<title>Senioritis</title>\n<h1>Got This Working</h1><br><br><p>yay</p>"
    
    
if __name__ == "__main__":
    app.run()