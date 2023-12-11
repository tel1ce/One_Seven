import sqlite3

connect = sqlite3.connect('db_mvp.db')
cursor = connect.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS INFO(
                date CHAR,
                info CHAR
            );
        ''')
connect.commit()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS PRIVATE_INFO(
                tgtoken STR,
                date CHAR,
                info CHAR
            );
        ''')
connect.commit()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS USERS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tgtoken STR,
                isheadman INT
            );
        ''')
connect.commit()

def update_counter():
    counter = 0
    with open('counter.txt', 'r') as r:
        counter = r.readline()
        counter = int(counter.strip())
        counter += 1

        with open('counter.txt', 'w') as w:
            w.write(str(counter))

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
    result = cursor.fetchall()
    if result != []:
        return result[0][0]
    else:
        return None

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

def delete_private_info(token, date):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute(f'''
            DELETE FROM PRIVATE_INFO WHERE date='{date}' and tgtoken='{str(token)}';
        ''')
    connect.commit()

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

def check_user(tg):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute('SELECT tgtoken FROM USERS')
    connect.commit()
    result = cursor.fetchall()
    if result != []:
        for i in result:
            if str(i[0]) == str(tg):
                return 0
            else:
                if i == result[-1]:
                    return 1
    else:
        return 1

def is_have_info(token, date):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    n = 0
    cursor.execute(f'''
        SELECT info FROM INFO WHERE date='{date}';
    ''')
    connect.commit()
    if cursor.fetchall() != []: n+=1

    cursor.execute(f'''
            SELECT info FROM PRIVATE_INFO WHERE date='{date}' AND tgtoken='{str(token)}';
        ''')
    connect.commit()
    if cursor.fetchall() != []: n += 1

    if n == 0: return False
    else: return True

def add_private_info(token, date, info):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute(f'''
        INSERT INTO PRIVATE_INFO(tgtoken, date, info) VALUES('{token}', '{date}', '{info}');
    ''')
    connect.commit()

def get_private_info(token, date):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    all_info = []
    cursor.execute(f'''
        SELECT info FROM PRIVATE_INFO WHERE tgtoken='{str(token)}' AND date='{date}';
    ''')
    connect.commit()
    for i in cursor.fetchall():
        all_info.append(i[0])

    if len(all_info) != 0:
        return all_info
    else:
        return False\

def change_private_info(token, date, info):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    cursor.execute(f'''
            DELETE FROM PRIVATE_INFO WHERE tgtoken='{str(token)}' AND date='{date}';
        ''')
    connect.commit()

    cursor.execute(f'''
                INSERT INTO PRIVATE_INFO(tgtoken, date, info) VALUES('{str(token)}', '{date}', '{info}');
            ''')
    connect.commit()

def change_public_info(token, date, info):
    connect = sqlite3.connect('db_mvp.db')
    cursor = connect.cursor()
    if check_isheadman(token) == 0:
        return False
    else:
        cursor.execute(f'''
                    DELETE FROM INFO WHERE date='{date}';
                ''')
        connect.commit()

        cursor.execute(f'''
                        INSERT INTO INFO(date, info) VALUES('{date}', '{info}');
                    ''')
        connect.commit()
