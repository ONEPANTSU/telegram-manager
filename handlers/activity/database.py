import sqlite3


def get_admin():
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            admins = cur.execute(
                'SELECT name FROM Admin')
            admin_list = []
            for admin in admins:
                admin_list.append(admin[0])
        return admin_list
    except Exception as e:
        print(f"Error getting admins by link from database: {e}")


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
            # Проверяем, есть ли такой телефон уже в базе данных
            cur.execute('SELECT phone FROM Phone WHERE phone=?', (phone,))
            row = cur.fetchone()
            if row is None:
                # Если телефон не найден, то добавляем его в базу данных
                cur.execute('INSERT INTO Phone (phone) VALUES (?)', (phone,))
                print(f"Added data to database: phone={phone}")
            else:
                # Если телефон уже есть в базе данных, то выводим сообщение об ошибке
                print("This phone number already exists in the database.")
    except Exception as e:
        print(f"Error adding data to database: {e}")


def add_link(link):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            # Проверяем, есть ли такая ссылка уже в базе данных
            cur.execute('SELECT link FROM Link WHERE link=?', (link,))
            row = cur.fetchone()
            if row is None:
                cur.execute('INSERT INTO Link (link) VALUES (?)', (link,))
            else:
                # Если ссылка уже есть в базе данных, то выводим сообщение об ошибке
                print("This link already exists in the database.")
    except Exception as e:
        print(f"Error adding data to database: {e}")


def add_phone_link(link, phone):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            # Проверяем, есть ли такой телефон и ссылка в базе данных
            cur.execute('SELECT id_link, id_phone FROM Phone_link '
                        'INNER JOIN Phone ON Phone_link.id_phone = Phone.id '
                        'INNER JOIN Link ON Phone_link.id_link = Link.id '
                        'WHERE link = ? AND phone = ?', (link, phone))
            result = cur.fetchone()

            if result is not None:
                # Если телефон и ссылка уже есть в базе данных, то выводим сообщение об ошибке
                print("This phone number is already linked to this link.")
            else:
                # Если телефон и ссылка не найдены в базе данных, то добавляем их
                cur.execute('SELECT id FROM Phone WHERE phone=?', (phone,))
                phone_id = cur.fetchone()[0]

                cur.execute('SELECT id FROM Link WHERE link=?', (link,))
                link_id = cur.fetchone()[0]

                cur.execute('INSERT INTO Phone_link (id_link, id_phone) VALUES (?, ?)', (link_id, phone_id))
                print(f"Added data to database: link={link}, phone={phone}")
    except Exception as e:
        print(f"Error adding data to database: {e}")


def add_database(link, phone):
    add_phone(phone)
    add_link(link)
    add_phone_link(link, phone)


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
            cur.execute('SELECT id_link, id_phone FROM Phone_link '
                        'INNER JOIN Phone ON Phone_link.id_phone = Phone.id '
                        'INNER JOIN Link ON Phone_link.id_link = Link.id '
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
            # Проверяем, есть ли данная связка телефона и ссылки в базе данных
            cur.execute(
                'SELECT id_link, id_phone FROM Phone_link '
                'INNER JOIN Phone ON Phone_link.id_phone = Phone.id '
                'INNER JOIN Link ON Phone_link.id_link = Link.id '
                'WHERE link = ? AND phone = ?',
                (link, phone))
            result = cur.fetchone()
            if result is not None:
                id_link, id_phone = result
                # Удаляем связь между телефоном и ссылкой
                cur.execute('DELETE FROM Phone_link WHERE id_link = ? AND id_phone = ?', (id_link, id_phone))
                # Проверяем, сколько телефонов еще связаны с этой ссылкой
                cur.execute('SELECT COUNT(*) FROM Phone_link WHERE id_link = ?', (id_link,))
                count = cur.fetchone()[0]
                if count == 0:
                    # Если больше ни один телефон не связан с этой ссылкой, то удаляем саму ссылку
                    cur.execute('DELETE FROM Link WHERE id = ?', (id_link,))
                    print(f"Deleted link from database: {link}")
                print(f"Deleted phone from database: {phone}")
            else:
                print(f"No matching data found in database: link={link}, phone={phone}")
    except Exception as e:
        print(f"Error deleting data from database: {e}")


def get_task():
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            cur.execute(
                'SELECT id, data_time FROM Task WHERE status = 1')
            result = cur.fetchone()
            if result is not None:
                return result
            else:
                print(f"No matching data found in database")
    except Exception as e:
        print(f"Error getting task from database: {e}")


def get_phone_by_task(id_task):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            cur.execute(
                'SELECT phone FROM Phone '
                'INNER JOIN Task_phone ON Phone.id = Task_phone.id_phone '
                'WHERE Task_phone.id_task = ?', id_task)
            result = cur.fetchone()
            if result is not None:
                return result
            else:
                print(f"No matching data found in database")
    except Exception as e:
        print(f"Error getting task from database: {e}")


def add_task(accounts, count, timing):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            status = 1
            cur = con.cursor()
            cur.execute('INSERT INTO Task (count, status, timing) VALUES (?, ?, ?)', (count, status, timing))
            id_task = cur.lastrowid
            for phone in accounts:
                phones = cur.execute(
                    'SELECT id FROM Phone WHERE phone = ?',
                    (phone,))
            for id_phone in phones:
                cur.execute('INSERT INTO Task_phone (id_task, id_phone) VALUES (?, ?)', (id_task, id_phone))
            print(f"Added task to database")
        return id_task
    except Exception as e:
        print(f"Error adding data to database: {e}")


def change_task_status(id_task):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            cur.execute('UPDATE Task SET status = 0 WHERE id = ?', (id_task,))
            print(f"Changed status in database: id_task={id_task}")
    except Exception as e:
        print(f"Error changing status in database: {e}")


def delete_task(id_tasks):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            for id_task in id_tasks:
                cur.execute('SELECT id FROM Task WHERE id = ? ', (id_task, ))
            result = cur.fetchone()
            if result is not None:
                id_task = result
                cur.execute('DELETE FROM Task WHERE id = ?', id_task)
                print(f"Deleted data from database: id_task={id_task}")
            else:
                print(f"No matching data found in database: id_task={id_task}")
    except Exception as e:
        print(f"Error deleting data from database: {e}")


def delete_task_phone(id_task, phone):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            id_phone = cur.execute(
                'SELECT id FROM Phone '
                'INNER JOIN Phone_link ON Phone.id = Phone_link.id_phone '
                'WHERE phone = ?',
                (phone,))
            cur.execute('DELETE FROM Task_phone WHERE id_task = ? AND id_phone = ?', (id_task, id_phone))
            print(f"Deleted data from database: id_task={id_task}")

    except Exception as e:
        print(f"Error deleting data from database: {e}")


def count_task_phone(id_task):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            remaining_rows = cur.execute('SELECT COUNT(*) FROM Task_phone WHERE id_task = ?', (id_task,)).fetchone()[0]
            print(f"Number of remaining rows in Task_phone with id_task {id_task}: {remaining_rows}")

    except Exception as e:
        print(f"Error deleting data from database: {e}")
