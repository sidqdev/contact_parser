from telebot import TeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from parser_999md import Parser999md
from parser_makler import ParserMakler
from dotenv import load_dotenv
load_dotenv()
import os

TOKEN = os.getenv("TOKEN")

bot = TeleBot(TOKEN)
storage = dict()

md999 = Parser999md(bot)
makler = ParserMakler(bot)


parser_storage = dict()
category_storage = dict()


@bot.message_handler(['start', 'menu'])
def start(message: Message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("999.md", callback_data='md999')
    )
    markup.add(
        InlineKeyboardButton("Makler", callback_data='makler')
    )
    bot.send_message(
        message.chat.id,
        "Выберете сайт",
        reply_markup=markup
    )


@bot.callback_query_handler(lambda e: e.data in ('md999', 'makler'))
def select_parser(callback: CallbackQuery):
    parser = None
    if callback.data == 'md999':
        parser_storage.update({callback.message.chat.id: md999})
        parser = md999
    elif callback.data == 'makler':
        parser_storage.update({callback.message.chat.id: makler})
        parser = makler
    else:
        return

    categories = parser.get_categories_for_markup()
    markup = InlineKeyboardMarkup()
    for i in categories:
        markup.add(InlineKeyboardButton(**i))
    
    markup.add(InlineKeyboardButton("Ввести ссылку", callback_data="input_links"))
    bot.edit_message_text(
        text="Выберете категорию",
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=markup
    )


@bot.callback_query_handler(lambda e: parser_storage[e.message.chat.id].check_category_id(e.data))
def select_category(callback: CallbackQuery):
    category_storage.update({callback.message.chat.id: callback.data})
    bot.edit_message_text(
        text="Введите количество номеров",
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )


@bot.callback_query_handler(lambda e: e.data == 'input_links')
def input_links_menu(callback: CallbackQuery):
    bot.edit_message_text(
        text="Введите ссылку",
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )


@bot.message_handler(func=lambda x: parser_storage.get(x.chat.id).check_link(x.text))
def input_count(message: Message):
    category_storage.update({message.chat.id: [message.text]})
    bot.send_message(
        text="Введите количество номеров",
        chat_id=message.chat.id,
        reply_markup=None
    )


@bot.message_handler(func=lambda x: parser_storage.get(x.chat.id) and category_storage.get(x.chat.id) and x.text.isdigit())
def input_count(message: Message):
    parser = parser_storage.pop(message.chat.id)
    if type(category_storage.get(message.chat.id)) is list:
        link = category_storage.get(message.chat.id)
    else:
        link = parser.get_link_by_id(category_storage.get(message.chat.id))
    if parser.parse(link, int(message.text), message.chat.id):
        bot.send_message(message.chat.id, "Ожидайте ответа")
    else:
        bot.send_message(message.chat.id, "Ошибка")


@bot.message_handler(['parse_999'])
def parse_command_handler(message: Message):
    _, link, limit = message.text.split(' ')
    limit = int(limit)
    if md999.parse(link, limit, message.chat.id):
        bot.send_message(message.chat.id, 'Ожидайте ответа')
    else:
        bot.send_message(message.chat.id, 'Ошибка')


@bot.message_handler(['parse_makler'])
def parse_command_handler(message: Message):
    _, link, limit = message.text.split(' ')
    limit = int(limit)
    if makler.parse(link, limit, message.chat.id):
        bot.send_message(message.chat.id, 'Ожидайте ответа')
    else:
        bot.send_message(message.chat.id, 'Ошибка')

bot.infinity_polling(timeout=10, long_polling_timeout=5)