from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from texts.buttons import BUTTONS
from useful.callbacks import (
    reactions_callback,
    reactions_delay_callback,
    subscribe_callback,
    subscribe_yes_no_confirm_callback,
    unsubscribe_callback,
    viewer_post_callback,
    yes_no_callback, viewer_post_delay_callback,
)
from useful.instruments import callback_dict


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


def ask_keyboard(phone):
    yes_button = InlineKeyboardButton(
        text=BUTTONS["yes"],
        callback_data=yes_no_callback.new(answer=BUTTONS["yes"], phone=phone),
    )
    no_button = InlineKeyboardButton(
        text=BUTTONS["no"],
        callback_data=yes_no_callback.new(answer=BUTTONS["no"], phone=phone),
    )
    act_keyboard = InlineKeyboardMarkup(row_width=2).add(yes_button, no_button)

    return act_keyboard


def ask_delay_keyboard(user_id, link, count, is_public, callback):
    callback_dict[user_id] = [link, count, is_public]
    delay_1 = InlineKeyboardButton(
        text=BUTTONS["delay_1"],
        callback_data=callback.new(answer=BUTTONS["delay_1"], user_id=user_id),
    )
    delay_2 = InlineKeyboardButton(
        text=BUTTONS["delay_2"],
        callback_data=callback.new(answer=BUTTONS["delay_2"], user_id=user_id),
    )
    act_delay_keyboard = InlineKeyboardMarkup(row_width=2).add(delay_1, delay_2)

    return act_delay_keyboard


def ask_delay_keyboard_viewer(user_id, link, count, last_post_id, count_posts):
    callback_dict[user_id] = [link, count, last_post_id, count_posts]
    delay_1 = InlineKeyboardButton(
        text=BUTTONS["delay_1"],
        callback_data=viewer_post_delay_callback.new(
            answer=BUTTONS["delay_1"], user_id=user_id
        ),
    )
    delay_2 = InlineKeyboardButton(
        text=BUTTONS["delay_2"],
        callback_data=viewer_post_delay_callback.new(
            answer=BUTTONS["delay_2"], user_id=user_id
        ),
    )
    act_delay_keyboard = InlineKeyboardMarkup(row_width=2).add(delay_1, delay_2)

    return act_delay_keyboard


def ask_delay_keyboard_reactions(user_id, link, count, post_id, position):
    callback_dict[user_id] = [link, count, post_id, position]
    delay_1 = InlineKeyboardButton(
        text=BUTTONS["delay_1"],
        callback_data=reactions_delay_callback.new(
            answer=BUTTONS["delay_1"], user_id=user_id
        ),
    )
    delay_2 = InlineKeyboardButton(
        text=BUTTONS["delay_2"],
        callback_data=reactions_delay_callback.new(
            answer=BUTTONS["delay_2"], user_id=user_id
        ),
    )
    act_delay_keyboard = InlineKeyboardMarkup(row_width=2).add(delay_1, delay_2)

    return act_delay_keyboard


def confirm_keyboard(user_id, callback, is_percent):
    yes_confirm = InlineKeyboardButton(
        text=BUTTONS["yes_confirm"],
        callback_data=callback.new(
            answer=BUTTONS["yes_confirm"], user_id=user_id, is_percent=is_percent
        ),
    )
    no_confirm = InlineKeyboardButton(
        text=BUTTONS["no_confirm"],
        callback_data=callback.new(
            answer=BUTTONS["no_confirm"], user_id=user_id, is_percent=is_percent
        ),
    )
    yes_no_confirm_keyboard = InlineKeyboardMarkup(row_width=2).add(
        yes_confirm, no_confirm
    )

    return yes_no_confirm_keyboard
