from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from texts.buttons import BUTTONS
from useful.callbacks import subscribe_callback, unsubscribe_callback, viewer_post_callback, reactions_callback


def activity_keyboard():
    subscribe_public_button = InlineKeyboardButton(
        text=BUTTONS["subscribe_public"],
        callback_data=subscribe_callback.new(is_public=True),
    )
    subscribe_private_button = InlineKeyboardButton(
        text=BUTTONS["subscribe_private"],
        callback_data=subscribe_callback.new(is_public=False),
    )
    unsubscribe_public_button = InlineKeyboardButton(
        text=BUTTONS["unsubscribe_public"],
        callback_data=unsubscribe_callback.new(is_public=True),
    )
    unsubscribe_private_button = InlineKeyboardButton(
        text=BUTTONS["unsubscribe_private"],
        callback_data=unsubscribe_callback.new(is_public=False),
    )
    view_button = InlineKeyboardButton(
        text=BUTTONS["view"], callback_data=viewer_post_callback.new()
    )
    react_button = InlineKeyboardButton(
        text=BUTTONS["react"], callback_data=reactions_callback.new()
    )

    act_keyboard = InlineKeyboardMarkup(row_width=1).add(
        subscribe_public_button,
        subscribe_private_button,
        unsubscribe_public_button,
        unsubscribe_private_button,
        view_button,
        react_button,
    )
    return act_keyboard