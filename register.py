from flask import Flask
import datetime
from data import db_session
from data.__all_models import users, jobs
from flask import render_template
import random
import flask
import os
from flask import url_for, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField
import flask
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


Jobs = jobs.Jobs
User = users.User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init("db/mars.sqlite")
session = db_session.create_session()


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password_1 = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


def make_users():
    for i in range(10):
        info = [random.choice(['Ivanov', 'Vasilev', 'Antonov', 'Andreev', 'Alekseev']),
                random.choice(['Ivan', 'Andrey', 'Anton', 'Vasiliy', 'Aleksey']),
                random.choice(list(range(12, 40))),
                random.choice('middle junior senior'.split()),
                random.choice('programmer povar ingeneer pilot captain'.split()),
                'module_' + str(random.choice(list(range(1, 10)))),
                random.choice(list('qwertyuioasdfghjkzxcvbnm')) + random.choice(
                    list('qwertyuioasdfghjkzxcvbnm')) + random.choice(
                    list('qwertyuioasdfghjkzxcvbnm')) + '@ya.ru'
                ]

        s = User()
        s.surname = info[0]
        s.name = info[1]
        s.age = int(info[2])
        s.position = info[3]
        s.speciality = info[4]
        s.address = info[5]
        s.email = info[6]
        session.add(s)
        session.commit()


def make_jobs():
    for i in range(10):
        s = random.choice([2, 3, 4])
        lst = []
        lst2 = list(range(1, 11))
        for i in range(s):
            d = random.choice(lst2)
            lst.append(str(d))
            lst2.remove(d)
        team_lead_id = random.choice(list(range(1, 10)))
        info = [team_lead_id,
                random.choice(
                    'Make module_1, Make module_2, Make_module_3, Взять грунт, Поставить кровати, Заспавнить мобов'.split(
                        ', ')),
                random.choice(list(range(3, 30))),
                ', '.join(lst),
                session.query(User).filter(User.id == team_lead_id).first()
                ]

        s = Jobs()
        s.team_leader_id = info[0]
        s.job = info[1]
        s.work_size = int(info[2])
        s.collaborators = info[3]
        s.team_leader = info[4]
        session.add(s)
        session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password_1.data == form.password_2.data:
                s = User()
                s.surname = form.surname.data
                s.name = form.name.data
                s.age = form.age.data
                s.position = form.position.data
                s.speciality = form.speciality.data
                s.address = form.address.data
                s.email = form.email.data
                s.set_password(form.password_1.data)
                session.add(s)
                session.commit()
                return 'Регистрация успешна'
        else:
            return 'Регистрация не успешна'
    return render_template('register_form.html', form=form)


def main():
    app.run()


if __name__ == '__main__':
    main()
