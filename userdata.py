import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()

    def init_db(self, force: bool = False):
        with self.conn:
            if force:
                self.c.execute('DROP TABLE IF EXISTS user_data')
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS user_data (
                    id       INTEGER PRIMARY KEY,
                    user_id   INTEGER NOT NULL,
                    language TEXT    NOT NULL DEFAULT 'ukr',
                    list_0   TEXT    NOT NULL DEFAULT '',
                    list     TEXT    NOT NULL DEFAULT '',
                    time     TEXT    NOT NULL DEFAULT '',
                    set_time TEXT    NOT NULL DEFAULT '',
                    switch   INTEGER NOT NULL DEFAULT 0
                )
            ''')
            self.conn.commit()

    def add_user(self, user_id: int):
        with self.conn:
            exist = self.c.execute("SELECT language FROM user_data WHERE user_id = ?", (user_id,)).fetchone()
            if exist is not None:
                pass
            else:
                self.c.execute('INSERT INTO user_data (user_id) VALUES (?)', (user_id,))
                self.conn.commit()

    def change_language(self, user_id: int, language: str):
        with self.conn:
            self.c.execute('UPDATE user_data SET language = ? WHERE user_id = ?', (language, user_id))
            self.conn.commit()

    def change_list_0(self, user_id: int, list_0: str, target: str):
        with self.conn:
            list_ = str(self.c.execute('SELECT list_0 FROM user_data WHERE user_id = ?', (user_id,)).fetchone())
            list_ = list_[2:(len(list_) - 3)].split(" ")
            a = list(list_)
            if target == '+':
                a.append(list_0)
                list_ = tuple(a)
            else:
                if list_0 in a:
                    a.remove(list_0)
                    list_ = tuple(a)
            self.c.execute('UPDATE user_data SET list_0 = ? WHERE user_id = ?', (" ".join(list_), user_id))
            self.conn.commit()

    def change_list(self, user_id: int, new: str, target: str):
        with self.conn:
            list_ = str(self.c.execute('SELECT list FROM user_data WHERE user_id = ?', (user_id,)).fetchone())
            list_ = list_[2:(len(list_) - 3)].split(" ")
            a = list(list_)
            if target == '+':
                a.append(new)
                list_ = tuple(a)
            else:
                if new in a:
                    a.remove(new)
                    list_ = tuple(a)
            self.c.execute('UPDATE user_data SET list = ? WHERE user_id = ?', (" ".join(list_), user_id))
            self.conn.commit()

    def change_time(self, user_id: int, time: str):
        with self.conn:
            self.c.execute('UPDATE user_data SET time = ? WHERE user_id = ?', (time, user_id))
            self.conn.commit()

    def change_set_time(self, user_id: int, time: str):
        with self.conn:
            self.c.execute('UPDATE user_data SET set_time = ? WHERE user_id = ?', (time, user_id))
            self.conn.commit()

    def change_switch(self, user_id: int, target: int):
        with self.conn:
            self.c.execute('UPDATE user_data SET switch = ? WHERE user_id = ?', (target, user_id))
            self.conn.commit()

    def clear_data(self, user_id: int, target: str):
        with self.conn:
            if target == 'list_0':
                self.c.execute('UPDATE user_data SET list_0 = ? WHERE user_id = ?', ('', user_id))
                self.conn.commit()

    def get_data(self, user_id: int, target: str):
        with self.conn:
            self.c.execute('SELECT * FROM user_data WHERE user_id = ?', (user_id,))
            if target == 'user_id':
                return str(self.c.fetchone()[1])
            elif target == 'language':
                return str(self.c.fetchone()[2])
            elif target == 'list_0':
                return str(self.c.fetchone()[3]).split(" ")[1:]
            elif target == 'list':
                return str(self.c.fetchone()[4]).split(" ")[1:]
            elif target == 'full_list':
                a = str(self.c.fetchone()[4]).split(" ")[1:]
                full_list = ''
                for i in range(len(a)):
                    full_list = full_list + f'{a[i]}, '
                return full_list[:(len(full_list) - 2)]
            elif target == 'time':
                return str(self.c.fetchone()[5])
            elif target == 'set_time':
                return str(self.c.fetchone()[6])
            elif target == 'switch':
                return int(str(self.c.fetchone()[7]))

    def get_data_all(self):
        with self.conn:
            a = self.c.execute('SELECT user_id FROM user_data WHERE switch = 1').fetchone()
            if a is not None:
                list1 = []
                max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
                for i in range(1, max_id + 1):
                    if self.c.execute('SELECT switch FROM user_data WHERE id = ?', (i, )).fetchone()[0] == 1:
                        list1.append(self.c.execute('SELECT user_id FROM user_data WHERE id = ?', (i, )).fetchone()[0])
                return list1
            else:
                return 0
