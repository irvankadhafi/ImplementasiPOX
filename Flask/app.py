import os
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, Response
import mysql.connector
from hashlib import md5
from base64 import b64encode
from subprocess import Popen, call, PIPE
from celery import Celery

app = Flask(__name__)
config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'implementasipox'
    }
db = mysql.connector.connect(**config)
cur = db.cursor()
p="a"
#Celery configuration
app.config['CELERY_BROKEN_URL'] = 'redis://0.0.0.0:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://0.0.0.0:6379/0'

#initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKEN_URL'])
celery.conf.update(app.config)


@app.route('/test')
def main():
    return render_template('index.html')

@app.route('/')
def index():
    error = None
    print(index)
    if 'username' in session:
        return 'test';
    return render_template('login-gui.html',error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print(signup)
    error = None
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']
        sql = "INSERT INTO user(username, pwd) VALUES(%s ,%s)"
        data = (username_form, password_form)
        cur.execute(sql,data)
        db.commit()
        error = "Berhasil Daftar!"
    return render_template('login-gui.html', error=error)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)
