import pika
import uuid
import json
import sys
import uuid
import requests
import base64
from PIL import Image
from io import BytesIO
import datetime
import logging
from dateutil.relativedelta import relativedelta
from flask import Flask, request, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from os import environ

from werkzeug.datastructures import Headers
from QR import scanQR, decodeQR, generateQR

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:S@mbamasala123!@localhost:3306/user'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/citi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
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
    voucherid = db.Column(db.Integer, primary_key=True, autoincrement = True)
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
    purchaseid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(64), nullable=False)
    voucherid = db.Column(db.Integer, nullable=False)
    purchasedatetime = db.Column(db.DateTime, nullable=False)
    expirydate = db.Column(db.Date, nullable=False)
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
@app.route("/viewvoucher")
def viewvoucher():
    return render_template("vouchers.html")

@app.route("/buyvoucher", methods=['POST'])
def buyvoucher():
    serviceName = 'buyvoucher'
    data = request.get_json()
    userid = data['userid']
    voucherid = data['voucherid'] # list of vouchers
    credit = data['credit'] # dictionary of credit card info
    #Make Payment
    cost = 0
    for v in voucherid:
        voucher = Voucher.query.filter_by(voucherid = v).first()
        cost += voucher.vouchercost
    if not makepayment(credit, cost):
        return jsonify({"message": "Insufficient Funds"}), 500
    #insert into purchase database
    for v in voucherid:
        voucher = Voucher.query.filter_by(voucherid = v).first()
        points = voucher.voucheramt * 10
        purchaseid = uuid.uuid4().hex[:6].upper()
        purchase = Purchase(purchaseid, userid, v, datetime.datetime.now(), datetime.datetime.now()+relativedelta(years=1), points, "Redeemable")
        while True:
            try:
                db.session.add(purchase)
                db.session.commit
                break
            except:
                purchaseid = uuid.uuid4().hex[:6].upper()
                purchase = Purchase(purchaseid, userid, v, datetime.datetime.now(), points)
    #update loyalty points
    user = Account.query.filter_by(userid = userid).first()
    if user:
        user.loyaltypoints = user.loyaltypoints + points
        db.session.commit
    return jsonify({"message": "Successful Purchase"}), 201

@app.route("/generatevoucher", methods=['POST'])
@cross_origin()
def generate():
    serviceName = 'redeemvoucher'
    data = request.get_json()
    userid = data['userid']
    voucherid = data['voucherid']
    purchase = Purchase.query.filter_by(userid=userid, voucherid=voucherid).first()
    if purchase:
        eprint("hi")
        img = generateQR(purchase.purchaseid)              
        buffer = BytesIO()
        img.save(buffer,format="JPEG")               
        myimage = buffer.getvalue()
        eprint(myimage)
        return (base64.b64encode(myimage)), 200
    else:
        return 500

def makepayment(credit, cost):

    return True

if __name__ == '__main__':
    app.run(host = '127.0.0.1',port=5020, debug=True)