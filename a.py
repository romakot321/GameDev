import telebot
import re, pickle, time

users = []
market = []
jobsList = ["шахтер", "полицейский", "работникназаводе", "медработник", "хирург", "главврач", "бомж", "учитель", "официант", "повар"]

bot = telebot.TeleBot('1302974569:AAHIyT0L3YqzX4OZqD2RLQzmksC8P2ADEcE')
bot.timedout = 120

adminId = 799377676 

with open('users.txt', 'rb') as f:
    users = pickle.load(f)
print(users)

@bot.message_handler(commands=['reg'])
def regiser(message):
    global users, jobsList
    user = message.text.lower().replace('/reg', '')
    user = re.split(r'\W+', user)
    f = True
    for u in users:
        if u[0] == message.from_user.id:
            f = False
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы')
    if f:
        c = 0
        name = False
        job = False
        for i in user:
            if i != "" and c == 0:
                print(i)
                name = i
                c += 1
                continue
            if i != "" and c == 1:
                print(i, name, jobsList)
                if i in jobsList:
                    job = i
                else:
                    bot.send_message(message.chat.id, "Такой работы не существует")
        if name != False and job != False:
            users.append([message.from_user.id, name, job])
            bot.send_message(message.chat.id, f"Зарегистрирован новый пользователь {name} с работой {job}!")
            with open('users.txt', 'wb') as f:
                pickle.dump(users, f)

@bot.message_handler()
def msg(message):
    print(message.from_user.username, message.from_user.id, message.text)
    f = True
    for u in users:
        if u[0] == message.from_user.id:
            f = False
    if f:
        bot.send_message(message.chat.id, "Для регистрации введите /reg [ник в игре] [профессия из списка]")
    if re.search("новый трейд", message.text.lower()):
        itemName = message.text.lower().replace('новый трейд', '')
    if message.text.lower() == "профессии":
        msg = ""
        for j in jobsList:
            msg += j + ", "
        bot.send_message(message.chat.id, msg)
    if message.text.lower() == "инфо":
        for u in users:
            if u[0] == message.from_user.id:
                bot.send_message(message.chat.id, f'''
    Ник: {u[1]}({message.from_user.id}),
    Профессия: {u[2]}.
   ''')
                break
    if message.text.lower() == "привет":
        name = message.from_user.first_name
        for u in users:
            if u[0] == message.from_user.id:
                name = u[1]
        bot.send_message(message.chat.id, f"Привет, {name}")
    if message.text.lower() == "иди нахуй":
        bot.send_message(message.chat.id, 'а ты кто такой а')
    if re.search('ник', message.text.lower()):
        name = message.text.lower().replace('ник', '')
        for u in users:
            if u[0] == message.from_user.id:
                users[users.index(u)][1] = name
        with open('users.txt', 'wb') as f:                  pickle.dump(users, f)

@bot.message_handler(commands=['start'])
def start_message(message):
    global users
    bot.send_message(message.chat.id, 'Приветствую тебя в ЛФ, странник!')
    if not [message.from_user.username, message.chat.id] in users:
        print('new user')
        users.append([message.chat.username, message.chat.id])

def send_text(message):
    global users
    print(f'User: {message.chat.username}, /n  text: {message.text}')
    if message.text.lower() == 'привет':
        name = ""
        for u in users:
            if u[1] == message.chat.id:
                name = u[0]
                break
        bot.send_message(message.chat.id, f'Привет, {name}')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, пользователь')
    elif message.text == 'ZzZx':
        bot.send_message(message.chat.id, "Happy new year!")
        for u in users:
            if u[0] == message.chat.id:
                users[users.index(u)][3] = "Лошара!"

bot.polling()
