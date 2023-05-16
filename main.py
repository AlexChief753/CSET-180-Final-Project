from flask import Flask, flash, render_template, request, redirect, session, app
from mysqlx import Session
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text
import mysql.connector
import hashlib
import MySQLdb
import secrets

# use cset 155 db

app = Flask(__name__)
conn_str = 'mysql://root:Rangers1@localhost/ecommerce'
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

app.secret_key = 'mpjGcpxLghHiJePajN0uzA'
app.config['SECRET_KEY'] = 'mpjGcpxLghHiJePajN0uzA'
SECRET_KEY = 'mpjGcpxLghHiJePajN0uzA'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


@app.route('/')
def landing():
    flash('This is a flash message')
    return render_template("base.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    # Duplicate email check
    if request.method == "POST":
        encrypted_password = hashlib.sha224(request.form['password'].encode('utf-8')).hexdigest()
        conn.execute(text(
            "INSERT INTO users VALUES (:firstname, :lastname, :emailaddress, :username, :encrypted_password, :type);"
        ).bindparams(encrypted_password=encrypted_password), request.form)
        conn.commit()
        return render_template('successfulregister.html')
    else:
        return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        emailqueryresult = conn.execute(text("SELECT password FROM users WHERE email_address =:credential").bindparams(credential=request.form.get('credential'))).scalar()
        usernamequeryresult = conn.execute(text("SELECT password FROM users WHERE username = :credential").bindparams(credential=request.form.get('credential'))).scalar()
        inputpass = hashlib.sha224((request.form.get('password')).encode('utf-8')).hexdigest()
        errormsg = ' '
        if emailqueryresult == inputpass or usernamequeryresult == inputpass:
            return render_template('account.html')
        else:
            errormsg = 'Invalid username or password. Please try again.'
            return render_template("login.html", errormsg=errormsg)
    else:
        return render_template("login.html")


# @app.route()

if __name__ == '__main__':
    app.run(debug=True)
