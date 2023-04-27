start_message = (
    "Здравствуйте, {0.first_name}! 🖐\n Я <b>Telegram Manager</b> "
    "для управелния активностью в телеграм-каналах!\n Что вам нужно?"
)
faq_message = (
    "<b>❓️ FAQ ❓️️️</b>\n"
    "\n➕ ДОБАВЛЕНИЕ АККАУНТА\n"
    " • <i>Необходимо отправить номер телефона.</i>\n"
    " • <i>Есть возможность авторизации при двухфакторной верификации.</i>\n"
    " • <i>Необходимо отправить код подтверждения.</i>\n"
    "\n🔒️ ПРИВАТНЫЙ КАНАЛ\n"
    " • <i>Приватный канал или приглосительная ссылка.</i>\n"
    "\n👀 НАКРУТКА ПРОСМОТРОВ\n"
    " • <i>Необходимо отправлять только публичные ссылки.</i>\n"
    "\n💥 НАКРУТКА РЕАКЦИЙ\n"
    " • <i>Необходимо отправлять только публичные ссылки.</i>\n"
)
main_menu_massage = "📌 Главное меню 📌"
activity_menu_massage = "🍌 Активность 🍌"
user_message = "Начинается добавление аккаунта"
parser_message = "Начинается parsing"
user_phone_message = "Введите номер телефона ☎️"
user_ask_message = "Аккаунт с паролем?"
user_password_message = "Введите пароль"
user_sms_message = "Введите код"
chose_activity_message = "Что будем делать?"
channel_link_message = "Введите ссылку на канал"
channel_name_message = "Введите название канала"
number_of_accounts_message = (
    "Введите количество аккаунтов. Доступных ботов на данный момент: {count}"
)
delay_ask_message = "Введите тип задержки"
delay_regular_message = "Введите постоянную задержку в секундах 📊"
delay_percent_message = (
    "Введите почасовые проценты аккаунтов 📉\n\n"
    "<i>Например, если в 1 час используются 50% аккаунтов, "
    "во 2 час 30%, а в 4 час 20%:</i>\n1 - 50\n2 - 30\n4 - 20"
)
subscribe_message = "Подписка на канал осуществлена"
unsubscribe_message = "Отписка от канала осуществлена"
id_post_message = "Введите id поста"
number_of_post_message = "Введите количество постов"
viewer_post_message = "Посты просмотрены"
number_of_button_message = "Введите номер кнопки"
reactions_message = "Нажатие кнопки произошло успешно"
isdigit_message = "Жду от вас циферки"

# информирование пользователя и ошибки

not_users_in_base_error = "В базе нет пользователей"
authorisation_error_message = "Произошла ошибка авторизации"
phone_error_message = "Телефон введен неверно. Попробуйте ввести ещё раз и убедитесь, что номер начинается с знака '+'"
sms_error_message = "Код введен неверно"
password_error_message = "Пароль введен неверно"
authorisation_success_message = "Авторизация прошла успешно. Пользователь: {user} "
available_bot_message = "Доступных ботов на данный момент: {count_user} "
count_user_error_message = (
    "Вы ввели слишком большое число. На данный момент в базе: {count}"
)
link_error_message = "Ссылка введена неправильно. Попробуйте ещё раз"
error_message = "Произошла ошибка! Попробуйте ещё раз!"
confirm_message = "Данные введены верно?"
confirm_no_message = "Действие не произведено!"
confirm_yes_message = "Действие произведено!"
get_timing_error = "Введен неправильный формат задержки. Действие не выполнено!"

LOADING = [
    "▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️ 0 %",
    "🟥▫️▫️▫️▫️▫️▫️▫️▫️▫️ 10 %",
    "🟥🟥▫️▫️▫️▫️▫️▫️▫️▫️ 20 %",
    "🟥🟥🟥▫️▫️▫️▫️▫️▫️▫️ 30 %",
    "🟧🟧🟧🟧▫️▫️▫️▫️▫️▫️ 40 %",
    "🟧🟧🟧🟧🟧▫️▫️▫️▫️▫️ 50 %",
    "🟧🟧🟧🟧🟧🟧▫️▫️▫️▫️ 60 %",
    "🟨🟨🟨🟨🟨🟨🟨▫️▫️▫️ 70 %",
    "🟨🟨🟨🟨🟨🟨🟨🟨▫️▫️ 80 %",
    "🟨🟨🟨🟨🟨🟨🟨🟨🟨▫️ 90 %",
    "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100 %",
]

MESSAGES = {
    "start": start_message,
    "main_menu": main_menu_massage,
    "activity_menu": activity_menu_massage,
    "user": user_message,
    "parser": parser_message,
    "user_phone": user_phone_message,
    "user_ask": user_ask_message,
    "user_password": user_password_message,
    "user_sms": user_sms_message,
    "channel_link": channel_link_message,
    "channel_name": channel_name_message,
    "number_of_accounts": number_of_accounts_message,
    "delay_ask": delay_ask_message,
    "delay_regular": delay_regular_message,
    "delay_perсent": delay_percent_message,
    "subscribe": subscribe_message,
    "unsubscribe": unsubscribe_message,
    "id_post": id_post_message,
    "number_of_post": number_of_post_message,
    "viewer_post": viewer_post_message,
    "number_of_button": number_of_button_message,
    "reactions": reactions_message,
    "chose_activity": chose_activity_message,
    "isdigit": isdigit_message,
    "faq": faq_message,
    "authorisation_error": authorisation_error_message,
    "phone_error": phone_error_message,
    "sms_error": sms_error_message,
    "password_error": password_error_message,
    "authorisation_success_error": authorisation_success_message,
    "available_bot": available_bot_message,
    "count_user_error": count_user_error_message,
    "link_error": link_error_message,
    "error": error_message,
    "confirm": confirm_message,
    "confirm_no": confirm_no_message,
    "confirm_yes": confirm_yes_message,
    "get_timing": get_timing_error,
}
