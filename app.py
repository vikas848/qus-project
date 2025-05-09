from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# DB (for login/register)
auth_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vikas",
    database="qus_data",
    autocommit=True
)
auth_cursor = auth_db.cursor()

# Question DB
qus_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vikas",
    database="qus_data",
    autocommit=True
)
qus_cursor = qus_db.cursor()

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
            auth_cursor.execute("INSERT INTO qus_data_table (name, email, password) VALUES (%s, %s, %s)",
                                (username, email, hashed_password))
            auth_db.commit()
            session['email'] = email
            flash("Registration successful!", "success")
            return redirect(url_for('home'))
        except mysql.connector.IntegrityError:
            flash("Email already exists.", "danger")

    return render_template("singin.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':    
        email = request.form.get('email')
        password = request.form.get('password')

        auth_cursor.execute("SELECT * FROM qus_data_table WHERE email = %s", (email,))
        user = auth_cursor.fetchone()

        if user:
            stored_password = user[2]
            if check_password_hash(stored_password, password):
                session['email'] = email
                return redirect(url_for('home'))
            else:
                flash("Invalid password.", "danger")
        else:
            flash("Email not found.", "danger")

    return render_template("index.html")

@app.route("/home")
def home():
   return render_template('home.html')

@app.route('/exam-type1.html', methods=['GET'])
def exam_type1_html():
    try:
        qus_cursor.execute("SELECT sr, Question, option1, option2, option3, option4 FROM save_qus_type1")
        questions = qus_cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Data load nahi ho paya. Error: {str(e)}", "danger")
        questions = []

    return render_template('exam-type1.html', questions=questions)

@app.route('/exam-type2.html', methods=['GET'])
def exam_type2_html():
    try:
        qus_cursor.execute("SELECT sr, Question, option1, option2, option3, option4 FROM save_qus_type2")
        questions = qus_cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Data load nahi ho paya. Error: {str(e)}", "danger")
        questions = []

    return render_template('exam-type2.html', questions=questions)

@app.route('/exam-type3.html', methods=['GET'])
def exam_type3_html():
    try:
        qus_cursor.execute("SELECT sr, Question, option1, option2, option3, option4 FROM save_qus_type3")
        questions = qus_cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Data load nahi ho paya. Error: {str(e)}", "danger")
        questions = []

    return render_template('exam-type3.html', questions=questions)

@app.route('/exam-type4.html', methods=['GET'])
def exam_type4_html():
    try:
        qus_cursor.execute("SELECT sr, Question, option1, option2, option3, option4 FROM save_qus_type4")
        questions = qus_cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Data load nahi ho paya. Error: {str(e)}", "danger")
        questions = []

    return render_template('exam-type4.html', questions=questions)

@app.route('/exam-type5.html', methods=['GET'])
def exam_type5_html():
    try:
        qus_cursor.execute("SELECT sr, Question, option1, option2, option3, option4 FROM save_qus_type5")
        questions = qus_cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Data load nahi ho paya. Error: {str(e)}", "danger")
        questions = []

    return render_template('exam-type5.html', questions=questions)

@app.route('/root_login', methods=['GET', 'POST'])
def root_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == '6391782926vs@gmail.com' and password == '9569':
            session['user'] = email 
            return redirect(url_for('root_home_html'))
        else:
            error = "Invalid username or password"
            return render_template('root-login.html', error=error)

    return render_template('root-login.html') 

@app.route('/root-home.html')
def root_home_html():
    return render_template('root-home.html')

@app.route('/type1.html')
def type1_html():
    return render_template('type1.html')

@app.route('/type1', methods=['POST'])
def type1():
    for i in range(10):
        question = request.form.get(f'question_{i}') or None
        option_a = request.form.get(f'option_a_{i}') or None
        option_b = request.form.get(f'option_b_{i}') or None
        option_c = request.form.get(f'option_c_{i}') or None
        option_d = request.form.get(f'option_d_{i}') or None
        correct_option = request.form.get(f'correct_option_{i}') or None

        try:
            qus_cursor.execute("""
                INSERT INTO save_qus_type1 (Question, option1, option2, option3, option4, Correct_Option)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (question, option_a, option_b, option_c, option_d, correct_option))
        except mysql.connector.Error as e:
            flash(f"Question {i+1} save nahi hua. Error: {str(e)}", "danger")

    qus_db.commit()
    flash("Questions save ho gaye!", "success")
    return redirect(url_for('type1_html'))

@app.route('/type1-edit.html', methods=['GET'])
def type1_edit_html():
    try:
        qus_cursor.execute("SELECT sr, Question, option1, option2, option3, option4, Correct_Option FROM save_qus_type1")
        questions = qus_cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Data load nahi ho paya. Error: {str(e)}", "danger")
        questions = []

    return render_template('type1-edit.html', questions=questions)

@app.route('/type1-update', methods=['POST'])
def type1_update():
    try:
        for i in range(10):
            sr = request.form.get(f'sr_{i}')
            question = request.form.get(f'question_{i}') or None
            option_a = request.form.get(f'option_a_{i}') or None
            option_b = request.form.get(f'option_b_{i}') or None
            option_c = request.form.get(f'option_c_{i}') or None
            option_d = request.form.get(f'option_d_{i}') or None
            correct_option = request.form.get(f'correct_option_{i}') or None

            if sr:
                qus_cursor.execute("""
                    UPDATE save_qus_type1
                    SET Question=%s, option1=%s, option2=%s, option3=%s, option4=%s, Correct_Option=%s
                    WHERE sr=%s
                """, (question, option_a, option_b, option_c, option_d, correct_option, sr))

        qus_db.commit()
        flash("Questions updated successfully!", "success")

    except mysql.connector.Error as e:
        flash(f"Error updating questions: {str(e)}", "danger")

    return redirect(url_for('type1_html'))  # or your correct redirect page



@app.route('/type2.html')
def type2_html():
    return render_template('type2.html')

@app.route('/type2', methods=['POST'])
def type2():
    for i in range(10):
        question = request.form.get(f'question_{i}') or None
        option_a = request.form.get(f'option_a_{i}') or None
        option_b = request.form.get(f'option_b_{i}') or None
        option_c = request.form.get(f'option_c_{i}') or None
        option_d = request.form.get(f'option_d_{i}') or None
        correct_option = request.form.get(f'correct_option_{i}') or None

        try:
            qus_cursor.execute("""
                INSERT INTO save_qus_type2 (Question, option1, option2, option3, option4, Correct_Option)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (question, option_a, option_b, option_c, option_d, correct_option))
        except mysql.connector.Error as e:
            flash(f"Question {i+1} save nahi hua. Error: {str(e)}", "danger")

    qus_db.commit()
    flash("Questions save ho gaye!", "success")
    return redirect(url_for('type2_html'))

@app.route('/type2-edit.html', methods=['GET'])
def type2_edit_html():
    try:
        qus_cursor.execute("SELECT sr, Question, option1, option2, option3, option4, Correct_Option FROM save_qus_type2")
        questions = qus_cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Data load nahi ho paya. Error: {str(e)}", "danger")
        questions = []

    return render_template('type2-edit.html', questions=questions)

@app.route('/type2-update', methods=['POST'])
def type2_update():
    try:
        for i in range(10):
            sr = request.form.get(f'sr_{i}')
            question = request.form.get(f'question_{i}') or None
            option_a = request.form.get(f'option_a_{i}') or None
            option_b = request.form.get(f'option_b_{i}') or None
            option_c = request.form.get(f'option_c_{i}') or None
            option_d = request.form.get(f'option_d_{i}') or None
            correct_option = request.form.get(f'correct_option_{i}') or None

            if sr:
                qus_cursor.execute("""
                    UPDATE save_qus_type2
                    SET Question=%s, option1=%s, option2=%s, option3=%s, option4=%s, Correct_Option=%s
                    WHERE sr=%s
                """, (question, option_a, option_b, option_c, option_d, correct_option, sr))

        qus_db.commit()
        flash("Questions updated successfully!", "success")

    except mysql.connector.Error as e:
        flash(f"Error updating questions: {str(e)}", "danger")

    return redirect(url_for('type2_html'))  # or your correct redirect page


@app.route('/type3.html')
def type3_html():
    return render_template('type3.html')

@app.route('/type3', methods=['POST'])
def type3():
    for i in range(10):
        question = request.form.get(f'question_{i}') or None
        option_a = request.form.get(f'option_a_{i}') or None
        option_b = request.form.get(f'option_b_{i}') or None
        option_c = request.form.get(f'option_c_{i}') or None
        option_d = request.form.get(f'option_d_{i}') or None
        correct_option = request.form.get(f'correct_option_{i}') or None

        try:
            qus_cursor.execute("""
                INSERT INTO save_qus_type3 (Question, option1, option2, option3, option4, Correct_Option)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (question, option_a, option_b, option_c, option_d, correct_option))
        except mysql.connector.Error as e:
            flash(f"Question {i+1} save nahi hua. Error: {str(e)}", "danger")

    qus_db.commit()
    flash("Questions save ho gaye!", "success")
    return redirect(url_for('type3_html'))

@app.route('/type3-edit.html', methods=['GET'])
def type3_edit_html():
    try:
        qus_cursor.execute("SELECT sr, Question, option1, option2, option3, option4, Correct_Option FROM save_qus_type3")
        questions = qus_cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Data load nahi ho paya. Error: {str(e)}", "danger")
        questions = []

    return render_template('type3-edit.html', questions=questions)

@app.route('/type3-update', methods=['POST'])
def type3_update():
    try:
        for i in range(10):
            sr = request.form.get(f'sr_{i}')
            question = request.form.get(f'question_{i}') or None
            option_a = request.form.get(f'option_a_{i}') or None
            option_b = request.form.get(f'option_b_{i}') or None
            option_c = request.form.get(f'option_c_{i}') or None
            option_d = request.form.get(f'option_d_{i}') or None
            correct_option = request.form.get(f'correct_option_{i}') or None

            if sr:
                qus_cursor.execute("""
                    UPDATE save_qus_type3
                    SET Question=%s, option1=%s, option2=%s, option3=%s, option4=%s, Correct_Option=%s
                    WHERE sr=%s
                """, (question, option_a, option_b, option_c, option_d, correct_option, sr))

        qus_db.commit()
        flash("Questions updated successfully!", "success")

    except mysql.connector.Error as e:
        flash(f"Error updating questions: {str(e)}", "danger")

    return redirect(url_for('type3_html'))

@app.route('/type4.html')
def type4_html():
    return render_template('type4.html')

@app.route('/type4', methods=['POST'])
def type4():
    for i in range(10):
        question = request.form.get(f'question_{i}') or None
        option_a = request.form.get(f'option_a_{i}') or None
        option_b = request.form.get(f'option_b_{i}') or None
        option_c = request.form.get(f'option_c_{i}') or None
        option_d = request.form.get(f'option_d_{i}') or None
        correct_option = request.form.get(f'correct_option_{i}') or None

        try:
            qus_cursor.execute("""
                INSERT INTO save_qus_type4 (Question, option1, option2, option3, option4, Correct_Option)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (question, option_a, option_b, option_c, option_d, correct_option))
        except mysql.connector.Error as e:
            flash(f"Question {i+1} save nahi hua. Error: {str(e)}", "danger")

    qus_db.commit()
    flash("Questions save ho gaye!", "success")
    return redirect(url_for('type4_html'))

@app.route('/type4-edit.html', methods=['GET'])
def type4_edit_html():
    try:
        qus_cursor.execute("SELECT sr, Question, option1, option2, option3, option4, Correct_Option FROM save_qus_type4")
        questions = qus_cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Data load nahi ho paya. Error: {str(e)}", "danger")
        questions = []

    return render_template('type4-edit.html', questions=questions)

@app.route('/type4-update', methods=['POST'])
def type4_update():
    try:
        for i in range(10):
            sr = request.form.get(f'sr_{i}')
            question = request.form.get(f'question_{i}') or None
            option_a = request.form.get(f'option_a_{i}') or None
            option_b = request.form.get(f'option_b_{i}') or None
            option_c = request.form.get(f'option_c_{i}') or None
            option_d = request.form.get(f'option_d_{i}') or None
            correct_option = request.form.get(f'correct_option_{i}') or None

            if sr:
                qus_cursor.execute("""
                    UPDATE save_qus_type4
                    SET Question=%s, option1=%s, option2=%s, option3=%s, option4=%s, Correct_Option=%s
                    WHERE sr=%s
                """, (question, option_a, option_b, option_c, option_d, correct_option, sr))

        qus_db.commit()
        flash("Questions updated successfully!", "success")

    except mysql.connector.Error as e:
        flash(f"Error updating questions: {str(e)}", "danger")

    return redirect(url_for('type4_html'))

@app.route('/type5.html')
def type5_html():
    return render_template('type5.html')

@app.route('/type5', methods=['POST'])
def type5():
    for i in range(10):
        question = request.form.get(f'question_{i}') or None
        option_a = request.form.get(f'option_a_{i}') or None
        option_b = request.form.get(f'option_b_{i}') or None
        option_c = request.form.get(f'option_c_{i}') or None
        option_d = request.form.get(f'option_d_{i}') or None
        correct_option = request.form.get(f'correct_option_{i}') or None

        try:
            qus_cursor.execute("""
                INSERT INTO save_qus_type5 (Question, option1, option2, option3, option4, Correct_Option)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (question, option_a, option_b, option_c, option_d, correct_option))
        except mysql.connector.Error as e:
            flash(f"Question {i+1} save nahi hua. Error: {str(e)}", "danger")

    qus_db.commit()
    flash("Questions save ho gaye!", "success")
    return redirect(url_for('type5_html'))

@app.route('/type5-edit.html', methods=['GET'])
def type5_edit_html():
    try:
        qus_cursor.execute("SELECT sr, Question, option1, option2, option3, option4, Correct_Option FROM save_qus_type5")
        questions = qus_cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Data load nahi ho paya. Error: {str(e)}", "danger")
        questions = []

    return render_template('type5-edit.html', questions=questions)

@app.route('/type5-update', methods=['POST'])
def type5_update():
    try:
        for i in range(10):
            sr = request.form.get(f'sr_{i}')
            question = request.form.get(f'question_{i}') or None
            option_a = request.form.get(f'option_a_{i}') or None
            option_b = request.form.get(f'option_b_{i}') or None
            option_c = request.form.get(f'option_c_{i}') or None
            option_d = request.form.get(f'option_d_{i}') or None
            correct_option = request.form.get(f'correct_option_{i}') or None

            if sr:
                qus_cursor.execute("""
                    UPDATE save_qus_type5
                    SET Question=%s, option1=%s, option2=%s, option3=%s, option4=%s, Correct_Option=%s
                    WHERE sr=%s
                """, (question, option_a, option_b, option_c, option_d, correct_option, sr))

        qus_db.commit()
        flash("Questions updated successfully!", "success")

    except mysql.connector.Error as e:
        flash(f"Error updating questions: {str(e)}", "danger")

    return redirect(url_for('type5_html'))

@app.route("/logout")
def logout():
    session.pop('email', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('log'))

if __name__ == '__main__':
    app.run(debug=True, port=5005)