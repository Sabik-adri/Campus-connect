from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['add']

@app.route('/')
def index():
    return render_template('addStudent.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    parent = request.form['parent']
    course = request.form['course']
    section = request.form['section']
    student_id = request.form['id']
    birthdate = request.form['birthdate']
    gender = request.form['gender']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']
    
    student = {
        'name': name,
        'parent': parent,
        'course': course,
        'section': section,
        'id': student_id,
        'birthdate': birthdate,
        'gender': gender,
        'address': address,
        'phone': phone,
        'email': email
    }
    
    collection.insert_one(student)
    return 'Student information added successfully!'

if __name__ == '__main__':
    app.run(debug=True)
