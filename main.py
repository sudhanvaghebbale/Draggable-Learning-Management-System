from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import text
from functools import wraps
import random
import datetime
import json

app = Flask(__name__)

# Change the credentials to fit your localhost details.
_engine = create_engine("mysql+pymysql://root:Sudhanva@localhost/LoginRegister")
db = scoped_session(sessionmaker(bind=_engine))

# Secret Key for secure transaction!
app.config['SECRET_KEY'] = 'SER@515@Findler'


# Home Page route
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# Register Page Route
@app.route("/register", methods=["GET", "POST"])
def register():
    # Get elements from the database
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpass = request.form.get("confirmPassword")
        role = request.form.get("rolePicker")
        status = "0"
        # If both the passwords match, then register
        if password == confirmpass:
            _engine.execute("INSERT INTO Users VALUES (%s, %s, %s, %s, %s)", [name, email, password, role, status])
            db.commit()
            flash("Successfully Registered!", "success")
            return render_template("login.html")
        else:
            flash("Passwords do not match!", "danger")
            return render_template('register.html')

    return render_template('register.html')


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get elements from the database
        # Get elements from the database
        email = request.form.get("email")
        session['email'] = request.form.get("email")
        password = request.form.get("password")

        EmailID = _engine.execute("SELECT Email FROM Users WHERE Email = %s", [email]).fetchone()
        em = ''.join(EmailID)
        '''
        emailsql = "SELECT email FROM Users WHERE email = '" + email + "'"
        EmailID = _engine.execute(emailsql).fetchone()
        em = ''.join(EmailID)
        '''

        passwordsql = "SELECT password FROM Users WHERE email = '" + email + "'"
        Passwords = _engine.execute(passwordsql).fetchone()
        Password = ''.join(Passwords)

        roles = _engine.execute("SELECT Role FROM Users WHERE Email = %s", [email]).fetchone()
        role = ''.join(roles)

        statuses = _engine.execute("SELECT Status FROM Users WHERE Email = %s", [email]).fetchone()
        status = str(statuses)

        if em is None:
            flash("User does not exist!", "danger")
            return redirect(url_for("login"))

        # If both the fields match, then register
        if password == Password:
            name = _engine.execute("SELECT Name FROM Users WHERE Email = %s", [em]).fetchone()
            # If admin
            if "Admin" in role and "1" in status:
                session['logged in'] = em
                for row in name:
                    flash("Welcome Back,  " + str(row), "success")
                return redirect(url_for("admin"))

            # If teacher
            if "Teacher" in role and "1" in status:
                session['logged in'] = em
                for row in name:
                    flash("Welcome Back,  " + str(row), "success")
                return redirect(url_for("teacher"))

            # IF Student
            if "Student" in role and "1" in status:
                session['logged in'] = em
                for row in name:
                    flash("Welcome Back,  " + str(row), "success")
                return redirect(url_for("student"))

            # If Neither
            elif "0" in status:
                for row in name:
                    flash(str(row) + ", " + " \n Your account is currently restricted. Contact admin for more information! ", "warning")
                return redirect(url_for("free"))
        else:
            flash("Password is incorrect!", "danger")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


# Admin Console Route
@app.route("/adminconsole", methods=["GET", "POST"])
def adminconsole():
    data1 = _engine.execute("SELECT * FROM Users WHERE status = '1'").fetchall()
    data2 = _engine.execute("SELECT * FROM Users WHERE status = '0'").fetchall()
    return render_template("users.html", acceptedusers=data1, reviewusers=data2)


# Update the status of a user
@app.route("/update/<string:email>", methods=["GET", "POST"])
def update(email):
    _engine.execute("UPDATE Users SET status = '1' WHERE email = %s", [email])
    db.commit()
    flash("User added successfully", "success")
    return redirect(url_for("adminconsole"))


