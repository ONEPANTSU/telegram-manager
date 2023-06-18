from random import shuffle

import requests

from config import DATABASE_SERVER
from useful.instruments import logger


@logger.catch
def get_admin():
    json = requests.get(DATABASE_SERVER + "admins").json()
    admins = list(json.values())
    logger.info(f"Get Admins Request: {len(admins)}")
    return admins


@logger.catch
def get_phones(link):
    json = requests.get(DATABASE_SERVER + "phones", params={"link": link}).json()
    phones = list(json.values())
    logger.info(f"Get Phones By {link} Request: {len(phones)}")
    return phones


@logger.catch
def add_phone(phone):
    res = requests.post(DATABASE_SERVER + "phone", params={"phone": phone})
    logger.info(f"Add Phone ({phone}) Request: {res.text}")


@logger.catch
def add_link(link):
    res = requests.post(DATABASE_SERVER + "link", params={"link": link})
    logger.info(f"Add Link ({link}) Request: {res.text}")


@logger.catch
def add_phone_link(link, phone):
    res = requests.post(
        DATABASE_SERVER + "phone_link", params={"phone": phone, "link": link}
    )
    logger.info(f"Add Phone_Link ({phone} - {link}) Request: {res.text}")


@logger.catch
def add_database(link, phone):
    add_phone(phone)
    add_link(link)
    add_phone_link(link, phone)


@logger.catch
def delete_phone(link, phone):
    res = requests.delete(
        DATABASE_SERVER + "phone", params={"phone": phone, "link": link}
    )
    logger.info(f"Delete Phone ({phone} - {link}) Request: {res.text}")


@logger.catch
def delete_link(link, phone):
    res = requests.delete(
        DATABASE_SERVER + "link", params={"phone": phone, "link": link}
    )
    logger.info(f"Delete Link ({phone} - {link}) Request: {res.text}")


@logger.catch
def delete_phone_link(link, phone):
    res = requests.delete(
        DATABASE_SERVER + "phone_link", params={"phone": phone, "link": link}
    )
    logger.info(f"Delete Phone Link ({phone} - {link}) Request: {res.text}")


@logger.catch
def get_tasks():
    json = requests.get(DATABASE_SERVER + "tasks").json()
    tasks = list(json.values())
    logger.info(f"Get Tasks Request: {len(tasks)}")
    return tasks


@logger.catch
def get_task_by_id(id_task):
    json = requests.get(DATABASE_SERVER + "task", params={"id_task": id_task}).json()
    tasks = list(json.values())
    logger.info(f"Get Tasks By Id (#{id_task}) Request: {tasks}")
    return tasks[0]


@logger.catch
def get_phone_by_task(id_task):
    json = requests.get(
        DATABASE_SERVER + "phones_by_task", params={"id_task": id_task}
    ).json()
    phones = list(json.values())
    shuffle(phones)
    logger.info(f"Get Phones By Task (#{id_task}) Request: {len(phones)}")
    return phones


@logger.catch
def add_task(accounts, count, timing):
    accounts_dict = {}
    iteration = 0
    for account in accounts:
        accounts_dict[str(iteration)] = account
        iteration += 1
    res = requests.post(
        DATABASE_SERVER + "task",
        params={"accounts": str(accounts_dict), "count": count, "timing": str(timing)},
    ).json()
    id_task = res["id_task"]
    logger.info(f"Add Task (#{id_task}) Request: {res.text}")
    return id_task


@logger.catch
def change_task_status(id_task, status):
    res = requests.put(
        DATABASE_SERVER + "task",
        params={"id_task": id_task, "status": status},
    )
    logger.info(f"Change Task Status (#{id_task} - {status}) Request: {res.text}")


@logger.catch
def delete_task(id_task):
    try:
        res = requests.delete(DATABASE_SERVER + "task", params={"id_task": id_task})
        logger.info(f"Delete Task (#{id_task}) Request: {res.text}")
    except Exception as e:
        logger.error(f"Delete Task (#{id_task}) Error: {e}")


@logger.catch
def delete_task_phone(id_task, phone):
    res = requests.delete(
        DATABASE_SERVER + "task_phone", params={"id_task": id_task, "phone": phone}
    )
    logger.info(f"Delete Task_Phone (#{id_task} - {phone}) Request: {res.text}")


@logger.catch
def count_task_phone(id_task):
    json = requests.get(
        DATABASE_SERVER + "task_phone", params={"id_task": id_task}
    ).json()
    res = list(json.values())[0]
    logger.info(f"Count Task_Phone (#{id_task}) Request: {res}")
    return res
