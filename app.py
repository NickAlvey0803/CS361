#!/usr/bin python

from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'

# Initialize DB

db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    workout_time = db.Column(db.Integer, nullable=False)
    workout_distance = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<Workout %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.id

db.create_all()


@app.route('/')
def home():
    title = "LogMyRun Home"

    return render_template("index.html", title=title)

@app.route('/login')
def login():
    title = "Log In"

    if request.method == "POST":

        # existing user

        login_username = request.form['name']
        login_password = request.form['password']

        # new user

        new_username = request.form['new_name']
        new_password = request.form['new_password']
        new_conf_password = request.form['conf_new_name']

        if login_username == None:
            if new_password == new_conf_password:
                new_user = User(username=new_username, password=new_conf_password)
            else:
                return "Passwords don't match!"
        else:
            pass

        # add to db

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return "Error!"

    else:
        return render_template("login.html", title=title)

@app.route('/workouts', methods=['POST', 'GET'])
def workouts():
    title = "Your Workouts"

    if request.method == "POST":

        form_workout_time = request.form['time']
        form_workout_distance = request.form['distance']

        new_workout = Workout(workout_time=form_workout_time, workout_distance = form_workout_distance)

        # add to db

        try:
            db.session.add(new_workout)
            db.session.commit()
            return redirect('/workouts')
        except:
            return "Error!"

    else:
        show_workouts = Workout.query.order_by(Workout.date_created)
        return render_template("workouts.html", title=title, workouts=show_workouts)

@app.route('/update/<int:newid>', methods=['POST', 'GET'])
def update(newid):
    workout_to_update = Workout.query.get_or_404(newid)
    if request.method == "POST":
        workout_to_update.workout_time = request.form['new_time']
        workout_to_update.workout_distance = request.form['new_distance']
        try:
            db.session.commit()
            return redirect('/workouts')
        except:
            return "Error in Update!"

    else:
        return render_template('update.html', workout_to_update=workout_to_update)

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    workout_to_delete = Workout.query.get_or_404(id)
    try:
        db.session.delete(workout_to_delete)
        db.session.commit()
        return redirect('/workouts')
    except:
        return "Error in Delete!"

@app.route('/logrun')
def logrun():
    title = "Log Your Run"



    return render_template("logrun.html", title=title, datetime = str(datetime.now()))

@app.route('/comparetime')
def comparetime():
    title = "Compare Run Times"

    return render_template("comparetime.html", title=title)

@app.route('/changepass', methods=['POST', 'GET'])
def changepass():
    title = "Change Your Password"

    if request.method == "POST":
        pass_to_update = User.query.filter_by(username=request.form['name']).first()
        pass_to_update.password = request.form['password']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error in Update!"

    return render_template("changepass.html", title=title)



if __name__ == "__main__":
    app.run(debug=True)