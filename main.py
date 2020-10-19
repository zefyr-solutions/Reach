from flask import Flask, redirect, render_template, session, flash, url_for, request
from flask_mysqldb import MySQL
from passlib.hash import argon2
import yaml

app = Flask(__name__)
app.secret_key = "hello"

# Loading database connection data from "resources\db.yaml"
db = yaml.load(open("resources/db.yaml"))

#Setting up database connection credentials and initialization of MySQL object
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST" :

        #If no input, redirect back
        if ((request.form["user_name"] == "") or (request.form["password"] == "")):
            flash("Enter Credentials!")
            return redirect(url_for("home"))

        user_name = request.form["user_name"]
        password = request.form["password"]

        #Checking with database for username and password
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id,password,role FROM users where user_name = %s ",[user_name])
        row = cur.fetchone()

        #If username is found on database,
        if row:
            #Checking password is correct or not
            if (argon2.verify(password,row[1])):
                session["user_id"] = row[0]
                session["role"] = row[2]
                flash("Login Succesful")
                return redirect(url_for("home"))
            else:
                flash("Login Failed")
                return redirect(url_for("home"))
        else:
            flash("Could not find user")
            return redirect(url_for("home"))
    else:
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
