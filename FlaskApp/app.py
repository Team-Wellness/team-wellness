from flask import Flask, request, session, g, redirect, url_for, abort, request, render_template, flash
import random
from flask_login import LoginManager
from flask_simplelogin import SimpleLogin
import sqlite3
import datetime

app = Flask(__name__) # create the application instance
SimpleLogin(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

conn = sqlite3.connect('database.db', check_same_thread=False)
print("Opened database successfully")
now = datetime.datetime.now()


@app.route("/", methods=['GET', 'POST'])
def main():
    error = 'none';
    cur = conn.cursor()
    if request.method == 'POST':
        if request.form['loginType'] == 'p':
            usernameP = request.form['usernameP']
            passwordP = request.form['passwordP']
            cur.execute("select * from patients where username = ? and password = ?", (usernameP, passwordP,))
            data = cur.fetchall()
            if cur.fetchone() is None:
                for id in data:
                    return redirect(url_for('homeP', id_num=id[1]))# Redirect to patient home
            else:
                error == 'Could not find account using email or password'
        elif request.form['loginType'] == 'd':
            usernameDr = request.form['usernameDr']
            passwordDr = request.form['passwordDr']
            cur.execute("select * from doctors where username = ? and password = ?", (usernameDr,passwordDr,))
            data = cur.fetchall()
            if cur.fetchone() is None:
                for id in data:
                    return redirect(url_for('homeDr', id_number=id[3]))  # Redirect to provider home
            else:
                error == 'Could not find account using email or password'
    return render_template('index.html')

@app.route('/providerHome/<id_number>', methods=['GET', 'POST'])
def homeDr(id_number):
    currentDoctor = id_number
    print(currentDoctor)
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from patients where id_num in (select patient_id from relationships where dr_id = " + id_number + ");") # who exist in the relationships table
    data = cur.fetchall()
    print(currentDoctor)
    return render_template('provider/providerHome.html', data=data, id_number=id_number)


# View screen of patients you can add
@app.route('/providerAdd/<id_number>')
def addDr(id_number):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from patients p where not exists (select * from relationships r where p.id_num in (select patient_id from relationships where dr_id = " + id_number + "));")
    data = cur.fetchall()
    return render_template('provider/providerAdd.html', data=data, id_number=id_number)


# Confirm you are adding a patient
@app.route('/providerConfirm/<id_number>/<patientId>', methods=['GET', 'POST'])
def confirmAddDr(patientId, id_number):
    global relationship_id, dr_id, patient_id
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from patients p where p.id_num ==" + patientId + ";")
    data = cur.fetchall()
    relationship_id = random.randint(0, 10000)
    dr_id = id_number;
    patient_id = patientId;
    rows = [(dr_id, patient_id, relationship_id)]
    # cur.bindarraysize = 1
    cur.setinputsizes(int, int, int)
    cur.executemany("insert into relationships(dr_id, patient_id, relationship_id) values (:1, :2, :3)", rows)
    conn.commit()
    print("success!")
    return render_template('provider/providerConfirm.html', data=data, id_number=id_number)


@app.route('/providerDeleteConfirm/<id_number>/<testVar>', methods=['GET', 'POST'])
def confirmDeleteDr(testVar, id_number):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from patients p where p.id_num ==" + testVar + ";")
    data = cur.fetchall();
    patient_id = testVar
    cur.setinputsizes(int)
    cur.execute("delete from relationships where patient_id = " + patient_id + ";")
    conn.commit()
    print("Success!")
    return render_template('provider/providerDeleteConfirm.html', data=data, id_number=id_number)


# Deletes message from provider side/database FIX THIS ONE AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
@app.route('/providerDeleteMsg/<id_number>/<msgVar>', methods=['GET', 'POST'])
def confirmMessageDeleteDr(msgVar, id_number):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from patients p where p.id_num =" + msgVar + ";")
    data = cur.fetchall()
    patient_id = msgVar
    cur.setinputsizes(int)
    cur.execute("delete from message where msg_id = " + msgVar + ";")
    conn.commit()
    print("Success!")
    return render_template('provider/providerDeleteMsg.html', data=data, id_number=id_number)


# Removes patient from dr's care
@app.route('/providerDeleteMsgConfirm/<id_number>/<testVar>', methods=['GET', 'POST'])
def confirmMsgDeleteDr(testVar, id_number):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from patients p where p.id_num ==" + testVar + ";")
    data = cur.fetchall();
    patient_id = testVar
    cur.setinputsizes(int)
    cur.execute("delete from relationships where patient_id = " + patient_id + ";")
    conn.commit()
    print("Success!")
    return render_template('provider/providerDeleteMsgConfirm.html', data=data, id_number=id_number)


@app.route('/providerMessages/<id_number>', methods=['GET', 'POST'])
def msgDr(id_number):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from patients a join message b on a.id_num = b.patient where b.dr = " + id_number + ";")
    joinedData = cur.fetchall()
    return render_template('provider/providerMessages.html', joinedData=joinedData, id_number=id_number)


# Actually confirms that note has been sent, not msg
# testVar is patient's id, id_number is doctor's id
@app.route('/providerConfirmMsgSend/<id_number>/<testVar>', methods=['GET', 'POST'])
def noteConfirmDr(testVar, id_number):
    global relationship_id, dr_id, patient_id
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from patients p where p.id_num ==" + testVar + ";")
    data = cur.fetchall()
    note_id = random.randint(0, 10000)
    dr_id = id_number
    patient_id = testVar
    rows = [(dr_id, patient_id, relationship_id)]
    # cur.bindarraysize = 1
    cur.setinputsizes(int, int, int)
    cur.executemany("insert into doctor_notes(dr_id, patient_id, note_id, subject, date, content) values (:1, :2, :3, )", rows)
    conn.commit()
    return render_template('provider/providerConfirmMsgSend.html', data=data, id_number=id_number)


@app.route('/providerNotes/<id_number>/<patient_id>', methods=["GET", "POST"])
def notesDr(id_number, patient_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from patients p where p.id_num = " + patient_id + ";")
    data = cur.fetchall()
    if request.method == 'POST':
        print("got into post")
        print(str(now))
        subject = str(request.values.get('patientSubject'))
        content = str(request.values.get('patientMessage'))
        note_id = random.randint(0, 1000000000000)
        cur.execute("INSERT INTO doctor_notes(dr_id, patient_id, note_id, subject, date, content) VALUES(1, " + str(id_number) + ", " + str(note_id) + ", '" + subject + "', '" + str(now) + "', '" + content + "');")
        conn.commit()
    return render_template('provider/providerNotes.html', data=data, id_number=id_number)


@app.route('/providerEntry/<id_number>/<patient_id>/')
def entryViewDr(id_number, patient_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from entries where patient_id = " + patient_id + ";")
    data = cur.fetchall()
    return render_template('provider/providerEntry.html', patient_id=patient_id, id_number=id_number, data=data)


@app.route('/patientMyDoctor')
def drP():
    return render_template('patient/patientMyDoctor.html')


@app.route('/patientHome/<id_num>', methods=["GET", "POST"])
def homeP(id_num):
    cur = conn.cursor()
    cur.execute("select * from entries where patient_id = ?", (id_num,))
    data = cur.fetchall()
    return render_template('patient/patientHome.html', data=data)


@app.route('/patientHome/edit/<id_num>')
def homeEditP(id_num):
    cur = conn.cursor()
    cur.execute("select * from entries where patient_id = ?", (id_num,))
    data = cur.fetchall()

    if request.method == 'POST':
        print('jasdoahgfiua')
        if request.form['add'] == 'sleep':
            hours = request.form["slhours"]
            cur.execute("update entries set sleep = ? where id_num = ?", (hours,id_num,))
            print("add success")
            return redirect(url_for('homeEditP', id_num=id_num))
    return render_template('patient/patientHomeEdit.html', data=data)


@app.route('/patientProfile')
def profileP():
    return render_template('patient/patientProfile.html')


@app.route('/patientProfile/edit')
def editP():
    return render_template('patient/patientProfileEdit.html')


@app.route('/sendMsg')
def msgP():
    return render_template('patient/patientSendMessage.html')

