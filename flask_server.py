import flask
from flask import *

app = Flask(__name__)

@app.route("/",methods=['GET'])
def index():
    return "<h1> Lineage C2 Server</h1>"

if __name__=='__main__':
    app.run(debug=True)
