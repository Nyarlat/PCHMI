import smtplib
from email.header import Header
from email.mime.text import MIMEText

from labapp import db
from datetime import datetime
import re
from flask import session, make_response, redirect, url_for, jsonify
import bcrypt

"""
    В данном модуле реализуются CRUD-методы для работы с БД.
    Если в вашем приложении используется несколько сущностей (таблиц) в БД, то хорошей практикой 
    будет являться реализация ОТДЕЛЬНЫХ модулей с CRUD-операциями для каждой таблицы, при этом 
    данные модули лучше группировать в отдельном пакете Python, т.е. создавать папку с файлом __init__.py
"""


def get_tour_req_all():  # новый метод
    result = []
    rows = db.session.execute("SELECT * FROM tour").fetchall()
    for row in rows:
        result.append(dict(row))
    return {'tour': result}


# Получаем список всех запросов.
def get_contact_req_all():
    result = []  # создаем пустой список
    # Получаем итерируемый объект, где содержатся все строки таблицы contactrequests
    rows = db.session.execute("SELECT * FROM contactrequests").fetchall()
    # Каждую строку конвертируем в стандартный dict, который Flask может трансформировать в json-строку
    for row in rows:
        result.append(dict(row))
    # возвращаем dict, где result - это список с dict-объектов с информацией
    return {'contactrequests': result}


def get_login_req_all():
    result = []  # создаем пустой список
    rows = db.session.execute("SELECT * FROM logins").fetchall()
    # Каждую строку конвертируем в стандартный dict, который Flask может трансформировать в json-строку
    for row in rows:
        result.append(dict(row))
    # возвращаем dict, где result - это список с dict-объектов с информацией
    return {'logins': result}


# новый метод
def get_tour_req_by_id(id):
    result = db.session.execute(f"SELECT * FROM tour WHERE id = {id}").fetchone()
    return dict(result)


# Получаем запрос с фильтром по id
def get_contact_req_by_id(id):
    result = db.session.execute(f"SELECT * FROM tour WHERE id = {id}").fetchone()
    return dict(result)


# новый метод
def get_tour_req_by_typeoftour(typeoftour):
    result = []
    rows = db.session.execute(f"SELECT * FROM tour WHERE typeoftour = {typeoftour}").fetchall()
    for row in rows:
        result.append(dict(row))
    return {'tour': result}


# Получаем все запросы по имени автора
def get_contact_req_by_author(firstname):
    result = []
    rows = db.session.execute(f"SELECT * FROM contactrequests WHERE firstname = '{firstname}'").fetchall()
    for row in rows:
        result.append(dict(row))
    return {'contactrequests': result}


# Создать новый запрос
def create_contact_req(json_data):
    try:
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # текущая дата и время
        ownerId = session.get('userId')
        # INSERT запрос в БД
        db.session.execute(f"INSERT INTO contactrequests "
                           f"(firstname, lastname, email, reqtext, createdAt, updatedAt, ownerId) "
                           f"VALUES ("
                           f"'{json_data['firstname']}', "
                           f"'{json_data['lastname']}', "
                           f"'{json_data['email']}', "
                           f"'{json_data['reqtext']}', "
                           f"'{cur_time}', "
                           f"'{cur_time}',"
                           f"'{ownerId}')"
                           )
        # Подтверждение изменений в БД
        db.session.commit()
        # Возвращаем результат
        return {'message': "ContactRequest Created!"}
        # если возникла ошибка запроса в БД
    except Exception as e:
        # откатываем изменения в БД
        db.session.rollback()
        # возвращаем dict с ключом 'error' и текcтом ошибки
        return {'message': str(e)}

