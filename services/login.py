import pika
import uuid
import json
import sys
import requests
from flask import Flask, request, jsonify, render_template, redirect, session
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
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/blog")
def blog():
    return render_template("blog.html")
@app.route("/cart")
def cart():
    return render_template("cart.html")
@app.route("/checkout")
def checkout():
    return render_template("checkout.html")
@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/elements")
def elements():
    return render_template("elements.html")
@app.route("/index")
def index():
    return render_template("index.html")
@app.route("/index2")
def index2():
    return render_template("index2.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/main")
def main():
    return render_template("main.html")
@app.route("/product_details")
def product_details():
    return render_template("product_details.html")
@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/shop")
def shop():
    return render_template("shop.html")
@app.route("/viewvoucher")
def viewvoucher():
    return render_template("vouchers.html")

@app.route("/index")
def index():
    category = session['category']
    if category == 'cust':
        return render_template("index.html")
    elif category == 'cash':
        return render_template("index2.html")

@app.route("/login", methods=['POST'])
def loginCustomer():
    serviceName = 'loginCustomer'
    data = request.get_json()
    loginid = data['userid']
    loginpassword = data['password']
    category = loginid[:5]
    user = Account.query.filter_by(userid = loginid).first()
    session['category'] = category
    if (user and user.password == loginpassword):
        return redirect("/index")
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
        return jsonify(useraccount), 201
    else:
        return jsonify("Login Failed"), 500 


        
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5010, debug=True)