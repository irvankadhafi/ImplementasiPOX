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
        # celery.send_task('tasks.tambahdockers', args=[11,"10.0.0.2/8", "mysql:5.7","s"+1], kwargs={})
        username_form = session['username']
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT id_user FROM user WHERE username=%s"
        data = (username_form)
        cursor.execute(sql,data)
        hasil = cursor.fetchall()
        for hasil1 in hasil:
            idUser_form=str(hasil1[0])

        sql = "SELECT * from dockerhost where iduser=%s"
        data = (idUser_form)
        cursor.execute(sql,data)
        rows = cursor.fetchall()

        error = "Berhasil Daftar!"
        return render_template('index-gui.html',rows=rows, error=error)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/add-gui')
def addgui():
    error = None
    print(index)
    if 'username' in session:
        return render_template('add-gui.html')
    return render_template('login-gui.html', error=error)

@app.route('/tesnet')
def tesNet():
    task = celery.send_task('tasks.tesNets')
    res = celery.AsyncResult(task.id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)

@app.route('/addswitch')
def lordyAddSwitches():
    conn = None
    cursor = None
    try:
        source = str(session['username'])
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT id_user FROM user WHERE username=%s"
        data = (source)
        cursor.execute(sql,data)
        hasil = cursor.fetchall()
        for hasil1 in hasil:
            source_id=str(hasil1[0])

        source_id="s"+str(source_id)
        celery.send_task('tasks.addSwitchs', args=[source_id], kwargs={})
        return str(source_id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



#untuk restart jaringan
@app.route('/tescelery')
def tescelery():
    celery.send_task('tasks.myNetworks')
    return "Network Started"

@app.route('/tambahdocker')
def tambahdocker():
    celery.send_task('tasks.tambahdockers')
    return "docker berhasil ditambah"

@app.route('/formtambahlink')
def formtambahlink():
    return render_template('formtambahlink.html')

@app.route('/formlinkupdown')
def formlinkupdown():
    return render_template('formlinkupdown.html')

@app.route('/seelinkofswitch')
def seelinkofswitch():
    hasil = None
    if 'username' in session:
        username_form = str(session['username'])

    print(username_form)
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT id_user FROM user WHERE username=%s"
        data = (username_form)
        cursor.execute(sql,data)
        hasil = cursor.fetchall()
        for hasil1 in hasil:
            iduser=str(hasil1[0])
            print(iduser)
            sql = "SELECT linkofswitch.source,userSource.username, linkofswitch.destination, userDestination.username FROM `linkofswitch` JOIN `user` userSource ON linkofswitch.source = userSource.id_user JOIN `user` userDestination ON linkofswitch.destination = userDestination.id_user WHERE source = %s OR destination = %s"
            data = (iduser,iduser)
            cursor.execute(sql,data)
            hasil=cursor.fetchall();
            return render_template('seeLink.html', hasil = hasil )
        error=None
        return render_template('login-gui.html', error=error)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

'''Method Get/Post'''

@app.route('/user', methods=['GET', 'POST'])
def user():
    return redirect(url_for('indexpage'))

@app.route('/login-gui', methods=['GET', 'POST'])
def login():
    print(login)
    error = None
    conn = None
    cursor = None
    try:
        if 'username' in session:
            return redirect(url_for('indexpage'))
        if request.method == 'POST':
            username_form = request.form['username']
            password_form = request.form['password']
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "SELECT COUNT(1) FROM user WHERE username = %s;"
            data = (username_form)
            cursor.execute(sql,data) # CHECKS IF USERNAME EXSIST
        if cursor.fetchone()[0]:
            sql = "SELECT pwd FROM user WHERE username = %s;"
            data = (username_form)
            cursor.execute(sql,data) # FETCH THE HASHEDPASSWORD
            for row in cursor.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('user'))
                else:
                    error = "Salah password!"
        else:
            error = "Anda belum terdaftar!"
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
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "INSERT INTO user(username, pwd) VALUES(%s ,%s)"
            data = (username_form, password_form)
            cursor.execute(sql,data)
            conn.commit()
            error = "Berhasil Daftar!"
            return render_template('login-gui.html', error=error)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route('/tambahlink', methods=['GET', 'POST'])
