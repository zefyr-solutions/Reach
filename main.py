from flask import Flask, redirect, render_template, session, flash, url_for, request, make_response, send_from_directory, json, jsonify
from passlib.hash import argon2
from db import connect
import yaml
import os
import pymysql
from werkzeug.utils import secure_filename
import datetime
# Imported all required files
cwd = os.getcwd()
UPLOAD_FOLDER = cwd +'/uploads/product_pic/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "hello"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Creating the login page
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST" :
        #If no input, redirect back
        if ((request.form["user_name"] == "") or (request.form["password"] == "")):
            flash("Enter Credentials!")
            session['alertFlash'] = "bg-red-400 text-red-900"
            return redirect(url_for("home"))

        user_name = request.form["user_name"]
        password = request.form["password"]

        #Checking with database for username and password
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT user_id,password,role,user_name FROM users where user_name = %s ",[user_name])
            row = cur.fetchone()
        cnx.close()
        #If username is found on database,
        if row:
            #Checking password is correct or not
            if (argon2.verify(password,row[1])):
                session["user_id"] = row[0]
                session["role"] = row[2]
                session["user_name"] = row[3]
                flash("Login Succesful")
                session['alertFlash'] = "bg-green-400 text-green-900"
                return redirect(url_for("driver"))
            else:
                flash("Login Failed")
                session['alertFlash'] = "bg-red-400 text-red-900"
                return redirect(url_for("home"))
        else:
            flash("Could not find user")
            session['alertFlash'] = "bg-red-400 text-red-900"
            return redirect(url_for("home"))
    else:
        return render_template("index.html")
# Creating Add user page
@app.route("/add_user", methods=["POST","GET"])
def add_user():
    if 'user_id' in session: # Checking if user is logged in or not
        if request.method == 'POST':

            if (request.form["name"] == "" or request.form["username"] == "" or request.form["email"] == "" or request.form["phone"] == "" or request.form["password"] == "" or request.form["cpassword"] == ""  or request.form["role"] == ""):
                # If user misses any fields
                flash("Enter all the fields")
                return render_template("add_user.html")
            else:
                # Inserting the data into database
                userDetails = request.form
                name = userDetails['name']
                username = userDetails['username']
                email = userDetails['email']
                phone = userDetails['phone']
                role = userDetails['role']
                password = userDetails['password']
                cpassword = userDetails['cpassword']
                cnx = connect()
                # Checking if user exists
                with cnx.cursor() as cur:
                    cur.execute("SELECT user_name FROM users")
                    usr = cur.fetchall()
                cnx.close()
                for u in usr :
                    if u[0] == username:
                        flash("User already exists")
                        return redirect(url_for("add_user"))
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
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))
# Creating the Add product page
@app.route("/add_product", methods=["POST","GET"])
def add_product():
    if 'user_id' in session: # Checking if user is logged in or not
        if request.method == 'POST':

            if (request.form["pname"] == "" or request.form["bcode"] == "" or request.form["price"] == "" ):
                # Checking if all the fields are entered
                flash("Enter all the fields")
                return redirect(url_for("add_product"))
            else:
                # Inserting data into database
                userDetails = request.form
                pname = userDetails['pname']
                bcode = userDetails['bcode']
                price = userDetails['price']
                # check if the post request has the file part
                if 'product_pic' not in request.files:
                    flash('No file part')
                    return redirect(url_for("add_product"))
                file = request.files['product_pic']
                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return redirect(url_for("add_product"))
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    ct = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
                    uid = str(session['user_id'])
                    fname = ct + uid + filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
                cnx = connect()
                with cnx.cursor() as cur:
                    cur.execute("INSERT INTO products(name,barcode,price,product_pic) VALUES(%s,%s,%s,%s)",(pname,bcode,price,fname))
                    cnx.commit()
                    cnx.close()
                flash("Records inserted")
                return redirect(url_for("view_product"))

        else:
            return render_template("add_product.html")
    else:
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))
# Creating Add Customer page
@app.route("/add_customer", methods=["POST","GET"])
def add_customer():
    if 'user_id' in session:  # Checking if user is logged in or not
        if request.method == 'POST':

            if (request.form["name"] == "" or request.form["phone_no"] == "" or request.form["email"] == "" or request.form["location"] == ""):
                flash("Enter all the fields")
                return redirect(url_for("add_customer"))
                # Checking if all the fields are entered
            else:
                # Inserting data into database
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
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))

@app.route("/driver")
def driver():
    if 'user_id' in session: # Checking if user is logged in or not
        return render_template("driver.html")
    else :
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))

