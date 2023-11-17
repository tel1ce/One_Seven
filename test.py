import sqlite3, random

connect = sqlite3.connect('db_mvp.db')
cursor = connect.cursor()

def add_user(token='token', isheadman=0):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute(
        f'INSERT INTO USERS(tgtoken, isheadman) VALUES(?, ?)', (token, isheadman)
    )
    connect.commit()

def delete_user(token='token'):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute(f'''
        DELETE FROM USERS WHERE tgtoken='{token}';
    ''')
    connect.commit()

def delete_all_users():
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute('''
        DELETE FROM USERS;
    ''')
    connect.commit()

def check_isheadman(token='token'):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute(f'''
        SELECT isheadman FROM USERS WHERE tgtoken='{str(token)}';
    ''')
    connect.commit()
    return cursor.fetchall()[0][0]

#______________________________________________________               INFO

def add_info_test(date='01.01.0001', info='info'):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute(f'''
        INSERT INTO INFO(date, info) VALUES('{date}', '{info}');
    ''')
    connect.commit()

def get_info(date):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    all_info = []
    cursor.execute(f'''
        SELECT info FROM INFO WHERE date='{date}';
    ''')
    connect.commit()
    for i in cursor.fetchall():
        all_info.append(i[0])

    if len(all_info) != 0:
        return all_info
    else:
        return False


# print(get_info('17.11.2023'))


def add_info(token, date, info):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    if check_isheadman(token) == 0:
        return False
    else:
        cursor.execute(f'''
            INSERT INTO INFO(date, info) VALUES('{date}', '{info}');
        ''')
        connect.commit()

def delete_info_test(date='01.01.0001'):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute(f'''
        DELETE FROM INFO WHERE date='{date}';
    ''')
    connect.commit()

def delete_all_info():
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute('''
        DELETE FROM INFO;
    ''')
    connect.commit()

def delete_info(token, date):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    if check_isheadman(token) == 0:
        return False
    else:
        cursor.execute(f'''
                DELETE FROM INFO WHERE date='{date}';
            ''')
        connect.commit()

#_____________________________________________________

def recreate_table(USERS=0, INFO=0):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    if USERS == 1:
        cursor.execute('''
            DROP TABLE USERS;
        ''')
        connect.commit()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS USERS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tgtoken CHAR,
                isheadman INT
            );
        ''')
        connect.commit()

    elif INFO == 1:
        cursor.execute('''
            DROP TABLE INFO;
        ''')
        connect.commit()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS INFO(
                date CHAR,
                info CHAR
            );
        ''')
        connect.commit()

# def check_user_in_db(user_id):
#     connect = sqlite3.connect('db_mvp.db')
#     cursor = connect.cursor()
#     print(user_id)
#     cursor.execute(f'''
#         SELECT id FROM USERS WHERE tgtoken='{str(user_id)}';
#     ''')
#     connect.commit()
#     print(111)
#     if cursor.fetchone() is None:
#         return 0
#     else:
#         return 1







# cursor.execute('''
#             CREATE TABLE IF NOT EXISTS INFO(
#                 date CHAR,
#                 info CHAR
#             );
#         ''')
# connect.commit()
#
# cursor.execute('''
#             CREATE TABLE IF NOT EXISTS USERS(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 tgtoken CHAR,
#                 isheadman INT
#             );
#         ''')
# connect.commit()





def check_user(tg):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute('SELECT tgtoken FROM USERS')
    connect.commit()
    result = cursor.fetchall()
    for i in result:
        if i[0] == str(tg):
            return 0
        else:
            if i == result[-1]:
                return 1

# print(check_user('1195917490'))