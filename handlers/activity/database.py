import sqlite3


def get_phones(link):
    con = sqlite3.connect("TelegramManager.db")
    cursor = con.cursor()
    phones = cursor.execute("SELECT phone FROM Bot WHERE link = '{}'".format(link))
    phone_list = []
    for phone in phones:
        phone_list.append(phone[0])
    con.close()
    return phone_list


def add_phones(link, phone):
    con = sqlite3.connect("TelegramManager.db")
    cursor = con.cursor()
    con.executemany('INSERT INTO orders (link, phone) values(?, ?)', [link, phone])
    con.close()


def delete_phones(link, phone):
    con = sqlite3.connect("TelegramManager.db")
    cursor = con.cursor()
    cursor.execute('DELETE FROM Bot WHERE link=? AND phone=?', [link, phone])
    con.commit()
    con.close()
