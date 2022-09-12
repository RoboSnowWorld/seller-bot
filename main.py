# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random
import time

import telebot

import telebot
import os
from telebot import types
import settings as s
import requests

bot = telebot.TeleBot(s.token)

general_markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
generalbtn_1 = types.KeyboardButton(s.language['sell_accounts_button'])
generalbtn_2 = types.KeyboardButton(s.language['buy_accounts_button'])
generalbtn_3 = types.KeyboardButton(s.language['about_button'])
general_markup.add(generalbtn_1, generalbtn_2, generalbtn_3)
admin_username = ''
currency = '$'

trade_markup = types.ReplyKeyboardMarkup(row_width=2)
tradebtn_1 = types.KeyboardButton(s.language['exit_button'])
trade_markup.add(tradebtn_1)

account_types = {}
current_checking = {}

def load_accounts():
    for folder in os.listdir('accounts'):
        if 'txt' in folder:
            try:
                with open(f'accounts/{folder}') as f:
                        first_line = f.read().splitlines()[0]
                    # first_line = ''
                    # for part in f.read().splitlines()[0].split(' ')[:-1]:
                    #     first_line += part
                account_types[first_line.replace(f' {first_line.split(" ")[-1]}', '')] = folder
            except:
                pass

@bot.message_handler(regexp=s.language['about_button'])
def bot_info(message):
    bot.send_message(message.chat.id, s.language['support'])

@bot.message_handler(regexp=s.language['exit_button'])
def command_exit(message):
    start_command(message)

@bot.message_handler(regexp=s.language['buy_accounts_button'])
def buy_tokens(message):
    account_types_to_buy = ''
    for account_type in account_types.keys():
        with open(f'accounts/{account_types[account_type]}') as f:
            price = f.readlines()[0].split(' ')[-1]
        account_types_to_buy += f'{account_type} {price[:-1]}р\n'
    bot.send_message(message.chat.id, f'{account_types_to_buy}',
                                      reply_markup=trade_markup)
    bot.send_message(message.chat.id, s.language['buy_accounts'])

@bot.message_handler(regexp='Sell accounts')
def sell_tokens(message):
    bot.send_message(message.chat.id, s.language['sell_accounts'],
                                       reply_markup=trade_markup)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.username} ✋\nUsing this bot you can buy and sell accounts 💰', reply_markup=general_markup)
    if message.from_user.username == s.admin_username:
        with open('admin_chat_id.txt', 'w') as f:
            f.write(str(message.chat.id))

@bot.message_handler(regexp='ba')
def buying_process(message):
    number = int(message.text.split(' ')[-1])
    account_name = message.text
    account_name = account_name.split('ba ')[1]
    account_name = account_name.split(f' {str(number)}')[0]
    try:
        account_types[account_name]
    except KeyError:
        bot.send_message(message.chat.id, s.language['accounts_not_in_stock'])
        return
    with open(f'accounts/{account_types[account_name]}') as f:
        counter = len(f.readlines()) - 1
        if counter < number:
            bot.send_message(message.chat.id, s.language['accounts_not_in_stock'])
            return
    with open(f'accounts/{account_types[account_name]}') as f:
                accounts = (f.readlines()[1:number + 1])
    with open(f'accounts/{account_types[account_name]}', 'r') as source:
        to_write = []
        lines = source.readlines()
        to_write.append(lines[0])
        for line in lines[number + 1:]:
            to_write.append(line)
    with open(f'accounts/{account_types[account_name]}', 'w') as dest:
        dest.writelines(to_write)
    order_id = random.randint(10000,99999)
    with open(f'{order_id}.txt', 'w') as f:
        f.write(f'{message.chat.id}\n {account_name}\n')
        f.writelines(accounts)
    with open(f'accounts/{account_types[account_name]}') as f:
        price = f.readlines()[0].split(' ')[-1]
    to_pay = int(price) * number
    r = requests.put(url=f'https://api.qiwi.com/partner/bill/v1/bills/{order_id}',
                     headers={'Authorization': f'Bearer {s.secret_key}', 'Content-Type': 'application/json',
                              'Accept': 'application/json'}, json={
            "amount": {
                "currency": "RUB",
                "value": to_pay
            },
            "expirationDateTime": "2025-12-10T09:02:00+03:00",})
    payurl = r.json()['payUrl']
    bot.send_message(message.chat.id, f'Your order number is {order_id}✅. Price: {to_pay}р\n payment details: {payurl} 📝')
    with open('admin_chat_id.txt') as f:
        admin_chat_id = int(f.read())
    bot.send_message(admin_chat_id, f'{order_id} {account_name} 📝\n amount to pay {to_pay} р\n')
    counter = 0
    while counter < 1800:
        r = requests.get(url=f'https://api.qiwi.com/partner/bill/v1/bills/{order_id}',
                         headers={'Authorization': f'Bearer {s.secret_key}'})
        status = r.json()['status']['value']
        if status == 'PAID':
            accept_buy(order_id)
            return
        counter += 1
        time.sleep(1)
    decline_buy(order_id)



@bot.message_handler(content_types=['document'])
def selling_process(message):
    sell_id = random.randint(10000,99999)
    file_id = message.document.file_id
    bytes_file = bot.download_file(bot.get_file(file_id).file_path)
    with open(f'selling/{sell_id}.txt', 'wb') as f:
        f.write(bytes_file)
    with open(f'selling/{sell_id}.txt', 'a') as f:
        f.write(f'{message.from_user.username}\n')
    with open('admin_chat_id.txt') as f:
        admin_chat_id = int(f.read())
    bot.send_message(admin_chat_id, f'New selling from {message.from_user.username} 💰')
    with open(f'selling/{sell_id}.txt', 'rb') as f:
        bot.send_document(admin_chat_id, f)
    bot.send_message(message.chat.id, s.language['successful'])

def accept_buy(order_id):
    with open(f'{order_id}.txt') as f:
        chat_id = f.readlines()[0]
    with open(f'{order_id}.txt', 'r') as source:
        to_write = source.readlines()[2:]
    with open(f'{order_id}.txt',  'w') as dest:
        dest.writelines(to_write)
    with open(f'{order_id}.txt', 'rb') as f:
        bot.send_document(chat_id, f)

@bot.message_handler(regexp='decline_buy')
def decline_buy(order_id):
    with open(f'{order_id}.txt') as f:
        accounts = f.readlines()[2:]
    with open(f'{order_id}.txt') as f:
        account_name = f.readlines()[1]
    account_name = account_name[1:-1]
    f_n = open(f'accounts/{account_types[account_name]}', 'a')
    for account in accounts:
        f_n.write(account)

while True:
    try:
        load_accounts()
        bot.polling()
    except:
        pass
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
