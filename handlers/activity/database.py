import sqlite3


def get_phones(link):
    with sqlite3.connect("TelegramManager.db") as con:
        cursor = con.cursor()
        phones = cursor.execute("SELECT phone FROM Bot WHERE link = ?", (link,))
        phone_list = []
        for phone in phones:
            phone_list.append(phone[0])
    return phone_list


def add_phone(link, phone):
    try:
        with sqlite3.connect("TelegramManager.db") as con:
            cur = con.cursor()
            cur.execute('INSERT INTO Bot (link, phone) VALUES (?, ?)', (link, phone))
            print(f"Added data to database: link={link}, phone={phone}")
    except Exception as e:
        print(f"Error adding data to database: {e}")


def delete_phone(link, phone):
    with sqlite3.connect("TelegramManager.db") as con:
        cursor = con.cursor()
        cursor.execute('DELETE FROM Bot WHERE link=? AND phone=?', (link, phone,))


def delete_link(link):
    with sqlite3.connect("TelegramManager.db") as con:
        cursor = con.cursor()
        cursor.execute('DELETE FROM Bot WHERE link=?', (link, ))