# Creating view user page
@app.route("/view_user", methods=["POST","GET"])
def view_user():
    if 'user_id' in session:  # Checking if user is logged in or not
        if request.method == "POST" :
            # Delete user function
            userDetails = request.form
            password = userDetails['password']
            dltuser = userDetails['dltuser']
            cnx = connect()
            # Password Checking
            with cnx.cursor() as cur:
                cur.execute("SELECT password FROM users where user_id = %s ",session['user_id'])
                row = cur.fetchone()
            cnx.close()
            if (argon2.verify(password,row[0])):
                cnx = connect()
                with cnx.cursor() as cur:
                    cur.execute("DELETE FROM users WHERE user_id =%s",dltuser)
                    cnx.commit()
                    cnx.close()

                flash("Row Deletion Succesful")
                return redirect(url_for("view_user"))
            else :
                flash("Please enter the Correct Password ")
                return redirect(url_for("view_user"))
        # Returning data of specific user
        if request.args.get("user_id") :
            user_id = request.args.get("user_id")
            cnx = connect()
            with cnx.cursor() as cur:
                cur.execute("SELECT user_name,name,email,phone_no,role,user_id FROM users where user_id = %s ",[user_id])
                row = cur.fetchone()
            return render_template("view_user_specific.html")
        # Returning data of all users
        else :
            cnx = connect()
            with cnx.cursor() as cur:
                cur.execute("SELECT user_name,name,email,phone_no,role,user_id FROM users")
                rows = cur.fetchall()
            cnx.close()
            return render_template("view_user.html", value=rows)
    else:
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))
# Creating view customer page
@app.route("/view_customer", methods=["POST","GET"])
def view_customer():
    if 'user_id' in session:  # Checking if user is logged in or not
        if request.method == "POST" :
            # Delete customer function
            userDetails = request.form
            password = userDetails['password']
            dltcustomer = userDetails['dltcustomer']
            cnx = connect()
            # Password Checking
            with cnx.cursor() as cur:
                cur.execute("SELECT password FROM users where user_id = %s ",session['user_id'])
                row = cur.fetchone()
            cnx.close()
            if (argon2.verify(password,row[0])):
                cnx = connect()
                with cnx.cursor() as cur:
                    cur.execute("DELETE FROM customers WHERE customer_id =%s",dltcustomer)
                    cnx.commit()
                    cnx.close()

                flash("Row Deletion Succesful")
                return redirect(url_for("view_customer"))
            else :
                flash("Please enter the Correct Password ")
                return redirect(url_for("view_customer"))
        # Returning data of specific customer
        if request.args.get("customer_id") :
            customer_id = request.args.get("customer_id")
            cnx = connect()
            with cnx.cursor() as cur:
                cur.execute("SELECT name,email,phone,location,customer_id FROM customers where customer_id = %s ",[customer_id])
                row = cur.fetchone()
            cnx.close()
            return render_template("view_customer_specific.html", row=row)
        # Returning Data of all Customers
        else :
            cnx = connect()
            with cnx.cursor() as cur:
                cur.execute("SELECT name,email,phone,location,customer_id FROM customers")
                rows = cur.fetchall()
            cnx.close()
            return render_template("view_customer.html", value=rows)
    else :
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))

# Creating view product page
@app.route("/view_product", methods=["POST","GET"])
def view_product():
    if 'user_id' in session:  # Checking if user is logged in or not
        if request.method == "POST" :
            # Delete product Function
            userDetails = request.form
            password = userDetails['password']
            dltproduct = userDetails['dltproduct']
            cnx = connect()
            # Password Checking
            with cnx.cursor() as cur:
                cur.execute("SELECT password FROM users where user_id = %s ",session['user_id'])
                row = cur.fetchone()
            cnx.close()
            if (argon2.verify(password,row[0])):
                cnx = connect()
                with cnx.cursor() as cur:
                    cur.execute("DELETE FROM products WHERE product_id =%s",dltproduct)
                    cnx.commit()
                    cnx.close()

                flash("Row Deletion Succesful")
                return redirect(url_for("view_product"))
            else :
                flash("Please enter the Correct Password ")
                return redirect(url_for("view_product"))
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT name,barcode,price,product_id FROM products")
            rows = cur.fetchall()
        cnx.close()
        return render_template("view_product.html", value=rows)
    else:
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))

# Creating Edit user page
@app.route("/edit_user/<user_id>", methods=["POST","GET"])
def edit_user(user_id):
    if 'user_id' in session:   # Checking if user is logged in or not
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT name,user_name,email,phone_no,role,password FROM users where user_id = %s",user_id)
            rows = cur.fetchone()
        cnx.close()

        if request.method == 'POST':
            if (request.form["name"] == "" or request.form["username"] == "" or request.form["email"] == "" or request.form["phone"] == "" or request.form["password"] == "" or request.form["npassword"] == "" or request.form["cpassword"] == ""  or request.form["role"] == ""):
                flash("Enter all the fields")
                return redirect(url_for('edit_user',user_id=user_id))
                # Checking if all the fields are entered
            else:
                # Inserting data into database
                userDetails = request.form
                name = userDetails['name']
                username = userDetails['username']
                email = userDetails['email']
                phone = userDetails['phone']
                role = userDetails['role']
                password = userDetails['password']
                npassword = userDetails['npassword']
                cpassword = userDetails['cpassword']
                cnx = connect()
                # Checking if username exists
                with cnx.cursor() as cur:
                    cur.execute("SELECT user_name FROM users")
                    usr = cur.fetchall()
                cnx.close()
                for u in usr :
                    if u[0] == username:
                        flash("User already exists")
                        return redirect(url_for("view_user"))
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
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))
# Creating edit product page
@app.route("/edit_product/<product_id>", methods=["POST","GET"])
def edit_product(product_id):
    if 'user_id' in session:  # Checking if user is logged in or not
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT name,barcode,price,product_id FROM products where product_id = %s",product_id)
            rows = cur.fetchone()
        cnx.close()

        if request.method == 'POST':

            if (request.form["pname"] == "" or request.form["bcode"] == "" or request.form["price"] == "" ):
                flash("Enter all the fields")
                return render_template("edit_product.html",value=rows ,product_id=product_id)
                # Checking if all the fields are entered

            else:
                # Inserting data into database
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
                return redirect(url_for('view_product'))

        else:
            return render_template("edit_product.html",value=rows ,product_id=product_id)
    else:
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))

