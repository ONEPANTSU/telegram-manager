import requests

from config import DATABASE_SERVER


def get_admin():
    json = requests.get(DATABASE_SERVER + "admins").json()
    admins = list(json.values())
    return admins


def get_phones(link):
    json = requests.get(DATABASE_SERVER + "phones", params={"link": link}).json()
    phones = list(json.values())
    return phones


def add_phone(phone):
    res = requests.post(DATABASE_SERVER + "phone", params={"phone": phone})
    print(res.text)


def add_link(link):
    res = requests.post(DATABASE_SERVER + "link", params={"link": link})
    print(res.text)


def add_phone_link(link, phone):
    res = requests.post(
        DATABASE_SERVER + "phone_link", params={"phone": phone, "link": link}
    )
    print(res.text)


def add_database(link, phone):
    add_phone(phone)
    add_link(link)
    add_phone_link(link, phone)


def delete_phone(link, phone):
    res = requests.delete(
        DATABASE_SERVER + "phone", params={"phone": phone, "link": link}
    )
    print(res.text)


def delete_link(link, phone):
    res = requests.delete(
        DATABASE_SERVER + "link", params={"phone": phone, "link": link}
    )
    print(res.text)


def delete_phone_link(link, phone):
    res = requests.delete(
        DATABASE_SERVER + "phone_link", params={"phone": phone, "link": link}
    )
    print(res.text)


def get_tasks():
    json = requests.get(DATABASE_SERVER + "tasks").json()
    tasks = list(json.values())
    return tasks


def get_task_by_id(id_task):
    json = requests.get(DATABASE_SERVER + "task", params={"id_task": id_task}).json()
    tasks = list(json.values())
    return tasks[0]


def get_phone_by_task(id_task):
    json = requests.get(
        DATABASE_SERVER + "phones_by_task", params={"id_task": id_task}
    ).json()
    phones = list(json.values())
    return phones


def add_task(accounts, count, timing):
    print(accounts)
    print(count)
    print(timing)
    res = requests.post(
        DATABASE_SERVER + "task",
        params={"accounts": accounts, "count": count, "timing": timing},
    ).json()
    print(res)
    id_task = res["id_task"]
    return id_task


def change_task_status(id_task, status):
    res = requests.put(
        DATABASE_SERVER + "task",
        params={"id_task": id_task, "status": status},
    )
    print(res.text)


def delete_task(id_task):
    res = requests.delete(DATABASE_SERVER + "task", params={"id_task": id_task})
    print(res.text)


def delete_task_phone(id_task, phone):
    res = requests.delete(
        DATABASE_SERVER + "task_phone", params={"id_task": id_task, "phone": phone}
    )
    print(res.text)


def count_task_phone(id_task):
    json = requests.get(
        DATABASE_SERVER + "task_phone", params={"id_task": id_task}
    ).json()
    print(json)
    res = list(json.values())
    return res
