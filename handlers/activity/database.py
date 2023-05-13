import sqlite3


def get_phones(link):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            phones = cur.execute(
                'SELECT phone FROM Phone INNER JOIN Phone_link ON Phone_link.id_phone = Phone.id '
                'INNER JOIN Link ON Phone_link.id_link = Link.id WHERE Link.link = ?',
                (link,))
            phone_list = []
            for phone in phones:
                phone_list.append(phone[0])
        return phone_list
    except Exception as e:
        print(f"Error getting phones by link from database: {e}")


def add_phone(phone):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            cur.execute('INSERT INTO Phone (phone) VALUES (?)', (phone,))
            print(f"Added data to database: phone={phone}")
    except Exception as e:
        print(f"Error adding data to database: {e}")


def add_link(link, phone):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            cur.execute('INSERT INTO Link (link) VALUES (?)', (link,))
            id_phone = cur.lastrowid
            id_link = cur.lastrowid
            cur.execute('INSERT INTO Phone_link (id_link, id_phone) VALUES (?, ?)', (id_link, id_phone))
            print(f"Added data to database: link={link}, phone={phone}")
    except Exception as e:
        print(f"Error adding data to database: {e}")


def delete_phone(link, phone):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            cur.execute('SELECT id_link, id_phone FROM Phone_link INNER JOIN Link ON Phone_link.id_link = Link.id '
                        'WHERE link = ? AND phone = ?', (link, phone))
            result = cur.fetchone()
            if result is not None:
                id_link, id_phone = result
                cur.execute('DELETE FROM Phone_link WHERE id_link = ? AND id_phone = ?', (id_link, id_phone))
                cur.execute('DELETE FROM Phone WHERE id = ?', (id_phone,))
                print(f"Deleted data from database: link={link}, phone={phone}")
            else:
                print(f"No matching data found in database: link={link}, phone={phone}")
    except Exception as e:
        print(f"Error deleting data from database: {e}")


def delete_link(link, phone):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            cur.execute('SELECT id_link, id_phone FROM Phone_link INNER JOIN Link ON Phone_link.id_link = Link.id '
                        'WHERE link = ? AND phone = ?', (link, phone))
            result = cur.fetchone()
            if result is not None:
                id_link, id_phone = result
                cur.execute('DELETE FROM Phone_link WHERE id_link = ? AND id_phone = ?', (id_link, id_phone))
                cur.execute('DELETE FROM Link WHERE id = ?', (id_link,))
                print(f"Deleted data from database: link={link}, phone={phone}")
            else:
                print(f"No matching data found in database: link={link}, phone={phone}")
    except Exception as e:
        print(f"Error deleting data from database: {e}")


def delete_phone_link(link, phone):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            cur.execute('SELECT id_link, id_phone FROM Phone_link INNER JOIN Link ON Phone_link.id_link = Link.id '
                        'WHERE link = ? AND phone = ?', (link, phone))
            result = cur.fetchone()
            if result is not None:
                id_link, id_phone = result
                cur.execute('DELETE FROM Phone_link WHERE id_link = ? AND id_phone = ?', (id_link, id_phone))
                print(f"Deleted data from database: link={link}, phone={phone}")
            else:
                print(f"No matching data found in database: link={link}, phone={phone}")
    except Exception as e:
        print(f"Error deleting data from database: {e}")
