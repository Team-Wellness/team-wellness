from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask.ext.mysql import MySQL

import mysql.connector

try:
    import configparser
except:
    from six.moves import configparser


# if __name__ == "__main__":
#     app.run()

# mysql = MySQL()
app = Flask(__name__)
# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
# app.config['MYSQL_DATABASE_DB'] = 'teamwellness'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
#
# conn = mysql.connect()
# cursor = conn.cursor()

@app.route("/")
def main():
    return render_template('index.html')


@app.route('/providerHome')
def homeDr():
    return render_template('provider/providerHome.html')


@app.route('/providerAdd')
def addDr():
    return render_template('provider/providerAdd.html')


@app.route('/providerEntry')
def entryDr():
    return render_template('provider/providerEntry.html')


@app.route('/providerMessages')
def msgDr():

    return render_template('provider/providerMessages.html')


@app.route('/providerNotes', methods=["GET", "POST"])
def notesDr():
    cur = mysql.connection.cursor()
    cur.execute('''select * from messages''')
    data = cur.fetchall()
    return render_template('provider/providerNotes.html', data=data)

###

@app.route('/patientMyDoctor')
def drP():
    return render_template('patient/patientMyDoctor.html')


@app.route('/patientHome')
def homeP():
    return render_template('patient/patientHome.html')


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