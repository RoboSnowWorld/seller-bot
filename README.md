# seller-bot
Telegram bot for selling accounts

<a href="https://github.com/RoboSnowWorld/seller-bot-ru"><strong>На русском »</strong></a>
# How to install
* Enter your creditionals in **creditionals.txt**
* Load your accounts in **accounts** folder
* Write **tile** for accounts and **price** in the first line of each file
```
simple_accounts 4
account_1
account_2
account_3
```
* Enter your username in the main.py
<img src="https://i.imgur.com/JjL5Mys.jpg" alt="From your telegram profile" width="320" height="160">

```
admin_username = your username
```
* Enter your bot token in the main.py
```
bot = telebot.TeleBot('token')
```
* Run bot and send "chat_id" message

<img src="https://i.imgur.com/nEwTAJC.jpg" alt="Exaple" width="320" height="160">

* Enter answer in the main.py
```
admin_chat_id = 'answer'
```
* Customize answers of bot in the main.py
```
bot.send_message(message.chat.id, 'Telegram bot for buying accounts\nSupport [your contacts]')
```
* Enter your currency in main.py
```
currency = '$'
```

# How to use
* You will see a notification that someone bought accounts
<img src="https://i.imgur.com/Hfb09yw.jpg" alt="Exaple" width="320" height="160">

* You can send **accept_buy [order id]** if you received money
<img src="https://i.imgur.com/0ZFOe4s.jpg" alt="Exaple" width="320" height="160">

* You can send **decline_buy [order_id]** if you didn't received money
<img src="https://i.imgur.com/GGKFM8d.jpg" alt="Exaple" width="320" height="160">
