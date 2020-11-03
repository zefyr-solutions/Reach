from flask import Flask, redirect, render_template, session, flash, url_for, request
from flask_mysqldb import MySQL
from passlib.hash import argon2
from db import connect
import yaml
import os
import pymysql

app = Flask(__name__)
app.secret_key = "hello"


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
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT user_id,password,role FROM users where user_name = %s ",[user_name])
            row = cur.fetchone()
        cnx.close()
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
    if 'user_id' in session:
        if request.method == 'POST':

            if (request.form["name"] == "" or request.form["username"] == "" or request.form["email"] == "" or request.form["phone"] == "" or request.form["password"] == "" or request.form["cpassword"] == ""  or request.form["role"] == ""):
                flash("Enter all the fields")
                return render_template("add_user.html")
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
                    cnx = connect()
                    with cnx.cursor() as cur:
                        cur.execute("INSERT INTO users(user_name,name,email,phone_no,role,password) VALUES(%s,%s,%s,%s,%s,%s)",(username,name,email,phone,role,xpassword))
                    cnx.commit()
                    cnx.close()
                    flash("Records inserted")
                    return redirect(url_for("view_user"))
                else:
                    flash("Both passwords must be same")
                    return redirect(url_for("add_user"))
        else:
                    return render_template("add_user.html")
    else:
        return redirect(url_for('static', filename='403-forbidden-error.jpg'))

@app.route("/add_product", methods=["POST","GET"])
def add_product():
    if 'user_id' in session:
        if request.method == 'POST':

            if (request.form["pname"] == "" or request.form["bcode"] == "" or request.form["price"] == "" ):
                flash("Enter all the fields")
            else:
                userDetails = request.form
                pname = userDetails['pname']
                bcode = userDetails['bcode']
                price = userDetails['price']
                cnx = connect()
                with cnx.cursor() as cur:
                    cur.execute("INSERT INTO products(name,barcode,price) VALUES(%s,%s,%s)",(pname,bcode,price))
                cnx.commit()
                cnx.close()
                flash("Records inserted")
                return redirect(url_for("view_product"))

        else:
            return render_template("add_product.html")
    else:
        return redirect(url_for('static', filename='403-forbidden-error.jpg'))

@app.route("/add_customer", methods=["POST","GET"])
def add_customer():
    if 'user_id' in session:
        if request.method == 'POST':

            if (request.form["name"] == "" or request.form["phone_no"] == "" or request.form["email"] == "" or request.form["location"] == ""):
                flash("Enter all the fields")
            else:
                userDetails = request.form
                name = userDetails['name']
                phone_no = userDetails['phone_no']
                email = userDetails['email']
                location = userDetails['location']
                cnx = connect()
                with cnx.cursor() as cur:
                    cur.execute("INSERT INTO customers(name,phone,email,location) VALUES(%s,%s,%s,%s)",(name,phone_no,email,location))
                cnx.commit()
                cnx.close()
                flash("Records inserted")
                return redirect(url_for("view_customer"))

        else:
            return render_template("add_customer.html")
    else:
        return redirect(url_for('static', filename='403-forbidden-error.jpg'))

@app.route("/driver")
def driver():
    return render_template("driver.html")


@app.route("/view_user")
def view_user():
    if 'user_id' in session:
        if request.args.get("customer_id") :
            customer_id = request.args.get("customer_id")
            cnx = connect()
            with cnx.cursor() as cur:
                cur.execute("SELECT name,email,phone,loaction FROM customers where customer_id = %s ",[customer_id])
                row = cur.fetchone()
            return render_template("view_user_specific.html")
        else :
            cnx = connect()
            with cnx.cursor() as cur:
                cur.execute("SELECT user_name,name,email,phone_no,role,user_id FROM users")
                rows = cur.fetchall()
            cnx.close()
            return render_template("view_user.html", value=rows)
    else:
        return redirect(url_for('static', filename='403-forbidden-error.jpg'))

@app.route("/view_customer")
def view_customer():
    if 'user_id' in session:
        if request.args.get("customer_id") :
            customer_id = request.args.get("customer_id")
            cnx = connect()
            with cnx.cursor() as cur:
                cur.execute("SELECT name,email,phone,location,customer_id FROM customers where customer_id = %s ",[customer_id])
                row = cur.fetchone()
            cnx.close()
            return render_template("view_customer_specific.html", row=row)
        else :
            cnx = connect()
            with cnx.cursor() as cur:
                cur.execute("SELECT name,email,phone,location,customer_id FROM customers")
                rows = cur.fetchall()
            cnx.close()
            return render_template("view_customer.html", value=rows)
    else :
        return redirect(url_for('static', filename='403-forbidden-error.jpg'))

