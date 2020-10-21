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
                return redirect(url_for("driver"))
            else:
                flash("Login Failed")
                return redirect(url_for("home"))
        else:
            flash("Could not find user")
            return redirect(url_for("home"))
    else:
        return render_template("index.html")

@app.route("/add_user", methods=["POST","GET"])
def add_user():
    if request.method == 'POST':

        if (request.form["name"] == "" or request.form["username"] == "" or request.form["email"] == "" or request.form["phone"] == "" or request.form["password"] == "" or request.form["cpassword"] == ""  or request.form["role"] == ""):
            flash("Enter all the fields")
        else:
            userDetails = request.form
            name = userDetails['name']
            username = userDetails['username']
            email = userDetails['email']
            phone = userDetails['phone']
            role = userDetails['role']
            password = userDetails['password']
            cpassword = userDetails['cpassword']
            if password == cpassword:
                xpassword = argon2.hash(password)
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(user_name,name,email,phone_no,role,password) VALUES(%s,%s,%s,%s,%s,%s)",(username,name,email,phone,role,xpassword))
                mysql.connection.commit()
                cur.close()
                flash("Records inserted")
            else:
                flash("Both passwords must be same")
    else:
        return render_template("add_user.html")

@app.route("/add_product", methods=["POST","GET"])
def add_product():
    if request.method == 'POST':

        if (request.form["pname"] == "" or request.form["bcode"] == "" or request.form["price"] == "" ):
            flash("Enter all the fields")
        else:
            userDetails = request.form
            pname = userDetails['pname']
            bcode = userDetails['bcode']
            price = userDetails['price']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO products(name,barcode,price) VALUES(%s,%s,%s)",(pname,bcode,price))
            mysql.connection.commit()
            cur.close()
            flash("Records inserted")

    else:
        return render_template("add_product.html")

@app.route("/add_customer", methods=["POST","GET"])
def add_customer():
    if request.method == 'POST':

        if (request.form["name"] == "" or request.form["phone_no"] == "" or request.form["email"] == "" or request.form["location"] == ""):
            flash("Enter all the fields")
        else:
            userDetails = request.form
            name = userDetails['name']
            phone_no = userDetails['phone_no']
            email = userDetails['email']
            location = userDetails['location']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO customers(name,phone,email,location) VALUES(%s,%s,%s,%s)",(name,phone_no,email,location))
            mysql.connection.commit()
            cur.close()
            flash("Records inserted")

    else:
        return render_template("add_customer.html")

@app.route("/driver")
def driver():
    return render_template("driver.html")


@app.route("/view_user")
def view_user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_name,name,email,phone_no,role FROM users")
    rows = cur.fetchall()
    return render_template("view_user.html", value=rows)

if __name__ == "__main__":
    app.run(debug=True)
