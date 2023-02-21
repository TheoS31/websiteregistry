import mysql.connector
import bcrypt

cnx = mysql.connector.connect(user="sql8599140",
                              password="xX7MgYR8Rz",
                              host="sql8.freemysqlhosting.net",
                              port=3306,
                              database="sql8599140")
cursor = cnx.cursor()
def reset():
    cursor.execute("DROP TABLE ACCOUNT")
    '''
    cursor.execute("CREATE TABLE CURSE(id INT AUTO_INCREMENT PRIMARY KEY,name_of_hiring_passenger_and_phone_number VARCHAR(255),date_and_time_of_the_booking VARCHAR(255),how_the_booking_was_received VARCHAR(255),driver_and_car VARCHAR(255),date_and_time_of_collection VARCHAR(255),address_of_collection VARCHAR(255),destination VARCHAR(255),price_£ VARCHAR(255));")
    '''
    cnx.commit()

def prints():
    cursor.execute("SELECT * FROM ACCOUNT")
    myresult = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    print(headers)
    for x in myresult:
        print(x)

def safety():
    cursor.execute("CREATE TABLE ACCOUNT(username VARCHAR(255),hash VARCHAR(255), type VARCHAR(255));")
    cnx.commit()

def populate():
    username = 'guest'
    password = "guestpassword"
    type = 'guest'
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
    values = [username,hashed, type]
    sql = "INSERT INTO ACCOUNT VALUES (%s, %s, %s)"
    cursor.execute(sql,values)
    cnx.commit()
def validate(name, password):
    try:
        sql = "SELECT * FROM ACCOUNT WHERE username = %s"
        cursor.execute(sql, (name,))
        password = password.encode('utf-8')
        match = cursor.fetchall()
        encoder = match[0][1]
        encoder = encoder.encode('utf-8')
        if bcrypt.checkpw(password, encoder):
            return True, match[0][2]
        else:
            return False, 'pass'
    except IndexError:
        return False, 'pass'
