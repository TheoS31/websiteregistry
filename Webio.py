import pywebio
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import start_server, session
from pywebio import config
from pywebio.pin import *
from Functions import *
import argparse
import locale
from pywebio.platform.flask import webio_view
from flask import Flask
app = Flask(__name__)
cnx = mysql.connector.connect(user="j8gyaqvjcifzcpkb",
                              password="hs04c2hqym36w909",
                              host="n2o93bb1bwmn0zle.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
                              port=3306,
                              database="oit5yzwieqpr5ash")
cursor = cnx.cursor(buffered=True)

auth = False
verified = False
headers = [
           'ID',
           'Name of hiring passenger and phone number',
           'Date and time of the booking',
           'How the booking was received',
           'Driver and car',
           'Date and time of collection',
           'Address of collection',
           'Destination',
           'Price £']

index_style = """
#pywebio-scope-buttons button{
  height: 250px;
  width: 100%;
  position: relative;
  border: 3px solid black;
  top: 50%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
font-size: 5vw;
font-size:100px;
color: black;
background-color: orange;
}
"""
form_style = '''
#pywebio-scope-buttons button{
  width: 100%;
  position: relative;
color: black;
background-color: orange;
font-size: 30px;
}
'''
table_style = '''
#pywebio-scope-buttons button{
color: black;
background-color: orange;
border-color: black;
}
'''


@config(title='Main page',theme="dark",css_style=index_style)
def index():
    global auth
    global verified
    if not auth:
        while True:
            inputs = input_group('Login', [
                    input('Username',placeholder='Username', name='1',required=True),
                    input('Password',placeholder='Password',type=PASSWORD, name='2',required=True)])
            check = validate(inputs['1'], inputs['2'])
            if check[0]:
                auth = True
                break
            else:
                pass
    if check[1] == 'admin':
        verified = True
        with use_scope('buttons'):
            put_column([
            put_buttons(['Table'], [lambda: go_app('table',new_window=False)]),
            None,
            put_buttons(['Form'], [lambda: go_app('form',new_window=False)])
            ],size='50% 20px 50%')
    elif check[1] == 'guest':
        with use_scope('buttons'):
            put_column([None,put_buttons(['Table'], [lambda: go_app('table2', new_window=False)])],size='50% 50%')

@config(title='Table',theme="dark", css_style=table_style)
def table():
    global auth
    global verified
    if auth and verified:
        sql = "SELECT * FROM CURSE"
        cursor.execute(sql)
        while True:
            index_list = []
            result = cursor.fetchall()
            for i in range(len(result)):
                index_list.append(i)
            for i in range(len(result)):
                index_list[i] += 1

            with use_scope('result', clear=True):
                put_scrollable(put_table(tdata=result, header=headers), height=500, keep_bottom=True, border=False)
            with use_scope('buttons', clear=True):

                put_row([
                put_select('Select', options=index_list),
                put_button('Delete', onclick=delete)
                ])

                put_actions(name='Action', buttons=['Ascending', 'Descending','Refresh','Download PDF', 'Form', 'Logout'])
                changed = pin_wait_change('Action')
                if changed["value"] == 'Ascending':
                    sql = "SELECT * FROM CURSE ORDER BY ID ASC;"
                    cursor.execute(sql)
                    continue
                if changed["value"] == 'Descending':
                    sql = "SELECT * FROM CURSE ORDER BY ID DESC;"
                    cursor.execute(sql)
                    continue
                if changed["value"] == 'Refresh':
                    sql = "SELECT * FROM CURSE ORDER BY ID ASC;"
                    cursor.execute(sql)
                    continue
                if changed["value"] == 'Download PDF':
                    continue
                if changed["value"] == 'Form':
                    go_app('form', new_window=False)
                if changed["value"] == 'Logout':
                    auth = False
                    verified = False
                    go_app('index', new_window=False)
    elif auth and not verified:
        go_app('table2', new_window=False)
    else:
        go_app('index', new_window=False)

@config(title='Form',theme="dark",css_style=form_style)
def form():
    if auth and verified:
        with use_scope('buttons'):
            put_buttons(['Table'], [lambda: go_app('table',new_window=False)])
        while True:
            sql = "SELECT * FROM CURSE ORDER BY ID ASC;"
            cursor.execute(sql)
            val = []
            result = cursor.fetchall()
            inputs = input_group('Form', [
                    input('Name of hiring passenger and phone number', name='1',required=True),
                    input('Date and time of the booking', name='2',required=True),
                    input('How the booking was received', name='3',required=True),
                    input('Driver and car', name='4',required=True),
                    input('Date and time of collection', name='5',required=True),
                    input('Address of collection', name='6',required=True),
                    input('Destination', name='7',required=True),
                    input('Price £', name='8',required=True)])

            index = int(len(result)) + 1
            val.append(index)
            val.append(inputs['1'])
            val.append(inputs['2'])
            val.append(inputs['3'])
            val.append(inputs['4'])
            val.append(inputs['5'])
            val.append(inputs['6'])
            val.append(inputs['7'])
            val.append(inputs['8'])

            sql = "INSERT INTO CURSE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, val)
            cnx.commit()
            val.clear()
    elif auth and not verified:
        go_app('table2', new_window=False)
    else:
        go_app('index', new_window=False)


@config(title='Table',theme="dark", css_style=table_style)
def table2():
    global auth
    global verified
    sql = "SELECT * FROM CURSE"
    cursor.execute(sql)
    while True:
        result = cursor.fetchall()

        with use_scope('result', clear=True):
            put_scrollable(put_table(tdata=result, header=headers), height=500, keep_bottom=True, border=False)
        with use_scope('buttons', clear=True):

            put_actions(name='Action', buttons=['Ascending', 'Descending','Refresh','Download PDF', 'Logout'])
            changed = pin_wait_change('Action')
            if changed["value"] == 'Ascending':
                sql = "SELECT * FROM CURSE ORDER BY ID ASC;"
                cursor.execute(sql)
                continue
            if changed["value"] == 'Descending':
                sql = "SELECT * FROM CURSE ORDER BY ID DESC;"
                cursor.execute(sql)
                continue
            if changed["value"] == 'Refresh':
                sql = "SELECT * FROM CURSE ORDER BY ID ASC;"
                cursor.execute(sql)
                continue
            if changed["value"] == 'Download PDF':
                continue
            if changed["value"] == 'Logout':
                auth = False
                verified = False
                go_app('index', new_window=False)

def delete():
    cursor.execute("DELETE FROM CURSE WHERE id = %s", (pin.Select,))
    cnx.commit()
    drop = '''
        ALTER TABLE CURSE
        DROP COLUMN id;
        '''
    cursor.execute(drop)
    cnx.commit()
    cursor.execute("ALTER TABLE CURSE ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST")

    cnx.commit()
    run_js('window.location.reload()')

app.add_url_rule('/index', 'webio_view', webio_view(index),methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()
pywebio.start_server([index, table, table2, form], port=args.port)
