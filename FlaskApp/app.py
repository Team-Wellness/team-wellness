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

###

@app.route('/patientMyDoctor/<id_num>', methods = ['GET'])
def drP(id_num):
    # Data for doctor notes: take all messages for patient
    cur.execute("select * from doctor_notes where patient_id = " + id_num + ";")
    dNotes = cur.fetchall()
    dNotes = list(dNotes)
    print(dNotes)

    # Need to grab names of dcotors for each message
    notesInfo = []
    for doc_id in dNotes:
        doc_id = list(doc_id)
        cur.execute("select name from doctors where id_number = " + str(doc_id[0]) + ";")
        name = cur.fetchall()
        # Change dr's id field to dr's name
        doc_id[0] = name[0][0]
        notesInfo.append(doc_id)
    print(notesInfo)

    return render_template('patient/patientMyDoctor.html', notesInfo = notesInfo, id_num = id_num)


@app.route('/patientHome')
def homeP():
    return render_template('patient/patientHome.html')


@app.route('/patientHome/edit')
def homeEditP():
    return render_template('patient/patientHomeEdit.html')


@app.route('/patientProfile/<id_num>', methods=['GET'])
def profileP(id_num):
    cur.execute("select * from patients p where p.id_num = " + id_num +";")
    pInfo = cur.fetchall()
    pDocs = getDocInfo(id_num)

    return render_template('patient/patientProfile.html', pInfo = pInfo, pDocs = pDocs)


@app.route('/patientProfile/edit/<id_num>', methods=['GET', 'POST'])
def editP(id_num):
    cur.execute("select * from patients where id_num = " + id_num +";")
    pInfo = cur.fetchall()

    if request.method == 'POST':
        name = request.form['pName']
        if name == '': name = pInfo[0][3]
        age = request.form['pAge']
        if age == '': age = pInfo[0][4]
        birthday = request.form['pBirthday']
        if birthday == '': birthday = pInfo[0][5]
        sex = request.form['pGender']
        if sex == '': sex = pInfo[0][6]
        height = request.form['pHeight']
        if height == '': height = pInfo[0][7]
        weight = request.form['pWeight']
        if weight == '': weight = pInfo[0][8]
        print(name, age, birthday, sex, height, weight)
        cur.execute("update patients set name = ?, age = ?, birthday = ?, sex = ?, height = ?, weight = ? where id_num = ?", (name, age, birthday, sex, height, weight, id_num))
        conn.commit()

        cur.execute("select * from patients where id_num = " + id_num +";")
        pInfo = cur.fetchall()
        print("Information update, success!")
    return render_template('patient/patientProfileEdit.html', pInfo = pInfo)

@app.route('/sendMsg/<id_num>', methods=['Get', 'POST'])
def msgP(id_num):
    pDocs = getDocInfo(id_num)

    # Get message subject and body
    if request.method == 'POST':
        # Take data from form
        selectDoc = request.form['selectDoc']
        pSubject = request.form['pSubject']
        pMessage = request.form['pMessage']
        cur.execute("select date('now');")
        date = cur.fetchall()
        date = date[0][0]
        msg_id = random.randint(0, 10000)
        print(selectDoc, pSubject, pMessage, date)

        # Get Doc id
        for doc in pDocs:
            if doc[2] == selectDoc: docId = doc[3]
        #print(selectDoc, docId, msg_id)

        data = [id_num, str(docId), str(msg_id), date, pSubject, pMessage]
        #print(data)
        # Place message into messages table
        cur.executemany("insert into message(patient, dr, msg_id, day, subject, body) values (:1, :2, :3, :4, :5, :6);", [data])
        conn.commit()
        pDocs = getDocInfo(id_num)

    # Check if message was inputted
    #cur.execute("select * from message where patient = " + id_num + ";")
    #print(cur.fetchall())

    return render_template('patient/patientSendMessage.html', pDocs = pDocs)


# Function that returns an array of patient's doctors
def getDocInfo(patient_Id):
    # Grab all id numbers of patient's doctors
    cur.execute("select dr_id from relationships where patient_id =" + patient_Id + ";")
    drIds = cur.fetchall()

    i = 0
    pDocs = []
    # Go through list of ids and take dr's name
    for id in drIds:
        cur.execute("select * from doctors where id_number = " + str(id[0]) + ";")
        drInfo = cur.fetchall()
        pDocs.append(drInfo[0])

    return pDocs
