import random, os
import telebot, time

players = [["Антон", [], 1123310395], ["Рома", [], 799377676], ["Камал", [], 1297353670], ["Глеб", [], 1374685400]]
locs = [["Дрова", 10, 20], ["Теплицы", 10, 20], ["Крыльцо", 5, 10], ["Туалет", 15, 20], ["Бытовка", 10, 20], ["Тачка", 8, 13], ["Курятник", 10, 20], ["Скважина", 10, 20], ["Пень", 5, 10]]
imposter = random.choice(players)
bot = telebot.TeleBot('1302974569:AAHIyT0L3YqzX4OZqD2RLQzmksC8P2ADEcE')

for pl in players:
	if pl == imposter:
		pass
	else:
		i = 0
		for i in range(3):
			miss = random.choice(locs)
			miss2 = [miss[0], random.randrange(miss[1], miss[2])]
			players[players.index(pl)][1].append(miss2)
			locs.remove(miss)
			i += 1

f = False

for pl in players:

	if pl == imposter:
		role = "Imposter"
	else:
		role = "Crewmate"
	msg = f'''
		{pl[0]}.
		  Роль: {role}
		  Миссии:
	'''
	if role != "Imposter":
		for m in pl[1]:
			msg += f'''
				Название: {m[0]}, время - {m[1]} сек
			'''
	print(pl[0])
	bot.send_message(pl[2], msg)
	time.sleep(1)