def tambahlink():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        source=session['username']
        dest=request.form['dest']
        status=1
        sql = "SELECT id_user FROM user WHERE username = %s;"
        data = (source)
        cursor.execute(sql,data)
        hasil=cursor.fetchall()
        for hasil1 in hasil:
            source_id=str(hasil1[0])

        sql = "SELECT id_user FROM user WHERE username = %s;"
        data = (dest)
        cursor.execute(sql,data)
        hasil=cursor.fetchall()
        for hasil1 in hasil:
            dest_id=str(hasil1[0])
        source_id_string="s"+str(source_id)
        dest_id_string="s"+str(dest_id)
        dest_id=int(dest_id)
        source_id=int(source_id)
        celery.send_task('tasks.tambahlinks', args=[source_id_string, dest_id_string], kwargs={})
        sql = "INSERT INTO linkofswitch(source, destination) VALUES(%s, %s);"
        data = (source_id, dest_id)
        cursor.execute(sql,data)
        conn.commit()
        return redirect(url_for('fetchTable'))
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/addDocker', methods=['GET', 'POST'])
def addDockers():
    error= None
    print(index)
    conn = None
    cursor = None
    try:
        if request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor()
            username_form = session['username']
            dockerName_form = request.form['dockerName']
            dockerImage_form = request.form['dockerImage']

            #cari IDDocker
            sql = "SELECT iddocker FROM dockerhost ORDER BY iddocker DESC LIMIT 1"
            cursor.execute(sql)
            hasil=cursor.fetchall()
            for hasil1 in hasil:
                idDocker_form=str(int(str(hasil1[0]))+1)
            #cari UserID
            sql = "SELECT id_user FROM user WHERE username = %s;"
            data = (username_form)
            cursor.execute(sql,data)
            hasil=cursor.fetchall()

            for hasil1 in hasil:
                idUser_form=str(hasil1[0])

            ipAddress="10.0.0."+idDocker_form
            sql = "INSERT INTO dockerhost(iduser,dockername,iddocker,jenisdocker,ip_address) VALUES(%s,%s,%s,%s,%s)"
            data = (idUser_form,dockerName_form,idDocker_form, dockerImage_form,ipAddress)
            cursor.execute(sql,data)
            conn.commit()

            #Nambah Docker di mininet
            celery.send_task('tasks.tambahdockers', args=[idDocker_form,"10.0.0."+idDocker_form+"/8", dockerImage_form,"s"+idUser_form], kwargs={})
            return redirect(url_for('fetchTable'))
            #nyeluk shell/mininet script
        return "Under Construction"
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/upOrDown', methods=['GET', 'POST'])
def upOrDown():
    conn = None
    cursor = None
    try:
        if request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor()
            dockerID_form = request.form['dockerID']
            mndocker="mn.d"+dockerID_form
            sql = "SELECT dockerstatus FROM dockerhost WHERE iddocker = %s;"
            data = (dockerID_form)
            cursor.execute(sql,data)
            hasil=cursor.fetchall()
            for hasil1 in hasil:
                dockerStatus_form=str(hasil1[0])
            if dockerStatus_form=='1':
                sql = "UPDATE dockerhost SET dockerstatus=0 WHERE iddocker = %s;"
                data = (dockerID_form)
                cursor.execute(sql,data)
                conn.commit()

                #popen stop docker
                output = Popen(['docker', 'stop', mndocker],stdout=PIPE)
                output.communicate()
            else:
                sql = "UPDATE dockerhost SET dockerstatus=1 WHERE iddocker = %s;"
                data = (dockerID_form)
                cursor.execute(sql,data)
                conn.commit()

                #popen start docker
                output = Popen(['docker', 'start', mndocker],stdout=PIPE)
                output.communicate()
            return redirect(url_for('fetchTable'))
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/deleteDocker', methods=['GET', 'POST'])
def deleteDocker():
    conn = None
    cursor = None
    try:
        if request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor()
            dockerID_form = request.form['dockerID']
            mndocker="mn.d"+dockerID_form
            sql = "SELECT dockerstatus FROM dockerhost WHERE iddocker = %s;"
            data = (dockerID_form)
            cursor.execute(sql,data)
            hasil=cursor.fetchall()
            for hasil1 in hasil:
                dockerStatus_form=str(hasil1[0])
            if dockerStatus_form=='1':
                output = Popen(['docker', 'stop', mndocker],stdout=PIPE)
            output.communicate()
            output = Popen(['docker', 'rm', mndocker],stdout=PIPE)
            output.communicate()
            sql = "DELETE FROM dockerhost WHERE iddocker = %s;"
            data = (dockerID_form)
            cursor.execute(sql,data)
            conn.commit()
            return redirect(url_for('fetchTable'))
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/linkupdown', methods=['GET', 'POST'])
def linkupdown():
    conn = None
    cursor = None
    try:
        if request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor()
            source=session['username']
            dest=request.form['dest']
            linkStatus=9
            sql = "SELECT id_user FROM user WHERE username = %s;"
            data = (source)
            cursor.execute(sql,data)
            hasil=cursor.fetchall()
            for hasil1 in hasil:
                source_id=str(hasil1[0])
            sql = "SELECT id_user FROM user WHERE username = %s;"
            data = (dest)
            cursor.execute(sql,data)
            hasil=cursor.fetchall()
            for hasil1 in hasil:
                dest_id=str(hasil1[0])
            source_id_string="s"+str(source_id)
            dest_id_string="s"+str(dest_id)
            celery.send_task('tasks.delLinks', args=[source_id_string,dest_id_string], kwargs={})
            sql = "DELETE FROM linkofswitch WHERE source = %s AND destination = %s;"
            data = (source_id,dest_id)
            cursor.execute(sql,data)
            conn.commit()
            return "berhasil hapusnya"
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conn.close()
@app.route('/seePort', methods=['GET', 'POST'])
def seePort():
    if request.method=='POST':
        dockerID_form = request.form['dockerID']
        mndocker="name=mn.d"+dockerID_form
        output = Popen(['docker', 'ps','-f',mndocker, '--format', '"{{.Ports}}"'], stdout=PIPE)
        output = output.stdout.read()
        return render_template('seePort.html', output = output )

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

app.secret_key = 'awankinton123'
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)
