import pika
import uuid
import json
import sys
import requests
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

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
    userid = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    loyaltypoints = db.Column(db.Float(precision=2), nullable=False)
    walletamt = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, userid, password, loyaltypoints, walletamt): #Initialise the objects
        self.userid = userid
        self.password = password
        self.loyaltypoints = loyaltypoints
        self.walletamt = walletamt

    def json(self):
        return {"userid": self.userid, "password": self.password, "loyaltypoints": self.loyaltypoints, "walletamt": self.walletamt}

#FOR DEBUGGING - eprint()
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)




###########################################################################


@app.route("/login", methods=['POST'])
def loginCustomer():
    serviceName = 'loginCustomer'
    data = request.get_json()
    loginid = data['userid']
    loginpassword = data['password']
    category = loginid[:5]
    user = Account.query.filter_by(userid = loginid).first()
    if (user and user.password == loginpassword):
        return jsonify("Login Success"), 201
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
        useraccount = {"points": user.loyaltypoints, "walletAmt": user.walletamt}
        return jsonify(useraccount), 201
    else:
        return jsonify("Login Failed"), 500 


        
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5010, debug=True)