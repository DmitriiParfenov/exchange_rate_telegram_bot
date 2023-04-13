import json
import os
import string

import telebot

from utils.currency_symbols import get_currency_symbols
from scr.exchange_rate import ExchangeRate

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')
EXCHANGE_RATE_API_KEY = os.environ.get('EXCHANGE_RATE_API_KEY')
CURRENCY_SYMBOLS = os.path.join('../utils', 'currency_symbols.json')
CURRENCY_RATES = 'currency_rates.json'
bot = telebot.TeleBot(TELEGRAM_API_KEY)
base_currency = ''


@bot.message_handler(commands=['start'])
def start(message):
    """
    Функция, которая приветствует пользователя и предлагает ему приступить к конвертации или узнать
    возможности бота. Также, функция открывает файл currency_symbols.json и туда записывает все
    возможные символы валют, полученных от API
    :param message: str
    :return: str
    """
    text = f'Привет, {message.from_user.first_name} {message.from_user.last_name}!\n' \
           f'Наш бот — это актуальный конвертер валют. \n' \
           f'Для просмотра полезных команд бота напиши — /help. \n' \
           f'Для конвертации валюты напиши — /convert.'
    with open(CURRENCY_SYMBOLS, 'a') as file:
        if os.stat(CURRENCY_SYMBOLS).st_size == 0:
            db = get_currency_symbols()
            json.dump(db, file)
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def get_help(message):
    """
    Функция возвращает строку, в которой написаны все возможности бота
    :param message: str
    :return: str
    """
    text = f'/convert — конвертация валют\n' \
           f'/get_requests — последние операции\n' \
           f'/get_symbols — аббревиатуры валют\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['get_symbols'])
def get_symbols(message):
    """
    Функция в читабельном виде выводит пользователю все возможные символы валют, полученных от API
    :param message: str
    :return: str
    """
    with open(CURRENCY_SYMBOLS) as file:
        db = json.load(file)
        text = ''
        for elem in db:
            text += f'{elem} — {db[elem]}\n'
        bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['get_requests'])
def get_requests(message):
    """
    Функция выводит пользователю историю совершенных конвертаций. Если не было произведено ни одной конвертации,
    то возвращает строку — 'Упс, кажется вы еще не совершали конвертацию'.
    :param message: str
    :return: str
    """
    with open(CURRENCY_RATES) as file:
        if os.stat(CURRENCY_RATES).st_size == 0:
            text = 'Упс, кажется вы еще не совершали конвертацию'
            bot.send_message(message.chat.id, text)
        else:
            text = ''
            db = json.load(file)
            for index, elem in enumerate(db):
                text += f'Операция {index + 1}:\n' \
                        f'Курс {elem["from_currency"]} к {elem["to_currency"]} составляет {elem["rate"]:.2f}\n' \
                        f'Дата обращения — {elem["timestamp"]}\n\n'
            bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    """
    Функция реагирует на все сообщения пользователя и возврощает строку с дальнейшими инструкциями.
    Если пользователь ввел /convert, то будет вызвана функция для получения от пользователя валюты для конвертации.
    Если пользователь ввел /help, то будет вызвана функция для вызова сообщения с описанием возможностей бота.
    :param message: str
    :return: str
    """
    if message.text == '/convert':
        text = f"Поехали!\nДля конвертации валют необходимо вводить их аббревиатуры на английском языке.\n" \
               f"Например, российские рубли — RUB или rub :)\n" \
               f"Приступаем к конвертации?\nВведите <b><u>да</u></b> или <b><u>нет</u></b>."
        bot.send_message(message.chat.id, text, parse_mode='html')
        bot.register_next_step_handler(message, get_from_currency)
    elif message.text == '/help':
        bot.register_next_step_handler(message, get_help)
    else:
        text = f'Я тебя не понял\n' \
               f'Для просмотра полезных команд бота напиши — /help. ' \
               f'Для конвертации валюты напиши — /convert.'
        bot.send_message(message.chat.id, text)


def get_from_currency(message):
    """
    Функция запрашивает у пользователя, какую валюту он хочет конвертировать. Если пользователь введен да в
    любом регистре, то будет вызвана функция для считывания валюты и ее валидации, а если нет — оповещающая строка.
    В ином случае, бот запросит у пользователя повторный ввод данных
    :param message: str
    :return: str
    """
    if message.text.lower() == 'да':
        text = f'Какую валюту хочешь конвертировать?'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, get_to_currency)
    elif message.text.lower() == 'нет':
        text = f'Очень жаль! Тогда в следующий раз :)'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, start)
    else:
        text = f'Я вас не понял. Повторите, пожалуйста, ввод'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, get_from_currency)


def get_to_currency(message):
    """
    Функция считывает у пользователя символ валюты, проверяет корректность введенных данных. Если данные
    корректны, то функция запрашивает у пользователя, относительно какой валюты пользователь хочет получить
    курс. В ином случае — вернет оповешающую строку и запросит повторный ввод.
    :param message: str
    :return: str
    """
    global base_currency
    upper_cases = string.ascii_uppercase
    flag = False
    for elem in message.text.upper():
        if elem in upper_cases:
            flag = True
        else:
            flag = False
    with open(CURRENCY_SYMBOLS) as file:
        db = json.load(file)
    if flag and len(message.text) == 3 and message.text.upper() in db:
        text = f'Относительно какой валюты хочешь получить конвертацию?'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, get_exchange_rate)
        base_currency = message.text
    else:
        text = "Кажется, что вы ввели недопустимые символы. Пожалуйста, повторите ввод в нужном формате"
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, get_to_currency)


def get_exchange_rate(message):
    """
    Функция считывает у пользователя символ валюты, проверяет корректность введенных данных. Если данные
    корректны, то функция вернет от API текущий курс валют. В ином случае — вернет оповешающую строку и
    запросит повторный ввод.
    :param message: str
    :return: str
    """
    upper_cases = string.ascii_uppercase
    flag = False
    for elem in message.text.upper():
        if elem in upper_cases:
            flag = True
        else:
            flag = False
    with open(CURRENCY_SYMBOLS) as file:
        db = json.load(file)
    if flag and len(message.text) == 3 and message.text.upper() in db:
        exchange_rate = ExchangeRate(EXCHANGE_RATE_API_KEY, base_currency, message.text)
        exchange_rate.get_currency_rate()
        text = exchange_rate.get_show
        bot.send_message(message.chat.id, text)
    else:
        text = "Кажется, что вы ввели недопустимые символы. Пожалуйста, повторите ввод в нужном формате"
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, get_exchange_rate)


bot.polling(none_stop=True)
