from flask import Flask, redirect, render_template, session, flash, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import yaml

app = Flask(__name__)

# configuring DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/add_user")
def add_user():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        username = userDetails['username']
        email = userDetails['email']
        phone = userDetails['phone']
        password = userDetails['password']
        cpassword = userDetails['cpassword']
        if password == cpassword:
            xpassword = sha256_crypt.encrypt(password)
        else:
            flash("Both passwords must be same")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(user_name,name,email,phone_no) VALUES(%s,%s,%s,%s)",(username,name,email,phone))
        mysql.connection.commit()
        cur.close()
    return render_template("add_user.html")

if __name__ == "__main__":
    app.run(debug=True)
