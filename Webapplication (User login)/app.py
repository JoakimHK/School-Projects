import json
import re
from flask import Flask, render_template, redirect, url_for, request, flash, session
import os.path
import bcrypt

PASSWORDFILE = 'passwords.json'
PASSWORDFILEDELIMITER = ":"

app = Flask(__name__)
# The secret key here is required to maintain sessions in flask 
app.secret_key = b'8852475abf1dcc3c2769f54d0ad64a8b7d9c3a8aa8f35ac4eb7454473a5e454c'

# Initialize Database file if not exists.
if not os.path.exists(PASSWORDFILE):
    open(PASSWORDFILE, 'w').close()


@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('loggedin.html', username = username)

    # TODO: Check if user is logged in
    # if user is logged in
    #    return render_template('loggedin.html')

    return render_template('home.html')


# Display register form
@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

# Handle registration data
@app.route('/register', methods=['POST'])
def register_post():
    username = request.form["username"]
    password = request.form["password"]
    matchpass = request.form["matchpassword"]
    
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    
    if password == matchpass:
        
        pat = re.compile(reg)                 
        mat = re.search(pat, password)
        # validating conditions
        if mat:
            salt = bcrypt.gensalt()
            hash_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
                    
            json_data = {"username": username, "password": hash_pass.decode('utf-8')}
            
            with open(PASSWORDFILE, "r") as f:
                data = json.load(f)
                data["users"].append(json_data)
            with open(PASSWORDFILE, "w") as f:
                json.dump(data, f, indent=2)
            return redirect("/login")
        else:
            return render_template('register.html', error='Password does not meet the requirements')
    else:
        return render_template('register.html', error='Password does not match')
            

# Display login form
@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


# Handle login credentials
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    
    with open(PASSWORDFILE, "r") as f:
        data = json.load(f)
        users = data["users"]
        i = 0

        for key in users:
            name, passw = key["username"], key["password"]

            if name == username:
                if bcrypt.checkpw(password.encode('utf-8'), passw.encode('utf-8')):
                    session['username'] = name
                    return redirect("/")
            i += 1
        return render_template("login.html", error="User does not exist or incorrect password")
    


if __name__ == '__main__':

    # TODO: Add TSL
    app.run(debug=True)
    
    #Used when running on the server for establishing a https connection
    #app.run(debug=True, ssl_context=('/../fullchain.pem', '/.../privkey.pem'))
