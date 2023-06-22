![TelegramManager Bot](/src/tgm_logo.svg)
___
🤖 Telegram Manager is an aiogram-based project that provides a Telegram bot designed to manage activity within Telegram channels. The bot allows users to add bot accounts that will perform various tasks, such as subscribing, unsubscribing, viewing posts, and clicking on inline buttons within the channel.

💪 With Telegram Manager, users can easily automate their channel management process by setting task schedules for bot accounts. Users can set how many subscriptions or unsubscriptions occur per hour, control the frequency of post views and click actions, and manage all tasks with ease. In addition, the bot enables users to pause, resume, and delete tasks at any time.

🚀 Overall, Telegram Manager is a powerful tool for those looking to enhance their Telegram channel's performance through automated management techniques.

## Features

- [X] Creating bot accounts to perform tasks in the channel 🤖
- [X] Setting task schedules for bot accounts 🔧
- [X] Automatic subscription and unsubscription from the channel 📈
- [X] Viewing posts and clicking on buttons within the channel ⭕
- [X] Ability to manage task frequency, pause, resume, and delete tasks at any time ⏯️

## Installation
1. Clone the repository: 
```
git clone https://github.com/ONEPANTSU/TelegramManager.git
```
2. Install the requirements:
```
pip install -r requirements.txt
```
3. Replace the file `/auth.py` to the directory `/venv/lib/python3.8/site-packages/telethon/client`:
```
pip install -r requirements.txt
```
4. Run the database server (REST API app) realising the processing of the requests:
```python
requests.get(DATABASE_SERVER + "admins")
requests.get(DATABASE_SERVER + "phones", params={"link": link})
requests.post(DATABASE_SERVER + "phone", params={"phone": phone})
requests.post(DATABASE_SERVER + "link", params={"link": link})
requests.post(DATABASE_SERVER + "phone_link", params={"phone": phone, "link": link})
requests.delete(DATABASE_SERVER + "phone", params={"phone": phone, "link": link})
requests.delete(DATABASE_SERVER + "link", params={"phone": phone, "link": link})
requests.delete(DATABASE_SERVER + "phone_link", params={"phone": phone, "link": link})
requests.get(DATABASE_SERVER + "tasks")
requests.get(DATABASE_SERVER + "task", params={"id_task": id_task})
requests.get(DATABASE_SERVER + "phones_by_task", params={"id_task": id_task})
requests.post(DATABASE_SERVER + "task", params={"accounts": str(accounts_dict), "count": count, "timing": str(timing)})
requests.put(DATABASE_SERVER + "task", params={"id_task": id_task, "status": status})
requests.delete(DATABASE_SERVER + "task", params={"id_task": id_task})
requests.delete(DATABASE_SERVER + "task_phone", params={"id_task": id_task, "phone": phone})
requests.get(DATABASE_SERVER + "task_phone", params={"id_task": id_task})
```
5. Create configurating file `config.py`
```python
BOT_TOKEN : str # The bot token from https://t.me/BotFather
API_ID : int # Telethon's API ID
API_HASH : str # Telethon's API Hash

MILES_IN_HOUR = 3600
HOURS_IN_WEEK = 168
MILES_IN_WEEK = MILES_IN_HOUR * HOURS_IN_WEEK

RANDOM_PERCENT = 80 # The percent coefficient affecting the randomness of the time between bot accounts activities

DATABASE_SERVER : str # The database servers path ending with '/'
```
6. Run the bot:
```
python main.py
``` 

## Usage
Once you have the bot installed and running, you can use the following commands:
- /start - Start bot ▶️
- /update - Update database and refresh journal files 🔄
- /help - FAQ ❓ 

## Contributors
The ProjectStoreBot was created by SoftBananas inc., which includes the following members:
- **[ONEPANTSU](https://github.com/ONEPANTSU)**
- **[nikramiar](https://github.com/nikramiar)**

![by SoftBannas inc.](/src/sbi_logo.svg)
