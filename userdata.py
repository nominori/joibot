import sqlite3


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS user_data')
        c.execute('DROP TABLE IF EXISTS user_data_details')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            language    TEXT NOT NULL,
            list_0      TEXT NOT NULL,
            list        TEXT NOT NULL,
            time        TEXT NOT NULL
        )
    ''')
    conn.commit()
    c.execute('''
            CREATE TABLE IF NOT EXISTS user_data_details (
                id          INTEGER PRIMARY KEY,
                user_id     INTEGER NOT NULL,
                user_name   TEXT NOT NULL,
                command     TEXT NOT NULL,
                time        TEXT NOT NULL
            )
        ''')
    conn.commit()


@ensure_connection
def add_user(conn, user_id: int):
    c = conn.cursor()
    exist = c.execute("SELECT language FROM user_data WHERE user_id = ?", (user_id,)).fetchone()
    if exist is not None:
        pass
    else:
        c.execute('INSERT INTO user_data (user_id, language, list_0, list, time) VALUES (?, ?, ?, ?, ?)',
                  (user_id, 'eng', '', '', ''))
        conn.commit()


@ensure_connection
def add_user_detail(conn, user_id: int, user_username: str, command: str, time_: str):
    c = conn.cursor()
    c.execute('INSERT INTO user_data_details (user_id, user_name, command, time) VALUES (?, ?, ?, ?)', (user_id, user_username, command, time_))
    conn.commit()


@ensure_connection
def change_language(conn, user_id: int, language: str):
    c = conn.cursor()
    c.execute('UPDATE user_data SET language = ? WHERE user_id = ?', (language, user_id))
    conn.commit()


@ensure_connection
def change_list_0(conn, user_id: int, list_0: str, target: str):
    c = conn.cursor()
    list_ = str(c.execute('SELECT list_0 FROM user_data WHERE user_id = ?', (user_id,)).fetchone())
    list_ = list_[2:(len(list_)-3)].split(" ")
    a = list(list_)
    if target == '+':
        a.append(list_0)
        list_ = tuple(a)
    else:
        if list_0 in a:
            a.remove(list_0)
            list_ = tuple(a)
    c.execute('UPDATE user_data SET list_0 = ? WHERE user_id = ?', (" ".join(list_), user_id))
    conn.commit()


@ensure_connection
def change_list(conn, user_id: int, new: str, target: str):
    c = conn.cursor()
    list_ = str(c.execute('SELECT list FROM user_data WHERE user_id = ?', (user_id,)).fetchone())
    list_ = list_[2:(len(list_)-3)].split(" ")
    a = list(list_)
    if target == '+':
        a.append(new)
        list_ = tuple(a)
    else:
        if new in a:
            a.remove(new)
            list_ = tuple(a)
    c.execute('UPDATE user_data SET list = ? WHERE user_id = ?', (" ".join(list_), user_id))
    conn.commit()


@ensure_connection
def change_time(conn, user_id: int, time: str):
    c = conn.cursor()
    c.execute('UPDATE user_data SET time = ? WHERE user_id = ?', (time, user_id))
    conn.commit()


@ensure_connection
def clear_detail(conn):
    c = conn.cursor()
    c.execute('DELETE FROM user_data_details')
    conn.commit()


@ensure_connection
def clear_data(conn, user_id: int, target: str):
    c = conn.cursor()
    if target == 'list_0':
        c.execute('UPDATE user_data SET list_0 = ? WHERE user_id = ?', ('', user_id))
    if target == 'list':
        c.execute('UPDATE user_data SET list = ? WHERE user_id = ?', ('', user_id))
    if target == 'time':
        c.execute('UPDATE user_data SET time = ? WHERE user_id = ?', ('', user_id))
    conn.commit()


@ensure_connection
def get_data(conn, user_id: int, target: str):
    c = conn.cursor()
    c.execute('SELECT language, list_0, list, time FROM user_data WHERE user_id = ?', (user_id,))
    if target == 'language':
        return str(c.fetchone()[0])
    elif target == 'list_0':
        return str(c.fetchone()[1]).split(" ")[1:]
    elif target == 'list':
        return str(c.fetchone()[2]).split(" ")[1:]
    elif target == 'full_list':
        a = str(c.fetchone()[2]).split(" ")[1:]
        full_list = ''
        for i in range(len(a)):
            full_list = full_list + f'{a[i]}, '
        return full_list[:(len(full_list)-2)]
    elif target == 'time':
        return str(c.fetchone()[3])
