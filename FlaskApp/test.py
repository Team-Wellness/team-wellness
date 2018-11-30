import os
import cx_Oracle
import cgi
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import random

con = cx_Oracle.connect('abc/123 @127.0.0.1/XE')
print(con.version)
con.close()