# Delete a particular user
@app.route("/delete/<string:email>", methods=["GET", "POST"])
def delete(email):
    _engine.execute("DELETE FROM Users WHERE email = %s", [email])
    db.commit()
    flash("User deleted successfully", "danger")
    return redirect(url_for("adminconsole"))


# Admin Route
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if 'logged in' in session:
        email = session['email']
        name = _engine.execute("SELECT Name FROM Users WHERE Email = %s", [email]).fetchone()
        return render_template("admin.html", user=name)
    else:
        return render_template('login.html')


# Teacher Route
@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if 'logged in' in session:
        email = session['email']
        name = _engine.execute("SELECT Name FROM Users WHERE Email = %s", [email]).fetchone()
        return render_template("teacher.html", user=name)
    else:
        return render_template('login.html')


# Student Route
@app.route("/student", methods=["GET", "POST"])
def student():
    if 'logged in' in session:
        email = session['email']
        name = _engine.execute("SELECT Name FROM Users WHERE Email = %s", [email]).fetchone()
        return render_template("student_landing.html", user=name)
    else:
        return render_template('login.html')


# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Playground
@app.route("/playground")
def playground():
    if 'logged in' in session:
        email = session['email']
        roles = _engine.execute("SELECT Role FROM Users WHERE Email = %s", [email]).fetchone()
        role = ''.join(roles)
        # If Elementary Student, else Load Middle School Playground
        if "1-2" in role:
            return render_template('Playground - Class 1-2.html')
        elif "3-4" in role:
            return render_template('Playground - Class 3-4.html')
        elif "5-8" in role:
            return render_template('Playground - Class 5-8.html')
        else:
            return render_template('Playground - Class 9-12.html')
    else:
        return render_template('login.html')


# Take Quiz Route
@app.route("/takeQuiz")
def takeQuiz():
    if 'logged in' in session:
        return render_template('takeQuiz.html')
    else:
        return render_template('login.html')


# Review Grades Route
@app.route("/reviewGrades")
def reviewGrades():
    if 'logged in' in session:
        email = session['email']
        name = _engine.execute("SELECT Name FROM Users WHERE Email = %s", [email]).fetchone()
        grade = _engine.execute("SELECT * FROM Grades WHERE Email = %s", [email]).fetchall()
        return render_template('reviewGrades.html', grades=grade, user=name)
    else:
        return render_template('login.html')


# Create Quiz Route
@app.route("/createQuiz", methods=["GET", "POST"])
def createQuiz():
    if 'logged in' in session:
        name = request.form.get("Names")
        description = request.form.get("Descriptions")
        Roles = request.form.get("rolePicker")
        email = session['email']
        session['level'] = Roles
        session['QuizName'] = name
        Instructors = _engine.execute("SELECT Name FROM Users WHERE Email = %s", [email]).fetchone()
        instructor = ''.join(Instructors)
        status = "0"
        names = _engine.execute("SELECT Name FROM Quiz WHERE Name = %s", [name]).fetchone()
        if names is None:
            _engine.execute("INSERT INTO Quiz VALUES (%s, %s, %s, %s, %s)", [name, instructor, Roles, description, status])
            db.commit()
            return render_template('createQuiz.html')
        else:
            flash("Quiz already exists!", "danger")
            return redirect(url_for("teacher"))
    else:
        return render_template('login.html')


# Submit Questions and Answers
@app.route("/createQuestion", methods=["GET", "POST"])
def createQuestion():
    levels = session['level']
    quizName = session['QuizName']
    i = 1
    while True:
        QID = "Q" + str(i)
        question = request.form.get("Q" + str(i))
        AID = "A" + str(i)
        answer = request.form.get("A" + str(i))
        if question is None:
            break
        _engine.execute("INSERT INTO Questions VALUES (%s, %s, %s, %s)", [QID, question, levels, quizName])
        db.commit()
        _engine.execute("INSERT INTO Answer VALUES (%s, %s, %s, %s)", [AID, answer, quizName, QID])
        db.commit()
        i += 1

    flash("Quiz added successfully!", "success")
    return redirect(url_for("teacher"))
    '''
	for i in 
		question = request.form.get("Q" + i)
		answer = request.form.get("A" + i)
	'''


