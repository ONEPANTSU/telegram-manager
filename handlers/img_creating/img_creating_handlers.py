import io

import anvil as anvil
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from PIL import Image, ImageDraw, ImageFont
from handlers.main.main_functions import main_menu
from states import CreateImgStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from useful.instruments import bot

chose_img_callback = CallbackData('img_type', 'type')
back_img_callback = CallbackData('back_img')


async def chose_img_by_callback(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    a1 = InlineKeyboardButton(BUTTONS['a1'], callback_data=chose_img_callback.new(type="A1"))
    a2 = InlineKeyboardButton(BUTTONS['a2'], callback_data=chose_img_callback.new(type="A2"))
    b1 = InlineKeyboardButton(BUTTONS['b1'], callback_data=chose_img_callback.new(type="B1"))
    b2 = InlineKeyboardButton(BUTTONS['b2'], callback_data=chose_img_callback.new(type="B2"))
    c1 = InlineKeyboardButton(BUTTONS['c1'], callback_data=chose_img_callback.new(type="C1"))
    c2 = InlineKeyboardButton(BUTTONS['c2'], callback_data=chose_img_callback.new(type="C2"))
    grammar = InlineKeyboardButton(BUTTONS['grammar'], callback_data=chose_img_callback.new(type="Грамматика"))
    level_keyboard = InlineKeyboardMarkup(row_width=2).add(a1, a2, b1, b2, c1, c2, grammar)
    await query.message.edit_text(MESSAGES['level'], reply_markup=level_keyboard)


async def chose_img_by_command(message: Message):
    a1 = InlineKeyboardButton(BUTTONS['a1'], callback_data=chose_img_callback.new(type="A1"))
    a2 = InlineKeyboardButton(BUTTONS['a2'], callback_data=chose_img_callback.new(type="A2"))
    b1 = InlineKeyboardButton(BUTTONS['b1'], callback_data=chose_img_callback.new(type="B1"))
    b2 = InlineKeyboardButton(BUTTONS['b2'], callback_data=chose_img_callback.new(type="B2"))
    c1 = InlineKeyboardButton(BUTTONS['c1'], callback_data=chose_img_callback.new(type="C1"))
    c2 = InlineKeyboardButton(BUTTONS['c2'], callback_data=chose_img_callback.new(type="C2"))
    grammar = InlineKeyboardButton(BUTTONS['grammar'], callback_data=chose_img_callback.new(type="Грамматика"))
    level_keyboard = InlineKeyboardMarkup(row_width=2).add(a1, a2, b1, b2, c1, c2, grammar)
    await message.answer(MESSAGES['level'], reply_markup=level_keyboard)


async def create_img(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = callback_data['type']
    await state.update_data(type=data)
    new_msg = MESSAGES["terminus"].format(type=data)
    back = InlineKeyboardButton(BUTTONS['back'], callback_data=back_img_callback.new())
    keyboard = InlineKeyboardMarkup().add(back)
    await query.message.edit_text(text=new_msg, reply_markup=keyboard)
    await CreateImgStates.text1.set()


async def text1_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(terminus=answer)
    await message.answer(MESSAGES['transcription'])
    await CreateImgStates.text2.set()


async def text2_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(transcription=answer)
    await message.answer(MESSAGES['translation'])
    await CreateImgStates.text3.set()


async def text3_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(translation=answer)
    data = await state.get_data()
    await state.finish()
    img = get_img(data['type'], data['terminus'], data['transcription'], data['translation'])
    await bot.send_photo(message.chat.id, img)


def get_img(type, terminus, transcription, translation):
    im = Image.open("src/img/" + type + '.jpg')
    font = ImageFont.truetype('src/font/19019.ttf', size=50)
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        (250, 100),
        terminus,
        font=font,
        fill=('#1C0606')
    )
    draw_text.text(
        (250, 130),
        transcription,
        font=font,
        fill=('#1C0606')
    )
    draw_text.text(
        (250, 160),
        translation,
        font=font,
        fill=('#1C0606')
    )
    return img_to_media_obj(im)


def img_to_media_obj(img):
    img_byte_arr = img
    b = io.BytesIO()
    img_byte_arr.save(b, format="jpeg")
    media_obj =  b.getbuffer()
    return media_obj


def register_img_creating_handlers(dp: Dispatcher):
    dp.register_message_handler(chose_img_by_command, text=[BUTTONS["create_post"]])
    dp.register_callback_query_handler(create_img, chose_img_callback.filter())
    dp.register_callback_query_handler(chose_img_by_callback, back_img_callback.filter())
    dp.register_message_handler(text1_state, state=CreateImgStates.text1)
    dp.register_message_handler(text2_state, state=CreateImgStates.text2)
    dp.register_message_handler(text3_state, state=CreateImgStates.text3)
