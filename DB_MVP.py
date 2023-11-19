import sqlite3

connect = sqlite3.connect('db_mvp.db')
cursor = connect.cursor()

def check_isheadman(token='token'):
    cursor.execute(f'''
        SELECT isheadman FROM USERS WHERE tgtoken='{token}';
    ''')
    connect.commit()
    return cursor.fetchall()[0][0]
# return = 0/1

def get_info(date):
    all_info = []
    cursor.execute(f'''
        SELECT info FROM INFO WHERE date='{date}';
    ''')
    connect.commit()
    for i in cursor.fetchall():
        all_info.append(i[0])
    return all_info
# all_info = [info1, info2, info3 ... ]

def add_info(token, date, info):
    if check_isheadman(token) == 0:
        return False
    else:
        cursor.execute(f'''
            INSERT INTO INFO(date, info) VALUES('{date}', '{info}');
        ''')
        connect.commit()

def delete_info(token, date):
    if check_isheadman(token) == 0:
        return False
    else:
        cursor.execute(f'''
                DELETE FROM INFO WHERE date='{date}';
            ''')
        connect.commit()

