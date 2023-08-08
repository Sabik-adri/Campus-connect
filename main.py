from flask import Flask, request, redirect, render_template, session, url_for
import pymongo
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded files
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
users_table = mydb["student_info"]
students_table = mydb["students"]
teacher_table = mydb["teachers"]
teacher_list = mydb["teachers_list"]
course_list_db = mydb["course_list"]
sheet_list = mydb["sheet_list"]

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        form_data = dict(request.form)
        form_username = form_data["username"]
        form_password = form_data["password"]
        db_user = users_table.find_one({"username": form_username})
        if db_user is None:
            return "Username not found"
        if form_password != db_user["password"]:
            return "Password did not match"
        session["logged_in"] = True
        session["username"] = form_username
        return redirect("/dashboard")  # Redirect to the dashboard after successful login
    if "logged_in" in session:
        return redirect("/dashboard")  # If already logged in, redirect to the dashboard
    return render_template("login.html")

@app.route('/')
def logout():
    session.clear()  # Clear the session
    return redirect('/login')  # Redirect to the login page

@app.route('/dashboard')
def dashboard():
    if "logged_in" in session:
        return render_template("dashboard.html")
    return redirect('/login')  # Redirect to the login page if not logged in






@app.route('/')
def add():
    return render_template('addStudent.html')

@app.route('/addStudent', methods=['GET', 'POST'])
def add_student():
    if request.method == "POST":
        form_data = dict(request.form)
        students_table.insert_one(form_data)
        return redirect(url_for('student'))
    return render_template('addStudent.html')


@app.route('/student')
def student():
    student_data = list(students_table.find({}, {"_id": 0, "name": 1, "parent": 1, "course": 1, "section": 1, "id": 1, "birthdate": 1, "gender": 1, "address": 1, "phone": 1, "email": 1}))
    return render_template('student.html', student_data=student_data)

@app.route('/')
def add9():
    return render_template('addCourse.html')

@app.route('/addCourse', methods=['GET', 'POST'])
def add_course():
    if request.method == "POST":
        form_data = dict(request.form)
        course_list_db.insert_one(form_data)
        return redirect(url_for('courses'))
    return render_template('addCourse.html')

@app.route('/courses')
def courses():
    course_data = list(course_list_db.find({}, {"_id": 0, "name": 1, "id": 1, "section": 1, "faculty": 1, "tslot": 1, "pre": 1}))
    return render_template('courses.html', course_data=course_data)

@app.route('/')
def add10():
    return render_template('addSheet.html')

@app.route('/addSheet', methods=['GET', 'POST'])
def add_sheet():
    if request.method == "POST":
        form_data = dict(request.form)
        sheet_list.insert_one(form_data)
        return redirect(url_for('sheet_info'))
    return render_template('addSheet.html')

@app.route('/sheet_info')
def sheet_info():
    sheet_data = list(users_table.find({}, {"_id": 0, "username": 1, "url": 1, "url1": 1}))
    return render_template('sheet.html', sheet_data=sheet_data)

@app.route('/')
def users():
    return render_template('user.html')

@app.route('/user', methods=['GET', 'POST'])
def add_user():
    if request.method == "POST":
        form_data = dict(request.form)
        users_table.insert_one(form_data)
        return redirect(url_for('user_list'))
    return render_template('user.html')

@app.route('/userList')
def user_list():
    user_data = list(users_table.find({}, {"_id": 0, "username": 1, "password": 1,}))
    return render_template('userList.html', user_data=user_data)

#@app.route('/userURL')
#def user_url():
#    user_data = list(users_table.find({}, {"_id": 0, "url": 1}))
#    return render_template('userList.html', user_data=user_data)




@app.route('/attendance')
def attendance():
    if "logged_in" in session:
        username = session["username"]
        url_data = list(users_table.find({"username": username}, {"_id": 0, "url": 1}))

        if len(url_data) > 0:
            url = url_data[0]["url"]
            return render_template("attendance.html", username=username, url=url)
        else:
            return render_template("attendance.html", username=username, url=None)
    return redirect('/login')  # Redirect to the login page if not logged in


@app.route('/examMarks')
def exam_marks():
    if "logged_in" in session:
        username = session["username"]
        url1_data = list(users_table.find({"username": username}, {"_id": 0, "url1": 1}))

        if len(url1_data) > 0:
            url1 = url1_data[0]["url1"]
            return render_template("examMarks.html", username=username, url1=url1)
        else:
            return render_template("examMarks.html", username=username, url1=None)
    return redirect('/login')  # Redirect to the login page if not logged in


#@app.route('/teacher')
#def teacher():
#    return render_template('teacher.html')

#@app.route('/attendance')
#def attendance():
#    return render_template('attendance.html')

#@app.route('/examMarks')
#def exam_marks():
#    return render_template('examMarks.html')



@app.route('/studentProfile')
def student_profile():
    return render_template('studentProfile.html')


@app.route('/')
def addt():
    return render_template('addTeacher.html')

@app.route('/addTeacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == "POST":
        form_data = dict(request.form)
        
        # Check if a file is included in the request
        if 'routine' in request.files:
            file = request.files['routine']
            
            # Check if the file is allowed and has a filename
            if file and allowed_file(file.filename):
                # Securely save the uploaded file
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                form_data['routine'] = filename
        
        teacher_table.insert_one(form_data)
        return redirect(url_for('teacherDB'))
    return render_template('addTeacher.html')



@app.route('/teacherDB')
def teacherDB():
    teacher_data = list(teacher_table.find({}, {"_id": 0, "name": 1, "reco": 1, "id": 1, "birthdate": 1, "gender": 1, "address": 1, "phone": 1, "email": 1}))
    return render_template('teacherDB.html', teacher_data=teacher_data)

@app.route('/')
def view():
    return render_template('viewRoutine.html')

@app.route('/view_routine/<filename>')
def view_routine(filename):
    
    return render_template('viewRoutine.html', filename=filename)


@app.route('/teacher')
def teacher():
    teacher_data = list(teacher_table.find({}, {"_id": 0, "name": 1, "reco": 1, "id": 1, "birthdate": 1, "gender": 1, "address": 1, "phone": 1, "email": 1}))
    return render_template('teacher.html', teacher_data=teacher_data)




if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)
