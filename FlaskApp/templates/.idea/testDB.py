import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="username",
    passwd="password"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)