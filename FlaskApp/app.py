from flask import Flask, request, session, g, redirect, url_for, abort, request, render_template, flash
import random
from flask_login import LoginManager
from flask_simplelogin import SimpleLogin
import sqlite3

app = Flask(__name__) # create the application instance
SimpleLogin(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

conn = sqlite3.connect('database.db', check_same_thread=False)
print("Opened database successfully")
# Login stuff
# login_manager = LoginManager()
# login_manager.init_app(app)

cur = conn.cursor()


#login; currently only works with providers
@app.route("/", methods=['GET', 'POST'])
def main():
    error = 'none';
    cur = conn.cursor()
    if request.method == 'POST':
        if request.form['loginType'] == 'p':
            usernameP = request.form['usernameP']
            passwordP = request.form['passwordP']
            cur.execute("select id_num from patients where username = ? and password = ?", (usernameP, passwordP,))
            if cur.fetchone() is not None:
                return redirect(url_for('homeP')) # Redirect to patient home
            else:
                error == 'Could not find account using email or password'
        elif request.form['loginType'] == 'd':
            usernameDr = request.form['usernameDr']
            passwordDr = request.form['passwordDr']
            cur.execute("select id_number from doctors where username = ? and password = ?", (usernameDr,passwordDr,))
            if cur.fetchone() is not None:
                return redirect(url_for('homeDr'))  # Redirect to provider home
            else:
                error == 'Could not find account using email or password'
    return render_template('index.html')

@app.route('/providerHome')
def homeDr():
    cur = conn.cursor()
    cur.execute("select * from patients where id_num in (select patient_id from relationships)") # who exist in the relationships table
    data = cur.fetchall()
    return render_template('provider/providerHome.html', data=data)


@app.route('/providerAdd')
def addDr():
    cur = conn.cursor()
    cur.execute("select * from patients p where not exists (select * from relationships r where p.id_num = r.patient_id)")
    data = cur.fetchall()
    return render_template('provider/providerAdd.html', data=data)


@app.route('/providerConfirm/<testVar>', methods=['GET', 'POST'])
def confirmAddDr(testVar):
    global relationship_id, dr_id, patient_id
    cur = conn.cursor()
    cur.execute("select * from patients p where p.id_num ==" + testVar + ";")
    data = cur.fetchall()
    relationship_id = random.randint(0, 10000)
    dr_id = 1;
    patient_id = testVar;
    rows = [(dr_id, patient_id, relationship_id)]
    # cur.bindarraysize = 1
    cur.setinputsizes(int, int, int)
    cur.executemany("insert into relationships(dr_id, patient_id, relationship_id) values (:1, :2, :3)", rows)
    conn.commit()
    print("success!")
    return render_template('provider/providerConfirm.html', data=data)


@app.route('/providerDeleteConfirm/<testVar>', methods=['GET', 'POST'])
def confirmDeleteDr(testVar):
    cur = conn.cursor()
    cur.execute("select * from patients p where p.id_num ==" + testVar + ";")
    data = cur.fetchall();
    patient_id = testVar
    cur.setinputsizes(int)
    cur.execute("delete from relationships where patient_id = " + patient_id + ";")
    conn.commit()
    print("Success!")
    return render_template('provider/providerDeleteConfirm.html', data=data)


@app.route('/providerEntry/<id_num>')
def entryDr(id_num):

    return render_template('provider/providerEntry.html')


@app.route('/providerMessages')
def msgDr():

    return render_template('provider/providerMessages.html')


@app.route('/providerNotes/<id_num>', methods=["GET", "POST"])
def notesDr(id_num):
    cur = conn.cursor()
    cur.execute("select * from patients p where p.id_num = " + id_num + ";")
    data = cur.fetchall();
    return render_template('provider/providerNotes.html', data=data)



@app.route('/patientMyDoctor')
def drP():
    return render_template('patient/patientMyDoctor.html')


@app.route('/patientHome')
def homeP():
    cur = conn.cursor()
    cur.execute("select * from entries where patient_id in (select id_num from patients)")
    data = cur.fetchall()
    return render_template('patient/patientHome.html', data=data)

@app.route('/patientHome/edit')
def homeEditP():
    return render_template('patient/patientHomeEdit.html')


@app.route('/patientProfile')
def profileP():
    return render_template('patient/patientProfile.html')


@app.route('/patientProfile/edit')
def editP():
    return render_template('patient/patientProfileEdit.html')


@app.route('/sendMsg')
def msgP():
    return render_template('patient/patientSendMessage.html')

@app.route('/viewEntry')
def entryViewDr():
    return render_template('provider/providerEntry.html')


@app.route('/enterNotes')
def notesEnterDr():
    return render_template('provider/providerNotes.html')
