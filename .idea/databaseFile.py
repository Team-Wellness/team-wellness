import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="username",
    passwd="password"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")