from aiogram.utils.callback_data import CallbackData

subscribe_callback = CallbackData("subscribe_public_button", "is_public")
unsubscribe_callback = CallbackData("unsubscribe_public_button", "is_public")
unsubscribe_all_callback = CallbackData("unsubscribe_all_button")
viewer_post_callback = CallbackData("viewer_post_button")
reactions_callback = CallbackData("reactions_button")