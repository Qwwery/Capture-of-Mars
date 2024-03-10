import json
import os
import random

from flask import Flask, url_for, render_template, request
from flask import redirect

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'me_secret_key:('


def create_user(surname, name, age, position, speciality, address, email, hashed_password,
                modified_date=None):
    db_sess = db_session.create_session()
    user = User()
    user.surname = surname
    user.name = name
    user.age = age
    user.position = position
    user.speciality = speciality
    user.address = address
    user.email = email
    user.hashed_password = hashed_password
    if modified_date:
        user.modified_date = modified_date
    db_sess.add(user)
    db_sess.commit()


def add_job(team_leader, job, work_size, collaborators, start_date=None, end_date=None, is_finished=None):
    db_sess = db_session.create_session()
    jobs = Jobs()

    jobs.team_leader = team_leader
    jobs.job = job
    jobs.work_size = work_size
    jobs.collaborators = collaborators
    if start_date:
        jobs.start_date = start_date
    if end_date:
        jobs.end_date = end_date
    if is_finished:
        jobs.is_finished = is_finished
    db_sess.add(jobs)
    db_sess.commit()


@app.route('/')
def main():
    db_session.global_init('db/mars_explorer.db')
    db_sess = db_session.create_session()
    user_info = db_sess.query(Jobs).all()
    info = {
        'title': 'Hello!',
        'jobs': user_info
    }
    return render_template('home.html', **info)


@app.route('/training/<prof>')
def training(prof):
    print(prof)
    if 'инженер' in prof.lower() or 'строитель' in prof.lower():
        info = {
            'title': prof,
            'text': 'Инженерные тренажеры',
            'img': f"{url_for('static', filename='img/инженерный.png')}"
        }
    else:
        info = {
            'title': prof,
            'text': 'Научные тренажеры',
            'img': f"{url_for('static', filename='img/научный.png')}"
        }
    return render_template('training.html', **info)


@app.route('/list_prof/<list>')
def list_prof(list):
    info = {
        'title': 'Профессии',
        'type_list': list,
        'prof': ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач', 'инженер по терраформированию',
                 'климатолог', 'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
                 'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода', 'киберинженер', 'штурман',
                 'пилот дронов']
    }
    return render_template('list_prof.html', **info)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/distribution')
def distribution():
    team = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандерс', 'Шон Бин']
    info = {
        'team': team
    }

    return render_template('distribution.html', **info)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    color = 'box1'

    if sex == 'male':
        if age < 21:
            color = 'box2'
        else:
            color = color
    else:
        if age < 21:
            color = 'box3'
        else:
            color = 'box4'

    if age < 21:
        img = 'mini'
    else:
        img = 'big'
    info = {
        'color': color,
        'img': img
    }

    return render_template('table.html', **info)


@app.route('/carousel', methods=['POST', 'GET'])
def carousel():
    files = os.listdir('static/img/landscapes')
    img = []
    for i in files:
        i = i.split('\\')[-1]
        img.append(url_for('static', filename=f'img/landscapes/{i}'))
    if request.method == 'GET':
        info = {
            'img': img
        }

        return render_template('carousel.html', **info)
    elif request.method == 'POST':
        new_file = f'Пейзаж {len(img) + 1}.png'
        f = request.files['new_photo']
        with open(f'static/img/landscapes/{new_file}', 'wb') as file:
            file.write(f.read())
        img.append(url_for('static', filename=f'img/landscapes/Пейзаж {len(img) + 1}.png'))

        info = {
            'img': img
        }

        return render_template('carousel.html', **info)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    info = {
        'title': 'Заголовок',
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'выше высшего',
        'profession': 'штурман марсоход',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на марсе!',
        'ready': 'True'
    }

    return render_template('answer.html', **info)


@app.route('/member')
def member():
    with open('templates/js.js', 'r', encoding='utf-8') as f:
        data = json.load(f)
    random.shuffle(data)
    data = data[0]
    info = {
        'info_user': data
    }

    return render_template('member.html', **info)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        print('ok')
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data,
            hashed_password=form.password.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    print(form.errors)
    return render_template('register.html', title='Регистрация', form=form, message='Поля заполнены некорректно')


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    try:
        create_user('Scott', 'Ridley', 21, 'captain', 'research engineer', 'module_1', 'scott_chief@mars.org', '1111')
        create_user('Сахаров', 'Илья', 15, 'admin=)', 'крутой', 'module_3000', 'qwe@qwe.qwe', '1112')
        create_user('Ларионов', 'Валера', 17, 'zam.admin=)', 'крутой', 'module_3001', 'qw1e@qwe1.qwe1', '1113')
        create_user('Мотовилов', 'Григорий', 16, 'zam.zam.admin=)', 'почти крутой', 'нет', 'qwe99@qwe99.qwe99', '9999')

        add_job(1, 'deployment of residential modules 1 and 2', 15, '2, 3')
    except Exception:
        print('Ошибка передачи параметров!!!')
    app.run()
    app.run(port=8080, host='127.0.0.1', debug=True)
