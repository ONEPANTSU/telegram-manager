from aiogram.utils.callback_data import CallbackData

subscribe_callback = CallbackData("subscribe_button", "is_public")
unsubscribe_callback = CallbackData("unsubscribe_button", "is_public")
unsubscribe_all_callback = CallbackData("unsubscribe_all_button")
viewer_post_callback = CallbackData("viewer_post_button")
reactions_callback = CallbackData("reactions_button")

yes_no_callback = CallbackData("yes_no", "answer", "phone")

subscribe_delay_callback = CallbackData("subscribe_delay", "answer", "user_id")
unsubscribe_delay_callback = CallbackData("unsubscribe_delay", "answer", "user_id")
viewer_post_delay_callback = CallbackData("viewer_post_delay", "answer", "user_id")
reactions_delay_callback = CallbackData("reactions_delay", "answer", "user_id")

subscribe_yes_no_confirm_callback = CallbackData(
    "subscribe_yes_no_confirm", "answer", "user_id", "is_percent"
)
unsubscribe_yes_no_confirm_callback = CallbackData(
    "unsubscribe_yes_no_confirm", "answer", "user_id", "is_percent"
)
viewer_yes_no_confirm_callback = CallbackData(
    "viewer_yes_no_confirm", "answer", "user_id", "is_percent"
)
reactions_yes_no_confirm_callback = CallbackData(
    "reaction_yes_no_confirm", "answer", "user_id", "is_percent"
)

task_callback = CallbackData("task", "page")
delete_task_callback = CallbackData("delete_task", "task_id", "page")
stop_task_callback = CallbackData("stop_task", "task_id", "page")

confirm_delete_task_callback = CallbackData(
    "task_yes_no_confirm_keyboard", "answer", "task_id"
)
