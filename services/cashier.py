import pika
import uuid
import json
import sys
import requests
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from QR import generateQR, scanQR, decodeQR

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

    def __init__(self, userid, password, loyaltypoints): #Initialise the objects
        self.userid = userid
        self.password = password
        self.loyaltypoints = loyaltypoints

    def json(self):
        return {"userid": self.userid, "password": self.password, "loyaltypoints": self.loyaltypoints}

class Voucher(db.Model):
    """
        This class is used to store the registered users in the database.
        * Functions
            - __init__(self, username, password, name, age, email, institution, credit)
            - json(self)
    """
    __tablename__ = 'vouchers'
    voucherid = db.Column(db.Integer(11), Primary_key=True, autoincrement = True)
    vouchername = db.Column(db.String(64), nullable=False)
    vouchercost = db.Column(db.Float(precision=2), nullable=False)
    voucheramt = db.Column(db.Float(precision=2), nullable=False)


    def __init__(self, voucherid, vouchername, vouchercost, voucheramt): #Initialise the objects
        self.voucherid = voucherid
        self.vouchername = vouchername
        self.vouchercost = vouchercost
        self.voucheramt = voucheramt


    def json(self):
        return {"voucherid": self.voucherid, "vouchername": self.vouchername, "vouchercost": self.vouchercost, "voucheramt": self.voucheramt}

class Purchase(db.Model):
    """
        This class is used to store the registered users in the database.
        * Functions
            - __init__(self, username, password, name, age, email, institution, credit)
            - json(self)
    """
    __tablename__ = 'purchase'
    purchaseid = db.Column(db.Integer(11), Primary_key=True)
    userid = db.Column(db.String(64), nullable=False)
    voucherid = db.Column(db.Integer(11), nullable=False)
    purchasedatetime = db.Column(db.Datetime, nullable=False)
    expirydate = db.Column(db.Datetime, nullable=False)
    points = db.Column(db.Float(precision=2), nullable=False)
    status = db.Column(db.String(64), nullable=False)

    def __init__(self, purchaseid, userid, voucherid, purchasedatetime, expirydate, points, status): #Initialise the objects
        self.purchaseid = purchaseid
        self.userid = userid
        self.voucherid = voucherid
        self.purchasedatetime = purchasedatetime
        self.expirydate = expirydate
        self.points = points
        self.status = status

    def json(self):
        return {"purchaseid": self.purchaseid, "userid": self.userid, "voucherid": self.voucherid, 
        "purchasedatetime": self.purchasedatetime, "expirydate": self.expirydate, "points": self.points, "status": self.status}

#FOR DEBUGGING - eprint()
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)




###########################################################################


@app.route("/scanvoucher", methods=['GET'])
def scanvoucher():
    serviceName = 'scanvoucher'
    data = request.get_json()
    purchaseid = data['purchaseid']
    purchase = Purchase.query(purchaseid=purchaseid).first()
    if purchase:
        purchase.status = "Redeemed"
        db.session.commit()


def updateDB():
    return

        
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5030, debug=True)