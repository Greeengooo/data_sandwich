from flask import Flask
from flask import request
import pyodbc, pandas
from werkzeug.wrappers import response
from creds import Credentials
import json

app = Flask(__name__)

def connect():
    creds = Credentials()
    config = creds.get_creds()
    cnxn = pyodbc.connect(f"Driver={config['driver']};ConnectionType=Direct;HOST={config['host']};PORT={config['port']};AuthenticationType=Plain;UID={config['uid']};PWD={config['pwd']}", autocommit=True)
    return cnxn


@app.route('/')
def greet():
    cnxn = connect()
    return json.dumps({
                       'dbms-name': cnxn.getinfo(pyodbc.SQL_DBMS_NAME), 
                       'dbms-version': cnxn.getinfo(pyodbc.SQL_DBMS_VER),
                       'dbms-driver-name': cnxn.getinfo(pyodbc.SQL_DRIVER_NAME)
                     }) 

@app.route('/users')
def get_all_users():
    cnxn = connect()
    sql = '''SELECT * FROM snow.test.public.test'''
    user_df = pandas.read_sql(sql, cnxn)
    return user_df.to_html()


@app.route('/query')
def get_user_by_id():
    cnxn = connect()
    name = None
    surname = None
    args = request.args
    sql = f'''SELECT * FROM snow.test.public.test WHERE '''
    if args:
        if "name" in args:
            name = args["name"]
            sql += f"name=\'{name}\'"
        if "surname" in args:
            surname = args["surname"]
            sql += f"surname=\'{surname}\'"
    else:
        return "Status: 404 Not Found"
    user_df = pandas.read_sql(sql, cnxn)
    print(name, surname)
    return user_df.to_html()
