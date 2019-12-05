from flask import Flask, jsonify
from  classes1 import lista as lista

app = Flask(__name__)

@app.route("/")
def listar_festival():
    return jsonify ({'lista': lista()})

app.run(debug=True, port = 4999)