@app.route("/view_product")
def view_product():
    if 'user_id' in session:
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT name,barcode,price FROM products")
            rows = cur.fetchall()
        cnx.close()
        return render_template("view_product.html", value=rows)
    else:
        return redirect(url_for('static', filename='403-forbidden-error.jpg'))


@app.route("/edit_user/<user_id>", methods=["POST","GET"])
def edit_user(user_id):
    if 'user_id' in session:
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT name,user_name,email,phone_no,role,password FROM users where user_id = %s",user_id)
            rows = cur.fetchone()
        cnx.close()

        if request.method == 'POST':
            if (request.form["name"] == "" or request.form["username"] == "" or request.form["email"] == "" or request.form["phone"] == "" or request.form["password"] == "" or request.form["npassword"] == "" or request.form["cpassword"] == ""  or request.form["role"] == ""):
                flash("Enter all the fields")
                return redirect(url_for('edit_user',user_id=user_id))
            else:
                userDetails = request.form
                name = userDetails['name']
                username = userDetails['username']
                email = userDetails['email']
                phone = userDetails['phone']
                role = userDetails['role']
                password = userDetails['password']
                npassword = userDetails['npassword']
                cpassword = userDetails['cpassword']
                if (argon2.verify(password,rows[5])):
                    if npassword == cpassword:
                        xpassword = argon2.hash(npassword)
                        cnx = connect()
                        with cnx.cursor() as cur:
                            cur.execute("UPDATE users SET user_name = %s,name = %s,email = %s,phone_no = %s,role = %s,password = %s where user_id = %s",(username,name,email,phone,role,xpassword,user_id) )
                        cnx.commit()
                        cnx.close()
                        flash("Records updated")
                        return redirect(url_for("view_user"))
                    else:
                        flash("Both passwords must be same")
                        return redirect(url_for('edit_user',user_id=user_id))
                else:
                    flash("Current password is not verified")
                    return redirect(url_for('edit_user',user_id=user_id))
        else:
            return render_template("edit_user.html",value=rows, user_id=user_id)

    else:
        return redirect(url_for('static', filename='403-forbidden-error.jpg'))

@app.route("/edit_product/<product_id>", methods=["POST","GET"])
def edit_product(product_id):
    if 'user_id' in session:
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT name,barcode,price,product_id FROM products where product_id = %s",product_id)
            rows = cur.fetchone()
        cnx.close()

        if request.method == 'POST':

            if (request.form["pname"] == "" or request.form["bcode"] == "" or request.form["price"] == "" ):
                flash("Enter all the fields")
                return render_template("edit_product.html",value=rows ,product_id=product_id)

            else:
                userDetails = request.form
                pname = userDetails['pname']
                bcode = userDetails['bcode']
                price = userDetails['price']
                cnx = connect()
                with cnx.cursor() as cur:
                    cur.execute("UPDATE products SET name = %s,barcode = %s,price = %s where product_id = %s",(pname,bcode,price,product_id))
                cnx.commit()
                cnx.close()
                flash("Records Updated")
                return redirect(url_for('view_user'))

        else:
            return render_template("edit_product.html",value=rows ,product_id=product_id)
    else:
        return redirect(url_for('static', filename='403-forbidden-error.jpg'))

@app.route("/edit_customer/<customer_id>", methods=["POST","GET"])
def edit_customer(customer_id):
    if 'user_id' in session:
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT name,email,phone,location,customer_id FROM customers where customer_id = %s ",customer_id)
            row = cur.fetchone()
        cnx.close()
        if request.method == 'POST':

            if (request.form["name"] == "" or request.form["phone_no"] == "" or request.form["email"] == "" or request.form["location"] == ""):
                flash("Enter all the fields")
                return render_template("edit_customer.html",value=rows, customer_id=customer_id)
            else:
                userDetails = request.form
                name = userDetails['name']
                phone_no = userDetails['phone_no']
                email = userDetails['email']
                location = userDetails['location']
                cnx = connect()
                with cnx.cursor() as cur:
                    cur.execute("UPDATE customers SET name = %s,phone = %s,email = %s,location = %s where customer_id = %s",(name,phone_no,email,location,customer_id))
                cnx.commit()
                cnx.close()
                flash("Records updated")
                return redirect(url_for('view_customer'))

        else:
            return render_template("edit_customer.html",value=row, customer_id=customer_id)
    else:
        return redirect(url_for('static', filename='403-forbidden-error.jpg'))


@app.route("/logout")
def logout():
    if 'user_id' in session:
        session.pop('user_id',None)
        flash("You have been logged out")

    if 'role' in session:
        session.pop('role',None)

    return redirect(url_for('home'))


@app.route("/sales")
def sales():
    return render_template("sales.html")

if __name__ == "__main__":
    app.run(debug=True)
