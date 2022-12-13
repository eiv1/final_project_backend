# import json
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)

CORS(app)

# CORS(app, supports_credentials=True)
#multiplying

app.config["SECRET_KEY"]="ibhbds7gs"
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///multiplying.sqlite3'
app.config['SESSION_TYPE'] = 'memcached'

sess = Session()

db=SQLAlchemy(app)

class Student(db.Model):  #name of table
    id=db.Column(db.Integer,primary_key=True)
    tz=db.Column(db.String(200), nullable=False)
    first_name=db.Column(db.String(200), nullable=False)
    last_name=db.Column(db.String(200), nullable=False)
    password=db.Column(db.String(200), default="12345678")
    email=db.Column(db.String(200), nullable=False)
    phone=db.Column(db.String(200), nullable=False)
    points=db.Column(db.Integer, default=0)
    role=db.Column(db.String(200),default="student")
    classrome=db.Column(db.String(200))
    school=db.Column(db.String(200), nullable=False)

    
class Teacher(db.Model):  #name of table
    id=db.Column(db.Integer,primary_key=True)
    tz=db.Column(db.String(200), nullable=False)
    first_name=db.Column(db.String(200), nullable=False)
    last_name=db.Column(db.String(200), nullable=False)
    password=db.Column(db.String(200), default="12345678")
    email=db.Column(db.String(200), nullable=False)
    phone=db.Column(db.String(200), nullable=False)
    points=db.Column(db.Integer, default=0)
    role=db.Column(db.String(200),default="teacher")
    school=db.Column(db.String(200), nullable=False)


db.create_all() #create all tables

@app.route('/all1',methods=["GET","POST"])
def index31():
    students=Student.query.all()
    Astudents=[]
    for s in students:
        Astudents.append({"id":s.id,"tz":s.tz,"first_name":s.first_name,"last_name":s.last_name,"email":s.email,"password":s.password,"phone":s.phone,"points":s.points,"classrome":s.classrome,"school":s.school})

    return ({"students":Astudents})

@app.route('/',methods=["GET","POST"])
def index():
    teachers=Teacher.query.all()  
    students=Student.query.all()  
    # contacts=Todo.query.order_by(Todo.date_created).all()
    return render_template('admin_show.html',teachers=teachers,students=students)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        tz=request.form['tz']
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email=request.form['email']
        phone=request.form['phone']
        role=request.form['role']
        classrome=request.form['classrome']
        school=request.form['school']
        if role=="teacher":
            new_teacher=Teacher(tz=tz,first_name=first_name,last_name=last_name,email=email,phone=phone,school=school)
            db.session.add(new_teacher)
            db.session.commit()
        else:
            new_student=Student(tz=tz,first_name=first_name,last_name=last_name,email=email,phone=phone,classrome=classrome,school=school)
            db.session.add(new_student)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:id>/<string:role>') # name of db (not 4 function..)
def delete(id,role):
    if role=="teacher":
        Teacher.query.filter_by(id=id).delete()
        db.session.commit()
    else:
        Student.query.filter_by(id=id).delete()
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:id>/<string:role>', methods=["POST","GET"]) #don't do update
def update_teacher(id,role):
    if role=="teacher":
        teacher=Teacher.query.filter_by(id=id).first()

        if request.method=='POST':
            teacher.tz=request.form.get('tz')
            teacher.first_name=request.form.get('first_name')
            teacher.last_name=request.form.get('last_name')
            teacher.school=request.form.get('school')
            teacher.email=request.form.get('email')
            teacher.phone=request.form.get('phone')

            db.session.commit()

            return redirect(url_for('index'))
        else:
            return render_template('update.html',user=teacher)
    else:
        student=Student.query.filter_by(id=id).first()

        if request.method=='POST':
            student.tz=request.form.get('tz')
            student.first_name=request.form.get('first_name')
            student.last_name=request.form.get('last_name')
            student.school=request.form.get('school')
            student.email=request.form.get('email')
            student.phone=request.form.get('phone')
            student.classrome=request.form.get('classrome')
            student.points=request.form.get('points')

            db.session.commit()

            return redirect(url_for('index'))
        else:
            return render_template('update.html',user=student)

@app.route('/loginS', methods=["POST"])
def login_userS():
    print(request.json)
    email=request.json["email"]
    password=request.json["password"]
    print(email)
    print(password)

    user=Student.query.filter_by(email=email).first()

    session["user_id"]=user.id
    print(user.id)

    return jsonify({
        "id":user.id,
        "email":user.email
    })

@app.route('/updatePoints', methods=["POST"])
def updatePoints():
    id=request.json["id"]
    points=request.json["points"]
    print(id)
    print(points)

    student=Student.query.filter_by(id=id).first()
    student.points=points
    db.session.commit()
    
    return ({"message":"s"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=int(os.environ.get('PORT',5000)))