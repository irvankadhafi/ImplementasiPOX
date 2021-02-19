import os
import time
from app import app
from db_config import mysql
from flask import session, redirect, url_for, escape, request, render_template, jsonify, Response
import pymysql
from hashlib import md5
from base64 import b64encode
from subprocess import Popen, call, PIPE
from worker import celery
import celery.states as states
# import lordy

p="a"

@app.route('/')
def index():
    error = None
    print(index)
    if 'username' in session:
        return redirect(url_for('indexpage'))
    return render_template('login-gui.html',error=error)

@app.route('/index-gui')
def indexpage():
    error = None
    print(index)
    if 'username' in session:
        return redirect(url_for('fetchTable'))
    return render_template('login-gui.html', error=error)

@app.route('/logout')
def logout():
    error = 'Berhasil Log Out!'
    session.pop('username', None)
    return render_template('login-gui.html', error=error)

@app.route('/fetchTable')
def fetchTable():
    rows = None
    error = None
    hasil = None
    print(index)
    conn = None
    cursor = None
    try:
        username_form = session['username']
        sql = "SELECT id_user FROM users WHERE username=%s"
        data = (username_form)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql,data)
        hasil = cursor.fetchall()
        for hasil1 in hasil:
            idUser_form=str(hasil1[0])

        conn.commit()
        error = "Berhasil Daftar!"
        return render_template('login-gui.html', error=error)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print(signup)
    error = None
    if request.method == 'POST':
        conn = None
        cursor = None
        try:
            username_form = request.form['username']
            password_form = request.form['password']
            sql = "INSERT INTO user(username, pwd) VALUES(%s ,%s)"
            data = (username_form, password_form)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql,data)
            conn.commit()
            error = "Berhasil Daftar!"
            return render_template('login-gui.html', error=error)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route('/list-user')
def users():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user")
        rv = cursor.fetchall()
        return str(rv)
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conn.close()

# Program Contoh Celery
@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response

@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)
