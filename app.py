from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vikas",
    database="qus_data",
    autocommit=True
)
cursor = db.cursor()

@app.route("/")
def log():
    return render_template("index.html")

@app.route('/singin')
def singin():
    return render_template('singin.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        try:
            cursor.execute("INSERT INTO qus_data_table (name, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
            db.commit()
            session['email'] = email
            flash("Registration successful!", "success")
            return redirect(url_for('home'))
        except mysql.connector.IntegrityError:
            flash("Email already exists. Try another!", "danger")

    return render_template("singin.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':    
        email = request.form.get('email')
        password = request.form.get('password')

        cursor.execute("SELECT * FROM qus_data_table WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            stored_password = user[2]
            if check_password_hash(stored_password, password):
                session['email'] = email
                return redirect(url_for('home'))
            else:
                flash("Invalid password. Please try again.", "danger")
        else:
            flash("Email not found. Please register first.", "danger")

    return render_template("index.html")

@app.route("/home")
def home():
   return render_template('home.html')

@app.route('/root_login', methods=['GET', 'POST'])
def root_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if  email == '6391782926vs@gmail.com' and password == '9569':
            session['user'] = email 
            return redirect(url_for('root_home'))
        else:
            error = "Invalid username or password"
            return render_template('root-login.html', error=error)

    return render_template('root-login.html') 

@app.route('/root-home')
def root_home():
    return render_template('root-home.html')

@app.route("/logout")
def logout():
    session.pop('email', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('log'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)
