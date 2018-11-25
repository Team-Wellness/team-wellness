# RxHelp

## What is this?
RxHelp aims to help patients manage their health easier and more efficiently by allowing for tracking of many attributes and access to a multitude of doctors.

## How to run it locally
1. Install Oracle DB, Python, and Flask
2. In the console, put yourself in the FlaskApp folder (team-wellness --> FlaskApp)
3. Run schema.sql in your database to create the relevant tables
4. In app.py, change the code so it matches your database account information
5. In your console, type "set FLASK_APP=app.py" without the quotations
6. (OPTIONAL) Type "set FLASK_DEBUG=true" without the quotations
7. Type "python -m flask run" without the quotations to run the application
8. In your brower, go to "127.0.0.1:500" without the quotations