# Creating edit customer page
@app.route("/edit_customer/<customer_id>", methods=["POST","GET"])
def edit_customer(customer_id):
    if 'user_id' in session:  # Checking if user is logged in or not
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT name,email,phone,location,customer_id FROM customers where customer_id = %s ",customer_id)
            row = cur.fetchone()
        cnx.close()
        if request.method == 'POST':

            if (request.form["name"] == "" or request.form["phone_no"] == "" or request.form["email"] == "" or request.form["location"] == ""):
                flash("Enter all the fields")
                return render_template("edit_customer.html", value=rows, customer_id=customer_id)
                # Checking if all the fields are entered
            else:
                # Inserting data into database
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
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))

# Creating logout function
@app.route("/logout")
def logout():
    if 'user_id' in session: # Checking if user is logged in or not
        session.pop('user_id',None)
        flash("You have been logged out")
        session["alertFlash"] = "bg-red-400 text-red-900"

    if 'role' in session:
        session.pop('role',None)

    return redirect(url_for('home'))

# Creating sales page
@app.route("/sales",methods=["POST","GET"])
def sales():
    # Checking if user is logged in or not
    if 'user_id' in session:
        if request.method == 'POST':

            if (request.form["customer_name"] == "" or request.form["product_name"] == "" or request.form["qty"] == ""):
                flash("Enter all the fields")
                return redirect(url_for("add_customer"))
            else:
                # Insering data into database
                cnx = connect()
                with cnx.cursor() as cur:
                    # To get customer id from database using customer name provided by user
                    cur.execute("SELECT customer_id FROM customers WHERE name = %s", request.form['customer_name'])
                    customer_id = cur.fetchone()[0]
                    # To get product id from database using product name provided by user
                    cur.execute("SELECT product_id FROM products WHERE name = %s", request.form['product_name'])
                    product_id = cur.fetchone()[0]
                    # Inserting data to database
                    cur.execute('''INSERT INTO sales (customer_id, product_id, user_id, quantity) VALUES (%s,%s,%s,%s)
                                            ''', (customer_id, product_id, session["user_id"], request.form['qty']))
                    cnx.commit()
                    cnx.close()
                flash("Records inserted")
                return redirect(url_for("/driver"))

        return render_template("sales.html")
    else :
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))

# Creating profile page
@app.route("/profile", methods=["POST","GET"])
def profile():
    if 'user_id' in session: #Checking id user is logged in or not
        cnx = connect()
        with cnx.cursor() as cur:
            cur.execute("SELECT user_name,name,email,phone_no,role FROM users WHERE user_id = %s", session['user_id'])
            rows = cur.fetchone()
        cnx.close()
        return render_template("profile.html",value = rows)
    else:
        return redirect(url_for('static', filename='images/403-forbidden-error.jpg'))

# Creating service worker initiation page
@app.route("/service-worker.js")
def sw():
    return app.send_static_file('service-worker.js')


# Route to return data to autocomplete (Availabilty of username)
@app.route("/username_check", methods=["POST","GET"])
def username_check() :
    search_term = request.form['username']
    cnx = connect()
    with cnx.cursor() as cur:
        cur.execute("SELECT user_name FROM users WHERE user_name LIKE %s ",(search_term))
        rows = cur.fetchall()
    cnx.close()
    if rows :
        return "username not available"
    else :
        return "available"


# This route is used for testing new features
@app.route("/test", methods=["POST","GET"])
def test() :
    return render_template("autocomplete_test.html")


# Route to return data required for autocompletion of customer name
@app.route("/autocomplete_customer_name", methods=["POST","GET"])
def autocomplete_customer_name () :
    search_term = request.args.get("term")
    print("search = ", search_term)
    cnx = connect()
    with cnx.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(f"SELECT name AS label FROM customers WHERE name LIKE '%{search_term}%' " )
        rows = cur.fetchall()
    cnx.close()
    return jsonify(rows)

@app.route("/report")
def report() :
    return render_template("report.html")

if __name__ == "__main__":
    app.run(debug=True)
