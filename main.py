from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

local_server=True
with open('config.json','r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['server_uri']
db = SQLAlchemy(app)


# Contacts - C should be capital always
#   id,name, phn_num,mgs,email
class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    mgs = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route("/")
@app.route("/index")
def home():
    app.logger.debug('logger function response:')
    return render_template('index.html', params=params)

@app.route("/about")
def about():
    return render_template('/about.html', params=params)

@app.route("/post")
def post():
    return render_template('/post.html', params=params)

@app.route("/contact", methods = ['GET','POST'])
def contact():
    if (request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phn_num')
        mgs = request.form.get('mgs')
        entry = Contacts(name=name, phone_number=phone, mgs=mgs, email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('/contact.html', params=params)


app.run(debug=True)
## True- autometically apply changes to UI
