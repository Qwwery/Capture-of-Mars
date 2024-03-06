import random

from flask import Flask, url_for, render_template, request
import json

app = Flask(__name__)


@app.route('/')
def main():
    info = {
        'title': 'Hello!'
    }
    return render_template('base.html', **info)


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
    img = [url_for('static', filename='img/landscapes/Пейзаж 1.png'),
           url_for('static', filename='img/landscapes/Пейзаж 2.png'),
           url_for('static', filename='img/landscapes/Пейзаж 3.png')]
    if request.method == 'GET':
        info = {
            'img': img
        }

        return render_template('carousel.html', **info)
    elif request.method == 'POST':
        new_file = f'Пейзаж {len(img)}.png'
        f = request.files['new_photo']
        with open(f'static/img/landscapes/{new_file}', 'wb') as file:
            file.write(f.read())
        img.append(url_for('static', filename=f'img/landscapes/Пейзаж {len(img) - 1}.png'))

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



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
