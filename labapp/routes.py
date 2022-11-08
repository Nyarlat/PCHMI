# -*- coding: utf-8 -*-
# Подключаем объект приложения Flask из __init__.py
from labapp import app, db
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for
import functools
from . import dbservice





"""

    Модуль регистрации маршрутов для запросов к серверу, т.е.
    здесь реализуется обработка запросов при переходе пользователя на определенные адреса веб-приложения

"""

# Структура основного навигационнго меню веб-приложения,
# оформленное в виде массива dict-объектов
navmenu = [
    {
        'name': 'HOME',
        'addr': '/homepage'
    },
    {
        'name': 'ABOUT US',
        'addr': '/aboutus'
    },
    {
        'name': 'SERVICES',
        'addr': '/services'
    },
    #{
    #    'name': 'BLOG ',
    #    'addr': '/blog'
    #},
    {
        'name': 'CONTACT',
        'addr': '/contact'
    },
]

# Функция-декоратор для проверки авторизации пользователя
def login_required(route_func):
    @functools.wraps(route_func)
    def decorated_route(*args, **kwargs):
        # Если не установлен параметр сессии user или значение cookie 'AuthToken' не равно логину пользователя
        if not session.get('user') or request.cookies.get('AuthToken') != session.get('user'):
            # перенаправляем на страницу авторизации
            return redirect(url_for('login'))
        return route_func(*args, **kwargs)
    return decorated_route



# Обработка запроса к индексной странице
@app.route('/')
@app.route('/homepage')
def homepage():
    css = "homepage.css"
    imgs = ['Logo.png', 'st-petersburg.jpg','man-touris.jpg', 'Logo-bottom.png']
    # "рендеринг" (т.е. вставка динамически изменяемых данных) index.html и возвращение готовой страницы
    return render_template('homepage.html', title='Wind Power', pname='HOME', navmenu=navmenu, imgs=imgs, css=css)

# Обработка запроса к странице contact.html
@app.route('/contact')
def contact():
    css = "contact.css"
    js = "formsend.js"
    return render_template('contact.html', title='Contact', pname='CONTACT', navmenu=navmenu, css=css, js=js)

@app.route('/aboutus')
def aboutus():
    css = "aboutus.css"
    js = "aboutus.js"
    imgs = ['Logo.png', 'supreme.png', 'Logo-bottom.png']
    # "рендеринг" (т.е. вставка динамически изменяемых данных) index.html и возвращение готовой страницы
    return render_template('aboutus.html', title='About Us', pname='ABOUT US', navmenu=navmenu, imgs=imgs, css=css, js=js)

@app.route('/services')
@login_required
def services():
    css = "services.css"
    imgs = ['Logo.png', 'turbine.png', 'Logo-bottom.png']
    js = "services.js"
    # "рендеринг" (т.е. вставка динамически изменяемых данных) index.html и возвращение готовой страницы
    return render_template('services.html', title='Services', pname='SERVICES', navmenu=navmenu, imgs=imgs, css=css,js=js)


@app.route('/previous_requests', methods=['GET'])
def get_previous_requests():
    previous = dbservice.get_previous_requests()
    return json_response(previous)


# Обработка POST-запроса для демонстрации AJAX
@app.route('/api/contactrequest', methods=['GET'])
# Получаем все записи contactrequests из БД
def get_contact_req_all():
    response = dbservice.get_contact_req_all()
    return json_response(response)

@app.route('/api/users', methods=['GET'])
# Получаем все записи contactrequests из БД
def get_login_req_all():
    response = dbservice.get_login_req_all()
    return json_response(response)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если POST-запрос
    if request.method == 'POST':
        # если нажата кнопка "Зарегистрировать", переадресуем на страницу регистрации
        if request.form.get('regBtn') == 'true':
            return redirect(url_for('register'))
        # иначе запускаем авторизацию по данным формы
        else:
            return dbservice.login_user(request.form)
    else:
        css = "register.css"
        imgs = ['Logo.png', 'Logo-bottom.png']
        return render_template('login.html', title='Log in', pname='LOGIN', navmenu=navmenu, imgs=imgs, css=css)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Если POST-запрос, регистрируем нового пользователя
    if request.method == 'POST':
        return dbservice.register_user(request.form)
    else:
        css = "register.css"
        imgs = ['Logo.png', 'Logo-bottom.png']
        return render_template('register.html', title='Registration', pname='REGISTRATION', navmenu=navmenu, imgs=imgs, css=css)


# новый метод
@app.route('/api/tour/<string:typeoftour>', methods=['GET'])
def get_tour_req_by_typeoftour(typeoftour):
    response = dbservice.get_tour_req_by_typeoftour(typeoftour)
    return json_response(response)


@app.route('/api/contactrequest/<int:id>', methods=['GET'])
# Получаем запись по id
def get_contact_req_by_id(id):
    response = dbservice.get_contact_req_by_id(id)
    return json_response(response)


@app.route('/api/contactrequest/author/<string:firstname>', methods=['GET'])
# Получаем запись по имени пользователя
def get_get_contact_req_by_author(firstname):
    if not firstname:
        # то возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
        # Иначе отправляем json-ответ
    else:
        response = dbservice.get_contact_req_by_author(firstname)
    return json_response(response)


@app.route('/api/contactrequest/<string:createdAt>', methods=['GET'])

def get_contact_req_by_data(createdAt):
    response = dbservice.get_contact_req_by_data(createdAt)
    return json_response(response)


# измененный метод

@app.route('/api/contactrequest', methods=['POST'])
# Обработка запроса на создание новой записи в БД
def create_contact_req():
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в данных нет обязательного поля 'firstname' или 'reqtext'
    if not request.json or not 'firstname' or not 'reqtext' in request.json:
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе добавляем запись в БД отправляем json-ответ
    else:
        response = dbservice.create_contact_req(request.json)
        return json_response(response)





@app.route('/api/contactrequest/<int:id>', methods=['PUT'])
# Обработка запроса на обновление записи в БД
def update_contact_req_by_id(id):
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в данных нет обязательного поля 'reqtext'
    if not request.json or not 'reqtext' in request.json:
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе обновляем запись в БД и отправляем json-ответ
    else:
        response = dbservice.update_contact_req_by_id(id, request.json)
        return json_response(response)


@app.route('/api/contactrequest/<int:id>', methods=['DELETE'])
# Обработка запроса на удаление записи в БД по id
def delete_contact_req_by_id(id):
    response = dbservice.delete_contact_req_by_id(id)
    return json_response(response)

@app.route('/api/contactrequest/<string:createdAt>', methods=['DELETE'])
# Обработка запроса на удаление записи в БД по дате
def delete_contact_req_by_data(createdAt):
    response = dbservice.delete_contact_req_by_data(createdAt)
    return json_response(response)




"""
    Реализация response-методов, возвращающих клиенту стандартные коды протокола HTTP
"""

# Возврат html-страницы с кодом 404 (Не найдено)
@app.route('/notfound')
def not_found_html():
    return render_template('404.html', title='404', err={ 'error': 'Not found', 'code': 404 })

# Формирование json-ответа. Если в метод передается только data (dict-объект), то по-умолчанию устанавливаем код возврата code = 200
# В Flask есть встроенный метод jsonify(dict), который также реализует данный метод (см. пример метода not_found())
def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))

# Пример формирования json-ответа с использованием встроенного метода jsonify()
# Обработка ошибки 404 протокола HTTP (Данные/страница не найдены)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)

# Обработка ошибки 400 протокола HTTP (Неверный запрос)
def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/api/tour',methods=['POST'])
def tour_req():
    response = dbservice.search(request.json)
    return json_response(response)




