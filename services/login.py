import uuid
import json
import sys
import requests
from flask import Flask, request, jsonify, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from flask import url_for

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:S@mbamasala123!@localhost:3306/user'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/citi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
###  This microservice contain User, Holdings, and Correlation class
"""
List of Functions for User


Port Number
    - 5010
"""

class Account(db.Model):
    """
        This class is used to store the registered users in the database.
        * Functions
            - __init__(self, username, password, name, age, email, institution, credit)
            - json(self)
    """
    __tablename__ = 'account'
    userid = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    loyaltypoints = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, userid, password, loyaltypoints): #Initialise the objects
        self.userid = userid
        self.password = password
        self.loyaltypoints = loyaltypoints

    def json(self):
        return {"userid": self.userid, "password": self.password, "loyaltypoints": self.loyaltypoints}

#FOR DEBUGGING - eprint()
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)




###########################################################################
@app.route("/index")
def index():
    category = session['category']
    if category == 'cust':
        return render_template("index.html")
    elif category == 'cash':
        return render_template("index2.html")
@app.route("/<filename>")
def path_to_filename(filename):
    return render_template(f"{filename}.html")


@app.route("/loginc", methods=['POST'])
def loginCustomer():
    serviceName = 'loginCustomer'
    data = request.get_json()
    loginid = data['userid']
    loginpassword = data['password']
    category = loginid[:4]
    user = Account.query.filter_by(userid = loginid).first()
    session['category'] = category
    if (user and user.password == loginpassword):
        return redirect(url_for('index'))
    else:
        return jsonify("Login Failed"), 500 


@app.route("/details", methods=['POST'])
def custdetails():
    serviceName = 'custDetails'
    data = request.get_json()
    loginid = data['userid']
    loginpassword = data['password']
    user = Account.query.filter_by(userid = loginid).first()
    if (user and user.password == loginpassword):
        useraccount = {"userid": loginid, "points": user.loyaltypoints}
        return jsonify(useraccount), 200
    else:
        return jsonify("Login Failed"), 500 


        
if __name__ == '__main__':
    app.secret_key="asd"
    app.run(host = '0.0.0.0',port=5010, debug=True)