# Grade Quiz Route
@app.route("/showQuizzes")
def showQuizzes():
    if 'logged in' in session:
        email = session['email']
        roles = _engine.execute("SELECT Role FROM Users WHERE Email = %s", [email]).fetchone()
        role = ''.join(roles)
        quizzes1 = _engine.execute("SELECT Name, Instructor, Description FROM Quiz WHERE Quiz_Level = %s AND Status = '0'", [role]).fetchall()
        quizzes2 = _engine.execute("SELECT Name, Instructor, Description FROM Quiz WHERE Quiz_Level = %s AND Status = '1'", [role]).fetchall()
        return render_template('viewQuizzes.html', quizzes1 =quizzes1, quizzes2 =quizzes2)
    else:
        return render_template('login.html')


# load quiz route
@app.route("/loadQuiz")
def loadQuiz():
    if 'logged in' in session:
        return render_template('takeQuiz.html')
    else:
        return render_template('login.html')


@app.route('/getQuestions')
def getQuestions():
    if 'logged in' in session:
        quizname = request.args.get('quizname')
        session['quizName'] = quizname
        questions = _engine.execute("SELECT ID, Question FROM questions WHERE Quiz_Name = %s", [quizname]).fetchall()
        resp = []
        for i in range(0, len(questions)):
            resp.append({
                'id': questions[i][0],
                'question': questions[i][1]
            })
        return json.dumps(resp), 200
    else:
        return json.dumps({'err': 'Not logged in'}), 401


@app.route('/checkAnswers')
def checkAnswers():
    if 'logged in' in session:
        questionName = request.args.get('questionName')
        quizName = request.args.get('quizName')
        answer = request.args.get('ans')
        questions = _engine.execute("SELECT choice from answer WHERE Quiz_Name = %s AND Question_ID = %s",
                                    [quizName, questionName]).fetchall()
        if questions[0][0] == answer:
            return 'answer correct', 200
        else:
            return 'answer incorrect', 500


@app.route("/playground_free")
def playground_free():
    email = session['email']
    roles = _engine.execute("SELECT Role FROM Users WHERE Email = %s", [email]).fetchone()
    role = ''.join(roles)
    if "1-2" in role:
        return render_template('Playground - Class 1-2.html')
    elif "3-4" in role:
        return render_template('Playground - Class 3-4.html')
    elif "5-8" in role:
        return render_template('Playground - Class 5-8.html')
    else:
        return render_template('Playground - Class 9-12.html')


@app.route("/free")
def free():
    return render_template("student_free.html")


@app.route("/free_playground")
def free_playground():
    return render_template('Playground - Class 1-2.html')


@app.route("/postResult", methods=["POST"])
def postResult():
    score = request.args.get('marks')
    email = session['email']
    quizNames = session['quizName']
    instructor = _engine.execute("SELECT Instructor from Quiz WHERE Name = %s", [quizNames]).fetchone()
    instructors = ''.join(instructor)
    now = str(datetime.datetime.now())
    quizzes = _engine.execute("SELECT Quiz_Name from Grades WHERE Quiz_Name = %s", [quizNames]).fetchone()

    if quizzes is None:
        _engine.execute("INSERT INTO Grades VALUES (%s, %s, %s, %s, %s)", [quizNames, email, score, instructors, now])
        db.commit()
    else:
        _engine.execute("UPDATE Grades SET Score = %s, Last_Taken = %s WHERE Name = %s", [score, now, quizzes])
        db.commit()

    _engine.execute("UPDATE Quiz SET Status = '1' WHERE Name = %s", [quizNames])
    db.commit()
    return "Updated the database"

# Run Main in Debug mode
if __name__ == '__main__':
    app.debug = True
    app.run()