def tour_appl(json_data):
    try:
        db.session.execute(f"INSERT INTO subb_appl "
                           f"(first_name, last_name, phone_number, sugg, email, num_of_ad, num_of_child)"
                           f"VALUES ("
                           f"'{json_data['fname']}', "
                           f"'{json_data['lname']}', "
                           f"'{json_data['number']}',"
                           f"'{json_data['reqtext']}', "
                           f"'{json_data['email']}', "
                           f"'{json_data['num_of_ad']}', "
                           f"'{json_data['num_of_child']}' "
                           ")")
        # Подтверждение изменений в БД
        db.session.commit()
        sender = "heart.of.russia.2022@gmail.com"
        reciever = ""
        password = "mkmkvrgsldtrscwv"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        try:
            # Формируем тело письма
            subject = u'Application confirmed '
            body = u'Hello, for payment go to the link:\nhttps://online.sberbank.ru/'
            msg = MIMEText(body, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            server.login(sender, password)
            #message = MIMEText("Hello, for payment go to the link:\nhttps://online.sberbank.ru/")
            server.sendmail(sender, {json_data['email']}, msg.as_string())
            # Переадресуем на страницу авторизации
            # если возникла ошибка запроса в БД
            return {'message': "The message was sent"}
        except Exception as _ex:
            return f"{_ex}\nCheck your login or password please!"
        #return {'message': "ContactRequest Created!"}

    except Exception as e:
        # откатываем изменения в БД
        db.session.rollback()
        # возвращаем response с ошибкой сервера
        return make_response(jsonify({'message': str(e)}), 500)



# создание нового запроса к tour
def create_tour_req(json_data):
    try:
        db.session.execute(f"SELECT place FROM tour WHERE place LIKE '{json_data['place']}'")
        # Возвращаем результат
        return {'message': "ContactRequest Created!"}
        # если возникла ошибка запроса в БД
    except Exception as e:
        print(json_data)
        # откатываем изменения в БД
        db.session.rollback()
        # возвращаем dict с ключом 'error' и текcтом ошибки
        # return {'message': str(e)}


# Удалить запрос по id в таблице
def delete_contact_req_by_id(id):
    try:
        # DELETE запрос в БД
        db.session.execute(f"DELETE FROM contactrequests WHERE id = {id}")
        db.session.commit()
        return {'message': "ContactRequest Deleted!"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}


# Обновить текст запроса по id в таблице
def update_contact_req_by_id(id, json_data):
    try:
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # текущая дата и время
        # UPDATE запрос в БД
        db.session.execute(f"UPDATE contactrequests SET reqtext = '{json_data['reqtext']}', "
                           f"updatedAt = '{cur_time}' WHERE id = {id}")
        db.session.commit()
        return {'message': "ContactRequest Updated!"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}


def delete_contact_req_by_data(createdAt):
    try:
        # DELETE запрос в БД
        x = str(createdAt)
        y = x[0:10]
        if (re.fullmatch(r'\d{4}\-\d\d\-\d\d', y)):
            db.session.execute(f"DELETE FROM contactrequests WHERE createdAt LIKE '%{y}%'")
            # db.session.execute(f"DELETE FROM contactrequests WHERE createdAt = '{createdAt}'")
            db.session.commit()
            return {'message': "ContactRequest Deleted!"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}


def get_previous_requests():
    result = []
    ownerId = session.get('userId')
    rows = db.session.execute(f"SELECT * FROM contactrequests WHERE ownerId LIKE '%{ownerId}%'").fetchall()
    for row in rows:
        result.append(dict(row))
    return {'contactrequest': result}


def get_contact_req_by_data(createdAt):
    result = []
    rows = db.session.execute(f"SELECT * FROM contactrequests WHERE createdAt LIKE '%{createdAt}%'").fetchall()
    for row in rows:
        result.append(dict(row))
    return {'contactrequests': result}


# Поиск аккаунта пользователя в БД
def login_user(form_data):
    # Получаем логин и пароль из данных формы
    username = form_data.get('loginField')
    password = form_data.get('passField')
    if username == '':
        return redirect(url_for('login'))
    # Ищем пользователя в БД
    result = db.session.execute(f"SELECT * FROM logins WHERE username = '{username}'").fetchone()
    # если пользователь не найден переадресуем на страницу /login
    if result is None:
        return redirect(url_for('login'))
    user = dict(result)
    # если пароль не прошел проверку, переадресуем на страницу /login
    if not bcrypt.checkpw(password.encode('utf-8'), user.get('password').encode('utf-8')):
        return redirect(url_for('login'))
    # иначе регистрируем сессию пользователя (записываем логин пользователя в параметр user) и высылаем cookie "AuthToken"
    else:
        response = redirect('/services')
        session['user'] = user['username']
        session['userId'] = user['id']
        response.set_cookie('AuthToken', user['username'])
        return response


def register_user(form_data):
    # Получаем данные пользователя из формы
    username = form_data.get('loginField')
    password = form_data.get('passField')
    email = form_data.get('emailField')
    # Проверяем полученные данные на наличие обязательных полей
    if username == '' or password == '' or email == '':
        return make_response(jsonify({'message': 'The data entered are not correct!'}), 400)
        return make_response(jsonify({'message': 'The data entered are not correct!'}), 400)
    # Создаем хеш пароля с солью
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    try:
        db.session.execute(f"INSERT INTO logins "
                           f"(username, password, email) "
                           f"VALUES ("
                           f"'{username}', "
                           f"'{hashed}', "
                           f"'{email}'"
                           ")")
        # Подтверждение изменений в БД
        db.session.commit()
        # Переадресуем на страницу авторизации
        return redirect(url_for('login'))
        # если возникла ошибка запроса в БД
    except Exception as e:
        # откатываем изменения в БД
        db.session.rollback()
        # возвращаем response с ошибкой сервера
        return make_response(jsonify({'message': str(e)}), 500)

def search(name):
    place = name.get('place')
    type = name.get('type')
    date_1 = db.session.execute(f"SELECT datet FROM tours WHERE place = '{place}' AND typeoftour = '{type}'").fetchone()
    #places = db.session.execute("SELECT place FROM tours").fetchall()
    #types = db.session.execute("SELECT typeoftour FROM tours").fetchall()
    return str(date_1[0])

def testik(form_data):
    place = form_data.get('place')
    type = form_data.get('type')
    print(type)
    if place!="" and type!="":
        date_1 = db.session.execute(f"SELECT * FROM tours WHERE place = '{place}' AND typeoftour = '{type}'").fetchall()
    elif place!="":
        date_1 = db.session.execute(f"SELECT * FROM tours WHERE place = '{place}'").fetchall()
    elif type!="":
        date_1 = db.session.execute(f"SELECT * FROM tours WHERE typeoftour = '{type}'").fetchall()
    else:
        date_1 = db.session.execute(f"SELECT * FROM tours").fetchall()
    print(date_1)
    list = []
    for str in date_1:
        d = {'place':str[0],'type':str[1], 'date':str[3], 'img': str[4], 'price': str[5], 'description': str[6], 'duration': str[7],'href': str[8], 'name': str[9]}
        list.append(d)
    #print(list)
    #response = redirect(url_for('tour2',date_from = list))
    print(list)
    return list
# test
def tour_create(form_data):
    place = form_data.get('place')
    type = form_data.get('type')
    date_1 = db.session.execute(f"SELECT datet FROM tours WHERE place = '{place}' AND typeoftour = '{type}'").fetchall()
    response = redirect(url_for('tour',date_from = date_1))
    return response


def load():
    date_1 = db.session.execute(f"SELECT * FROM tours").fetchall()
    list = []
    for str in date_1:
        d = {'place':str[0],'type':str[1], 'date':str[3], 'img': str[4], 'price': str[5], 'description': str[6], 'duration': str[7],'href': str[8], 'name': str[9]}
        list.append(d)
    return list