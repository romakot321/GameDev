# -*- coding: utf-8 -*-

from random import randrange
import os
import re
import pickle
import time
import json

class Map1():
	def __init__(self):
		self.mapSize = [3000, 10000] # maxX maxY
		self.chunks = []
		self.itemsInCoords = [[0, 1, 203, 2]] # [itemId, count, x, y]
		for i in range(0, (self.mapSize[0] + self.mapSize[1]) // 16):
			x = i * 16
			y = x
			listI = [i, 0, x, y, x + 16, y + 16] # chunk[id, isClear?, minX, minY, maxX, maxY]
			self.chunks.append(listI)
		self.locationsCoords = [[0, "ПолицейскийУчасток", 0, 500, 300, 1000, 0, 1], [1, "ШтабКрасногоОрла", 500, 1100, 800, 1600, 0, 1], 
								[2, "НиггасХрупперс", 700, 1700, 1100, 2300, 0, 1], [3, "РайонДипфельгаума", 1300, 2500, 2500, 4000, 0, 1],
								[-1, "Лос-Анджелес(гос.район)", -2, -2, 1500, 5000, -1, 1], [-2, "Лос-Анджелес(руины)", 1501, 5001, 3000, 10000, -1, 1] ] 
								# location[id, name, minx, miny, maxx, maxy, typeId, isUnlocked?] (typeIds: 0 - city, 1 - dung, -1 and -2 - world)
								# For dung type - loc[id, name, minx, miny, maxx, maxy, type, enterX, enterY]
		self.structures = [[-2, 0, "Руины", [1502, 1550], [5005, 5049], 0, 0], [0, 1, "Домик)", [5, 35], [501, 550], 1, 0], 
						   [0, 2, "Склад", [200, 300], [975, 1000], 1, 1], [-1, 3, "Команата тестировщика", [-1, 0], [-1, 0], 1, 0] ]
		# [locId, strId, strName, [minx, maxx], [miny, maxy], type, unlckd?]
		# typesStr: 0 - ruins, 1 - home, decor
		self.decor = [[1, 0, 'Сундук', 0, [[8, 1], [5, 150]] ], [1, 1, 'Сейф', 1, [[2, 1], [5, 500]], "1234"],
					  [2, 2, 'Оружейный сейф', 1, [[0, 5], [3, 1], [10, 2]], "0001878"], [2, 3, 'Шкафчик', 0, []],
					  [2, 4, "Шкаф с экипировкой", 2, [[0, 1], [9, 1], [11, 1], [12, 1], [13, 1], [14, 1]], 16],
					  [3, 5, "Нихуя незаметный шкаф", 0, []]]
		# [strId, decId, decName, decType] (types: 0 - container, 1 - container with pswrd, 2 - cont(need key))
		# if decType == 0: [strId, decId, decName, decType, inv[[itemId,count]], "password"(if decType = 1)]
																			#  , itemId(key)
		self.inDung = False
		for item in items.itemsList:
			i = [item[0], 1]
			self.decor[5][4].append(i)

	def checkCoords(self, pl, loc):
		for item in self.itemsInCoords:
			if pl.x == item[2] and pl.y == item[3]:
				items.addItemToInv(pl, item[0], item[1])
				self.itemsInCoords.pop(self.itemsInCoords.index(item))
				break
		s = map1.getStructure(pl, loc)
		if s[5] == 0 and s[6] == 0:
			c = False
			if s[1] != None:
				self.structures[s[7]][6] = 1
				c = True
			if c == True:
				print("Новая структура открыта")
				time.sleep(1)
				drop = []
				for i in range(0, randrange(1, 5)):
					r = randrange(0, 100)
					for d in items.strDrop:
						if r in range(d[1], d[2]):
							if d[3][0] != d[3][1]:
								dr = [d[0], randrange(d[3][0], d[3][1])]
							else:
								dr = [d[0], d[3][0]]
							drop.append(dr)
				if drop != []:
					for iD in drop:
						items.addItemToInv(pl, iD[0], iD[1])

	def getStructure(self, pl, loc):
		retStr = [-50, None, "None", [-1, -1], [-1, -1], 0, 0]
		for strc in self.structures:
			if loc[0] == strc[0]:
				if pl.x in range(strc[3][0], strc[3][1]) and pl.y in range(strc[4][0], strc[4][1]):
					retStr = strc
					break
		return retStr
	def getChunk(self, pl):
		retChunk = -1
		i = 0
		for chunk in self.chunks:
			if chunk != -1 and chunk != 1:
				if chunk[1] == 1:
					if pl.x in range(chunk[3], chunk[5]):
						retChunk = chunk
						break
			i += 1	
		return retChunk
	def getDecor(self, pl, loc):
		struct = self.getStructure(pl, loc)
		for dec in self.decor:
			if struct[1] == dec[0]:
				print("{}) {}".format(dec[1], dec[2]))
		input()

	def move(self, pl, currLoc, direction, enemies):
		minX = currLoc[2]
		maxX = currLoc[4]
		minY = currLoc[3]
		maxY = currLoc[5]
		if direction == "down" and pl.y in range(minY, maxY):
			pl.y -= pl.speed
		elif direction == "up" and pl.y in range(minY, maxY):
			pl.y += pl.speed
		elif direction == "right" and pl.x in range(minX, maxX):
			pl.x += pl.speed
		elif direction == "left" and pl.x in range(minX, maxX):
			pl.x -= pl.speed
		else:
			for loc in self.locationsCoords:
				if direction == loc[1].upper():
					if loc[7] == 1:
						pathLen = (pl.x + pl.y) - (loc[2] + loc[3])
						if pathLen < 0:
							pathLen = -pathLen
						print("Необходимое время на путь: " + str(pathLen / 100) + " секунд")
						time.sleep(pathLen / 100)
						pl.x = loc[2]
						pl.y = loc[3]
						enemies = []
						print("Автосохранение...")
						ui.save()
						break
					elif loc[7] == 0:
						print("Ты не открыл эту локацию")
						input()
			for strc in self.structures:
				if direction == strc[2].upper():
					if strc[6] == 1:
						pathLen = (pl.x + pl.y) - (strc[3][0] + strc[4][0])
						if pathLen < 0:
							pathLen = -pathLen
						print("Необходимое время на путь: " + str(pathLen / 100) + " секунд")
						time.sleep(pathLen / 100)
						pl.x = strc[3][0]
						pl.y = strc[4][0]
						enemies = []
						print("Автосохранение...")
						ui.save()
						break
					elif strc[6] == 0:
						print("Ты не открыл эту локацию")
						input()

		while pl.y < 1:
			pl.y += 1
		while pl.x < 1:
			pl.x += 1
		for t in quests.tradersList:
			t[1] -= 1
			if t[1] < 1:
				# t = quests.constTradersList[t[3]]
				quests.tradersList[quests.tradersList.index(t)] = quests.constTradersList[t[3]]

	def getLoc(self, pl):
		# retloc = [-1, "Лос-Анджелес", 0, 0, 1500, 5000, -1, 1]
		for loc in self.locationsCoords:
			if pl.x in range(loc[2], loc[4]) and pl.y in range(loc[3], loc[5]) and loc[6] == 0 and self.inDung == False:
				retloc = loc
				if loc[7] == 0:
					loc[7] = 1
					print("Новая локация открыта")
					time.sleep(1)
				break
			elif pl.x in range(loc[2], loc[4]) and pl.y in range(loc[3], loc[5]) and loc[6] == -1:
				retloc = loc
				break
			elif loc[6] == 1:
				if pl.x in range(loc[2], loc[4]) and pl.y in range(loc[3], loc[5]) and self.inDung == True:
					retloc = loc
					break
				if pl.x == loc[7] and loc[8] == pl.y:
					if self.inDung != True:
						print("Войти в данж?")
						print("1) Да")
						print("2) Нет")
						b = input()
						if int(b) == 1:
							self.inDung = True
							retloc = loc
							break
						elif int(b) == 2:
							pl.y -= 1
							pass
					else:
						print("Выйти?")
						print("1) Да")
						print("2) Нет")
						b = input()
						if int(b) == 1:
							self.inDung = False
							pl.y -= 1
							pass
						elif int(b) == 2:
							pl.y -= 1
							retloc = loc
							break
		return retloc

class NPC():
	def __init__(self):
		self.allQuests = [[0, "Принести оружие(203, 2)", "Принести оружие по координатам 203, 2"], [1, "Убийца в законе", "Убить 3 наемников Красного Орла"], 
						[2, "Перед битвой. II", "Принести 20 зелий здоровья"], [3, "Маленькая помощь", "Принести 5 концетрированных зелий здоровья"]] 
						# quest[id, name, description]
		self.dialogForQuest = [[0, "Генерал-полковник", [0, 1, 11], ["По координатам (203, 2) есть оружие, можешь принести?", "Так точно!", "У меня нет на это времени"], 1, 2], 
								[1, "Капрал Честнов", [0, 1, 11], ["Крансые Орлы много о себе возомнили, напомни им о нас. Убей парочку их наемников", "Хорошо", "У меня нет времени"], 1, 2], 
								[3, "Некромант", [0, 1, 11], ["Принеси мне 5 конц. зелий здоровья", "Без проблем", "Я сделаю это позже"], 1, 2]] 
								# dialog[questId, npcName, [question1, answer1, answer2...], idAnswerForAgreement, idAnswerForNo
								# 0 - question, 1 - answer, 11 - last answer
		self.npcList = [[0, "Босс", 1, 1], [1, "Генерал-полковник", 0, 0], [2, "Дипфельгаум", 3, 3], [3, "Рядовой Поджопкин", 0, 0], 
						[4, "Вор", 2, 2], [5, "Подрывник Клаус", 1, 1], [6, "Разведчик Вольскрем", 1, 1], [7, "Дядя Стёпа", 1, 1],
						[8, "Капрал Шпильдик", 1, 1], [9, "Биг Нигга", 2, 2], [10, "Наркоман", 2, 2], [11, "Пушечный Каджэм", 2, 2], 
						[12, "Рисковый", 2, 2], [13, "Бывалый", 2, 2], [15, "Сумашедший Френк", 2, 2], [16, "Иосиф Старфарен", 3, 3], 
						[17, "Клаус Шлипперген", 3, 3], [18, "Роберт Головорез", 3, 3], [19, "Томас Хруст", 3, 3], 
						[20, "Майор Жмот", 0, 0], [21, "Капрал Честнов", 0, 0], [22, "Сержант Взяточкин", 0, 0],
						[23, "Алекс Стулгманн", 0, 0], [24, "Томас Манн", 1, 1], [25, "Фреди Бешеный", 2, 2], [26, "Гредди Питерсон", 3, 3] ]
		# npc[id, name, locId(Where he), fracId]
		self.dialogList = [[0, 0, 1, [[0, 2, 0, "Чем вы занимаетесь здесь?", "Мы считаем что нынешняя власть бесполезна, мы хотим ее свергнуть."], 
									 [1, 1, 0, 0, "Могу ли я помочь вам?"] ]],
							[1, 0, 0, [[0, 2, 0, "Какова нынешняя ситуация?", "Ты серьезно думаешь что мы будем рассказывать тебе наши планы?"],
									   [1, 3, 45, "ENTERFRACTION", "Могу ли я вступить в вашу фракцию?", "Конечно, дружище, мы всегда рады тебе"]]],
							[2, 0, 3, [[0, 2, 0, "Кто ты?", "Я! Я... УВХХАВХВХАХВХАВХАХ"]]],
							[20, 0, 0, [[0, 2, 5, "Какой пароль от оружейного сейфа?", "0001... Так! Я тебе ничего не говорил! ЗАБУДЬ"]]],
							[21, 0, 0, [[0, 1, 1, 0, "Чем могу помочь?"]]],
							[23, 0, 0, [[0, 2, 0, "Кто ты?", "Ты прочитай вывеску, написано же, торговая лавка. Слепой..."], [1, 0, 0, "Что у тебя есть на продажу?"]]],
							] 
							# dialog[npcId, dialogType, idFrac, [[id, type, minNeedTrustLevel, questions], [id, type, idQuest(if type - 1), minNeedTrustLevel, question]], [idQuestions]] 
							# For basic: dialog[npcId, dialogType, idFrac, [[id, type, minTrustLevel, q, answer]], [idQuestions]]
							# For special: [nId, dType, idF, [[id, type, minTrustLevel, "command", q, answ]]]
							# idQuestions: 0 - trade, 1 - quest, 2 - basic, 3 - special
		self.questsInfo = [[0, 1, [[96, 5], [5,100]], -1, "Доставить оружие", 0, 1, 0, 0], [1, 0, 3, 2, [[96, 10], [101, 5], [5, 150]], "Убийца в законе", 0, 21],
							[2, 1, 5, 250, "Перед битвой. II", 0, 20, 0], [3, 1, 7, 1, "Маленькая помощь", 1, 5, 2]] # quest[id, type, reward(itemId), valReward, name] (types: 0 - killer, 1 - courier)
								     # For killer type - quest[id, type, val, enemyId, [reward, valReward], name, canGetAgain?, npcId]
								     # For courier type - quest[id, type, [reward, count], -1, name, requiredItemId, val, idNpc(Who got it), canGetAgain?]
		self.questBook = []
		self.fractions = [[-1, "None", [-1] ], [0, "Полиция", [1, 3, 20, 21, 22, 23] ], [1, "Красный Орел", [0, 5, 6, 7, 8] ], [2, "Ниггас Хрупперс", [4,9,10,11,12,13,15] ], 
						  [3, "Дипфельгаум и его наемники", [2, 16, 17, 18, 19] ] ]
		# fraction[id, name, [idsNPCInThisFraction]]
		self.arldyCompletedQuests = [] # idsQuests
		self.tradersList = [[23, 50, [[0, 2, 750], [17, 50, 10], [18, 15, 75], [19, 300, 2], [20, 200, 4], [21, 350, 2], [22, 150, 3], [1, 1, 1500]], 0 ]]
		self.constTradersList = [[23, 50, [[17, 50, 10], [18, 15, 75], [19, 300, 2], [20, 200, 4], [21, 350, 2], [22, 150, 3], [1, 1, 1500]], 0 ]]
		# trader[npcId, needTurnsForRenewItems, [[itemId, countItems, priceOneItem]]]

	def getFraction(self, iD):
		for f in self.fractions:
			if f[0] == iD:
				return f
				break
		return f

	def dialog(self, npcId, quests, pl, items):
		for npc in self.npcList:
			if npcId == npc[0]:
				for dialog in self.dialogList:
					if npcId == dialog[0]:
						idsQ = []
						for quest in self.questBook:
							if quest[1] == 1:
								if npcId == quest[7]:
									quests.questHandler(pl.inv, 1)
									idsQ.append(quest[0])
							if quest[1] == 0:
								if npcId == quest[7]:
									quests.questHandler(pl.inv, 0)
									idsQ.append(quest[0])
						print("========================")
						print("Имя персонажа: " + str(npc[1]))
						i = 0
						for question in dialog[3]:
							if question[2] <= pl.trustLevel[dialog[2]][1]:
								if question[1] == 0:
									print("{}) {}".format(question[0], question[3]))
								if question[1] == 1:
									for q in self.arldyCompletedQuests:
										print(q)
										for q1 in idsQ:
											if q1 == q:
												print("{}) {}".format(question[0], question[4]))
								if question[1] == 2:
									print("{}) {}".format(question[0], question[3]))
								if question[1] == 3:
									print("{}) {}".format(question[0], question[4]))
							i += 1
						b = input()
						if b != "":
							if int(b) > i:
								pass
							for q in dialog[3]:
								if int(b) == q[0]:
									if question[2] <= pl.trustLevel[dialog[2]][1]: 
										if q[1] == 0:
											ui.shop(pl, items, quests, npcId)
											break
										elif q[1] == 1:
											ui.quest(quests, q[2])
											break
										elif q[1] == 2:
											print(q[4])
											input()
											break
										elif q[1] == 3:
											print(q[5])
											if q[3] == "ENTERFRACTION":
												if pl.idFrac == -1:
													print("    Внимание! При вступлении в фракцию вы не сможете выйти из нее! Продолжть?")
													print("  1) Да")
													print("  2) Нет")
													b = input()
													if b != "":
														if int(b) == 1:
															pl.idFrac = dialog[2]
															print("Поздравляю со вступлением! Форму можно получить в складе. Вот ключ")
															input()
															if dialog[2] == 0:
																items.addItemToInv(pl, 16, 1)
														elif int(b) == 2:
															break
												else:
													print("Вы уже состоите в другой фракции")
											break
									else:
										print("Твой уровень доверия слишком низок")

	def nearNpc(self, currLoc):
		nearNpcList = []
		for npc in self.npcList:
			if npc[2] == currLoc[0]:
				nearNpcList.append(npc)
		return nearNpcList

	def questHandler(self, event, needType):
		for qst in self.questBook:
			# COURIER
			if needType == 1:
				if qst[1] == 1:
					for item in event: # Event = pl.inv
						if item[0] == qst[5] and item[3] > 0:
							delVal = qst[6]
							while item[3] < delVal:
								delVal -= 1
							items.delItemFromInv(pl, qst[5], delVal)
							qst[6] -= delVal
							if qst[6] < 1:
								print("Ты закончил квест " + str(qst[4]))
								for q in qst[2]:
									item = items.getItem(q[0])
									print("Ты получил " + str(item[1]))
									items.addItemToInv(pl, q[0], q[1])
								self.arldyCompletedQuests.append(qst[0])
								self.questBook.pop(self.questBook.index(qst))
								input()
								break							
			# KILLER
			if needType == 0:
				if qst[1] == 0:
					if event[0] == qst[3]: # Event = enemy
						qst[2] -= 1
						if qst[2] < 1:
							print("Ты закончил квест " + str(qst[6]))
							for i in qst[4]:
								item = items.getItem(i[0])
								print("Ты получил " + str(item[1]))
								items.addItemToInv(pl, i[0], i[1])
							self.questBook.pop(self.questBook.index(qst))
							input()
							break

	def getQuestInfo(self, quest):
		for q in self.allQuests:
			if q[0] == quest[0]:
				if quest[1] == 0:
					print(q[1])
					print("     Прогресс: {} Осталось".format(quest[2]))
				if quest[1] == 1:
					print(q[1])
					item = items.getItem(quest[5])
					for d in self.dialogForQuest:
						if d[0] == q[0]:
							npcName = d[1]
					print("     Прогресс: {} Осталось ({}, Для {})".format(quest[6], item[1], npcName))

class Items():
	def __init__(self):
		self.itemsList = [[0, "Пистолет USP", 2, 1, 0], [1, "Пистолет Desert Eagle", 2, 1, 0], [2, "AK 47", 2, 1, 0], [3, "Sawed off", 2, 1, 0],
						 [4, "Джинсы", 1, 1, 0], [5, "Монета", -1, 1], [6, "Кожаная куртка", 1, 1, 0], [7, "Сандали", 1, 1, 0], 
						 [8, "Деревянная дубинка", 2, 1, 0], [9, "Полицейская дубинка", 2, 1, 0], [10, "Электрошокер", 2, 1, 0], [11, "Полицейская фуражка", 1, 1, 0], 
						 [12, "Полицейская форма", 1, 1, 0], [13, "Полицейские штаны", 1, 1, 0], [14, "Стильные ботинки", 1, 1, 0],
						 [15, "Зелье улучшения", 0, 1], [16, "Ключ(Полицейский склад)", -1, 1], [17, "Бинт", 0, 1],
						 [18, "Аптечка", 0, 1], [19, "Патрон 9мм", -1, 1], [20, "Патрон 7.62мм", 0, 1], [21, "Патрон .45ACP", 0, 1], [22, "Патрон .44 Magnum", 0, 1],
						 [23, "Бронижелет Красного Орла", 1, 1, 0], [24, "Нижняя часть ЭкзоСкелета Красного Орла", 1, 1, 0], [25, "Резиновые сапоги", 1, 1, 0],[26, "Sвит0к т3л3п0ртaции", 4, 1],
						 [27, "Частичка зачарования BURN", -1, 1], [28, "Частичка зачарования STUN", -1, 1],
						 [96, "Доверие+ (Полиция)", -1, 1], [97, "Доверие+ (Красный Орел)", -1, 1], [98, "Доверие+ (Ниггас Хрупперс)", -1, 1], [99, "Доверие+ (Дипфельгаум и его наемники)", -1, 1],
						 [100, "Доверие- (Полиция)", -1, 1], [101, "Доверие- (Красный Орел)", -1, 1], [102, "Доверие- (Ниггас Хрупперс)", -1, 1], [103, "Доверие- (Дипфельгаум и его наемники)", -1, 1]] 
						 # item[id, name, type, count] (0 type - potions, 1 - armor, 2 - weapons, 3 - enchanted armor, 4 - scrolls)
					     # 2.1 - ench weapon [id, name, type, count, equip?, [enchId, enchName]]
					     # For armor and weapon type [id, name, type, count, equip?]
		self.equipmentListInfo = [[4, 1, 0.5, 4], [6, 1, 1, 3], [7, 1, 0, 5], [8, 2, -2, 0], [9, 2, -5, 0], [0, 2, -4, 0.1, 21], [1, 2, -5, 0.1, 22],
								  [10, 2, -4, 0], [3, 2, -8, 0], [11, 1, 1, 2], [12, 1, 3.5, 3], [13, 1, 1, 4], [14, 1, 0.5, 5], [2, 2, -6, 0.1, 20],
								  [23, 1, 3, 3], [24, 1, 4, 4], [25, 1, 5, 1]]
		# item[itemId, statId for change, value, type] (types: 2 - helmet, 3 - chestplate, 4 - leggings, 5 - boots, 0 - weapons, 0.1 - guns, 0.2 - enchanted weapon)
		# For gun [id, statId, val, type(0.1), needItemForShoot, minRangeForShoot]
		self.enchantesList = [[0, ["CHANGE STATS", 32, 0.1]], [1, ["STUN", [70, 74], 2]], [2, ["BURN", [10, 20], 1, -5]]] # ["STUN", [chance], turns, dmg("BURN")]]
		# ench[id, ["command", int]]
		self.descrEnchnts = [[0, "Изменяет информацию персонажа"], [1, "Оглушает противника"], [2, "Поджигает противника"]]
		self.potionsListInfo = [[15, 32, 0.01], [17, 0, 8], [18, 0, 65]]
		# item[itemId, statId for change, value]
		self.dropList = [] # dropItem[idItem, range]
		self.scrollsInfo = [[28, 0, -1, 3]] # EffectIds: 0 - tp
		# item[itemId, effect]
		# for tp effect [itemId, effectId, tpLocId, tpStrId(Can be None)]
		self.strDrop = [[0, 25, 30, [1, 1]], [5, 10, 50, [1, 250]], [1, 61, 64, [1, 1]] ]
		# [itemId, minChance, maxChance, [mincount, maxcount]]
		self.plEnchants = []
		# [enchId, name, lvl, needWorldTrustForEnch, needMoney]
		self.learnEnchantes = [[1, "STUN", 0.0, 0.3, 1000], [2, "BURN", 0.0, 0.4, 1200]]
		# [enchId, name, progress, needWorldTrustForEnch, needMoney]
		self.equipFractions = [[0, 0, 10, [[0, 1, 1], [11, 1, 1], [12, 1, 1,], [13, 1, 1], [7, 1, 1], [5, 20, 0]] ]]
		# [fracId, minPlLvlForEquip, maxpllvlforequip, inv[[itemId, col, equip?]]]

	def enchUse(self, enchant, mob, isReverse, itemId):
		if enchant[1][0] == "CHANGE STATS":
			if isReverse:
				mob.changeStats(enchant[1][1], -enchant[1][2])
			else:
				mob.changeStats(enchant[1][1], enchant[1][2])
		if enchant[1][0] == "STUN":
			eff = [itemId, enchant[1]]
			if isReverse:
				mob.effects.pop(mob.effects.index(eff))
			else:
				mob.effects.append(eff)
		if enchant[1][0] == "BURN":
			eff = [itemId, enchant[1]]
			if isReverse:
				mob.effects.pop(mob.effects.index(eff))
			else:
				mob.effects.append(eff)
	def upLvlEnch(self):
		for lEnch in self.learnEnchantes:
			if lEnch[2] > 99.9:
				lEnch[2] -= 100.0
				c = True
				if self.plEnchants != []:
					for plE in self.plEnchants:
						if plE[0] == lEnch[0]:
							self.plEnchants[self.plEnchants.index(plE)][2] += 1
							c = False
				elif c == True:
					e = [lEnch[0], lEnch[1], 1, lEnch[3], lEnch[4]]
					self.plEnchants.append(e)
				print("Уровень зачарования {} был поднят на 1".format(lEnch[1]))
				input()

	def getInvDec(self, decId, pl, loc):
		strc = map1.getStructure(pl, loc)
		for dec in map1.decor:
			if dec[0] == strc[1]:
				if dec[1] == decId:
					if dec[3] == 0:
						if dec[4] != []:
							for item in dec[4]:
								i = self.getItem(item[0])
								if i[0] != -1: print("{}) {} (В количестве {} штук)".format(i[0], i[1], item[1]))
							print("Введите номер предмета или 'взять всё'")
							b = input().upper()
							if re.search('ВЗЯТЬ ВСЁ', b):
								if b != "":
									for item in dec[4]:
										items.addItemToInv(pl, item[0], item[1])
									dec[4] = []
									if dec[1] == 2:
										pl.trustLevel[0][1] -= 20
								break
							else:
								for l in ui.letters:
									b = b.replace(l, "")
								b = b.replace(" ", "")
								if b != "":
									for item in dec[4]:
										if int(b) == item[0]:
											items.addItemToInv(pl, item[0], item[1])
											dec[4].pop(dec[4].index(item))
											break
						else:
							print(dec[2] + " пуст")
							input()
					if dec[3] == 1:
						print("Введите пароль")
						b = input()
						if b == dec[5]:
							if dec[4] != []:
								for item in dec[4]:
									i = self.getItem(item[0])
									if i[0] != -1: print("{}) {} (В количестве {} штук)".format(i[0], i[1], item[1]))
								print("Введите номер предмета или 'взять всё'")
								b = input().upper()
								if re.search('ВЗЯТЬ ВСЁ', b):
									if b != "":
										for item in dec[4]:
											items.addItemToInv(pl, item[0], item[1])
										dec[4] = []
									break
								else:
									for l in ui.letters:
										b = b.replace(l, "")
									b = b.replace(" ", "")
									if b != "":
										for item in dec[4]:
											if int(b) == item[0]:
												items.addItemToInv(pl, item[0], item[1])
												dec[4].pop(dec[4].index(item))
												break
							else:
								print(dec[2] + " пуст")
								input()
						else:
							print("Неверный пароль")
							input()
					if dec[3] == 2:
						if pl.checkItem(dec[5]) == True:
							if dec[4] != []:
								for item in dec[4]:
									i = self.getItem(item[0])
									if i[0] != -1: print("{}) {} (В количестве {} штук)".format(i[0], i[1], item[1]))
								print("Введите номер предмета или 'взять всё'")
								b = input().upper()
								if re.search('ВЗЯТЬ ВСЁ', b):
									if b != "":
										for item in dec[4]:
											items.addItemToInv(pl, item[0], item[1])
										dec[4] = []
										if dec[1] == 2:
											pl.trustLevel[0][1] -= 20
									break
								else:
									for l in ui.letters:
										b = b.replace(l, "")
									b = b.replace(" ", "")
									if b != "":
										for item in dec[4]:
											if int(b) == item[0]:
												items.addItemToInv(pl, item[0], item[1])
												dec[4].pop(dec[4].index(item))
												break
							else:
								print(dec[2] + " пуст")
								input()
						else:
							print("Вам нужен ключ")
							input()

	def getItem(self, iD):
		item = [-1, "None", -1, 0]
		for item in self.itemsList:
			if(iD == item[0]):
				return item
				break
		return item
	def getEnchItem(self, itemId): # get descrp enchant and ench name for item
		ret = ["UNKNOWN", "UNKNOWN"]
		for item in self.enchEquipListInfo:
			if item[0] == itemId:
				for ench in self.enchantesList:
					if ench[0] == item[2]:
						for desc in self.descrEnchnts:
							if desc[0] == ench[0]:
								ret = [ench[1][0], desc[1]]
								break
				break
		return ret

	def useitem(self, idSlot, pl):
		for item in self.itemsList:
			if(pl.inv[idSlot][0] == item[0]):
				if(pl.inv[idSlot][3] > 0):
					if(pl.inv[idSlot][2] == -1):
						print("Этот предмет не используемый")
						input()
						break
					# POTIONS
					if(pl.inv[idSlot][2] == 0):
						for potion in self.potionsListInfo:
							if potion[0] == pl.inv[idSlot][0]:
								pl.changeStats(potion[1], potion[2])
								pl.inv[idSlot][3] -= 1 
								break
					# ARMOR
					elif(pl.inv[idSlot][2] == 1):
						if(pl.inv[idSlot][4] == 1): # Not equiped
							for equipment in self.equipmentListInfo:
								if(equipment[0] == pl.inv[idSlot][0]):
									pl.changeStats(equipment[1], -equipment[2])	
									pl.equipSlots[equipment[3]] = -1
									break
							pl.inv[idSlot][4] = 0
							break
						if(pl.inv[idSlot][4] == 0): # Equiped
							for equipment in self.equipmentListInfo:
								if(equipment[0] == pl.inv[idSlot][0]):
									if pl.equipSlots[equipment[3]] == -1:
										pl.inv[idSlot][4] = 1
										pl.equipSlots[equipment[3]] = pl.inv[idSlot][0]
										pl.changeStats(equipment[1], equipment[2])
									else:
										print("Вы уже носите другую броню, сначала снимите ее")
									break
							break
					# ENCHANTED ARMOR
					elif(pl.inv[idSlot][2] == 3):
						if(pl.inv[idSlot][4] == 1): # Not equiped
							for equipment in self.enchEquipListInfo:
								if(equipment[0] == pl.inv[idSlot][0]):
									pl.changeStats(equipment[4], -equipment[5])	
									pl.equipSlots[equipment[1]] = -1
									for ench in self.enchantesList:
											if ench[0] == equipment[2]:
												items.enchUse(ench, pl, True, pl.inv[idSlot][0])
												break
									break
							pl.inv[idSlot][4] = 0
							break
						if(pl.inv[idSlot][4] == 0): # Equiped
							for equipment in self.enchEquipListInfo:
								if(equipment[0] == pl.inv[idSlot][0]):
									if pl.equipSlots[equipment[1]] == -1:
										pl.inv[idSlot][4] = 1
										pl.equipSlots[equipment[1]] = pl.inv[idSlot][0]
										pl.changeStats(equipment[4], equipment[5])
										for ench in self.enchantesList:
											if ench[0] == equipment[2]:
												items.enchUse(ench, pl, False, pl.inv[idSlot][0])
												break
									else:
										print("Вы уже носите другую броню, сначала снимите ее")
									break
							break
					# WEAPON
					elif(pl.inv[idSlot][2] == 2):
						if(pl.inv[idSlot][4] == 1): # Equiped
							for equipment in self.equipmentListInfo:
								if(equipment[0] == pl.inv[idSlot][0]):
									if pl.equipSlots[0] == pl.inv[idSlot][0]:
										pl.equipSlots[0] = -1
										pl.changeStats(equipment[1], -equipment[2])
										break
									elif pl.equipSlots[1] == pl.inv[idSlot][0]:
										pl.equipSlots[1] = -1
										pl.changeStats(equipment[1], -equipment[2])
										break
							pl.inv[idSlot][4] = 0
							break
						elif(pl.inv[idSlot][4] == 0): # Not equiped
							for equipment in self.equipmentListInfo:
								if(equipment[0] == pl.inv[idSlot][0]):
									if pl.equipSlots[0] == -1:
										pl.equipSlots[0] = pl.inv[idSlot][0]
										pl.changeStats(equipment[1], equipment[2])
										break
									elif pl.equipSlots[1] == -1:
										pl.equipSlots[1] = pl.inv[idSlot][0]
										pl.changeStats(equipment[1], equipment[2])
										break
									else:
										print("Вы уже носите другое оружие, сначала снимите его")
									break
							pl.inv[idSlot][4] = 1
							break
					# ENCHANTED WEAPON
					elif(pl.inv[idSlot][2] == 2.1):
						if(pl.inv[idSlot][4] == 1): # equiped
							for equipment in self.equipmentListInfo:
								if(equipment[0] == pl.inv[idSlot][0]): # If this item
									if pl.equipSlots[0] == pl.inv[idSlot][0]:
										pl.equipSlots[0] = -1
										pl.changeStats(equipment[1], -equipment[2])
										break
									elif pl.equipSlots[1] == pl.inv[idSlot][0]:
										pl.equipSlots[1] = -1
										pl.changeStats(equipment[1], -equipment[2])
										break
									for ench in self.enchantesList:
											if ench[0] == pl.inv[idSlot][5][0]:
												items.enchUse(ench, pl, True, pl.inv[idSlot][0])
												break
									break
							pl.inv[idSlot][4] = 0
							break
						if(pl.inv[idSlot][4] == 0): # not Equiped
							for equipment in self.equipmentListInfo:
								if(equipment[0] == pl.inv[idSlot][0]):
									if pl.equipSlots[0] == -1:
										pl.equipSlots[0] = pl.inv[idSlot][0]
										pl.changeStats(equipment[1], equipment[2])
										for ench in self.enchantesList:
											if ench[0] == pl.inv[idSlot][5][0]:
												items.enchUse(ench, pl, False, pl.inv[idSlot][0])
												break
										break
									elif pl.equipSlots[1] == -1:
										pl.equipSlots[1] = pl.inv[idSlot][0]
										pl.changeStats(equipment[1], equipment[2])
										for ench in self.enchantesList:
											if ench[0] == pl.inv[idSlot][5][0]:
												items.enchUse(ench, pl, False, pl.inv[idSlot][0])
												break
										break
									else:
										print("Вы уже носите другое оружие, сначала снимите его")
									break
							break
					# SCROLS
					elif pl.inv[idSlot][2] == 4:
						if(pl.inv[idSlot][3] > 0):
							for scroll in self.scrollsInfo:
								if pl.inv[idSlot][0] == scroll[0]:
									# TP TYPE
									if scroll[1] == 0:
										for loc in map1.locationsCoords:
											if loc[0] == scroll[2]:												
												pl.inv[idSlot][3] -= 1
												if scroll[3] != None:
													for strc in map1.structures:
														if strc[1] == scroll[3]:
															pl.x = strc[3][0]
															pl.y = strc[4][0]
												elif scroll[3] == None:
													pl.x = loc[2]
													pl.y = loc[3]
												break
				else:
					print("У вас нет такого предмета")
			else:
				pass
		return pl
	
	def useEnemyItem(self, idSlot, e): # e - enemy
		for item in self.itemsList:
			if(e[2][idSlot][0] == item[0]):
				if(e[2][idSlot][3] > 0):
					# ARMOR
					if(e[2][idSlot][2] == 1):
						if(e[2][idSlot][4] == 1): # Not equiped
							for equipment in self.equipmentListInfo:
								if(equipment[0] == e[2][idSlot][0]):
									enemyH.changeStats(equipment[1], -equipment[2], e)	
									e[3][equipment[3]] = -1
									break
							e[2][idSlot][4] = 0
							break
						if(e[2][idSlot][4] == 0): # Equiped
							for equipment in self.equipmentListInfo:
								if(equipment[0] == e[2][idSlot][0]):
									if e[3][equipment[3]] == -1:
										e[2][idSlot][4] = 1
										e[3][equipment[3]] = e[2][idSlot][0]
										enemyH.changeStats(equipment[1], equipment[2], e)
									else:
										pass
										# print("Вы уже носите другую броню, сначала снимите ее")
									break
							break
					
					# WEAPON
					elif(e[2][idSlot][2] == 2):
						if(e[2][idSlot][4] == 1): # Equiped
							for equipment in self.equipmentListInfo:
								if(equipment[0] == e[2][idSlot][0]):
									if e[3][0] == e[2][idSlot][0]:
										e[3][0] = -1
										enemyH.changeStats(equipment[1], -equipment[2], e)
										break
									elif e[3][1] == e[2][idSlot][0]:
										e[3][1] = -1
										enemyH.changeStats(equipment[1], -equipment[2], e)
										break
							e[2][idSlot][4] = 0
							break
						elif(e[2][idSlot][4] == 0): # Not equiped
							for equipment in self.equipmentListInfo:
								if(equipment[0] == e[2][idSlot][0]):
									if e[3][0] == -1:
										e[3][0] = e[2][idSlot][0]
										enemyH.changeStats(equipment[1], equipment[2], e)
										break
									elif e[3][1] == -1:
										e[3][1] = e[2][idSlot][0]
										enemyH.changeStats(equipment[1], equipment[2], e)
										break
									else:
										pass
										# print("Вы уже носите другое оружие, сначала снимите его")
									break
							e[2][idSlot][4] = 1
							break

	def addItemToInv(self, mob, iD, count, mobType):
			arldyHave = False
			if mobType == 0: # If player
				print("Получен {} в ".format(self.getItem(iD)[1]) + str(len(mob.inv)) + " слот (в количестве: {})".format(count))
				if iD == 5:
					mob.money += count
				elif iD == 96:
					mob.trustLevel[0][1] += count
					mob.worldTrustLevel += count / 100
				elif iD == 97:
					mob.trustLevel[1][1] += count
					mob.worldTrustLevel += count / 100
				elif iD == 98:
					mob.worldTrustLevel += count / 100
					mob.trustLevel[2][1] += count
				elif iD == 99:
					mob.worldTrustLevel += count / 100
					mob.trustLevel[3][1] += count
				elif iD == 100:
					mob.worldTrustLevel -= count / 100
					mob.trustLevel[0][1] -= count
				elif iD == 101:
					mob.worldTrustLevel -= count / 100
					mob.trustLevel[1][1] -= count
				elif iD == 102:
					mob.worldTrustLevel -= count / 100
					mob.trustLevel[2][1] -= count
				elif iD == 103:
					mob.worldTrustLevel -= count / 100
					mob.trustLevel[3][1] -= count
				elif iD == 27:
					self.learnEnchantes[1][2] += count
				elif iD == 28:
					self.learnEnchantes[0][2] += count
				else:
					for item in mob.inv:
						for i in items.itemsList:
							if item[0] == i[0] and i[0] == iD and item[2] == i[2]:
								arldyHave = True
								item[3] += count
					if arldyHave == False:
						currItem = items.getItem(iD)
						currItem[3] = count
						mob.inv.append(currItem)
					else:
						pass
			elif mobType == 1:
				print("Получен {} в ".format(self.getItem(iD)[1]) + str(len(mob[2])) + " слот (в количестве: {})".format(count))
				for item in mob[2]:
					for i in items.itemsList:
						if item[0] == i[0] and i[0] == iD and item[2] == i[2]:
							arldyHave = True
							item[3] += count
				if arldyHave == False:
					currItem = items.getItem(iD)
					currItem[3] = count
					mob[2].append(currItem)
				else:
					pass
	def delItemFromInv(self, mob, iD, val): # iD = idItem
		for slot in mob.inv:
			if slot[0] == iD:
				if slot[3] > 1:
					slot[3] -= 1
					break
				else:
					mob.inv.pop(mob.inv.index(slot))

	def getInv(self, mob):
		numItem = 0
		for item in mob.inv:
			if item[3] < 1:
				mob.inv.pop(mob.inv.index(item))
			if not item[2] == 1 and item[2] != 2 and item[2] != 2.1 and item[2] != 3:
				print("{}) {} (кол-во: {})".format(numItem, item[1], item[3]))
			elif item[2] == 1 or item[2] == 2:
				if item[4] == 0:
					print(str(numItem) + ") " + str(item[1]))
				elif item[4] == 1:
					print("{}) {} (экипирован)".format(numItem, item[1]))
			elif item[2] == 2.1 or item[2] == 3:
				print("{}) {} (кол-во: {}) \n   Зачарование: {}".format(numItem, item[1], item[3], item[5][0]))
			numItem += 1
		numItem = 0
		print("======Экипировка======")
		for item in mob.equipSlots:
			if item != 0:
				for itm in self.itemsList:
					if item == int(itm[0]):
						if numItem == 0:
							print("В правой руке: " + str(itm[1]))
						if numItem == 1:
							print("В левой руке: " + str(itm[1]))
						if numItem == 2:
							print("На голове: " + str(itm[1]))
						if numItem == 3:
							print("На теле: " + str(itm[1]))
						if numItem == 4:
							print("На ногах: " + str(itm[1]))
						if numItem == 5:
							print("На ступах: " + str(itm[1]))
			numItem += 1

	def setDrop(self, enemy, pl):
		r = randrange(0, 100)
		dropEnemy = []
		i = 0
		for i in range(0, 2):
			for drop in self.dropList:
				if r >= drop[1] and r <= drop[2]:
					for item in items.itemsList:
						if drop[0] == item[0]:
							currItem = [item[0]] # id
							if item[0] == 5: # If coins
								if pl.idCharacter == 3:
									items.addItemToInv(pl, 5, randrange(10, 30))
								else:
									items.addItemToInv(pl, 5, randrange(1, 20))
								currItem = [-1]
							else:
								currItem.append(1) # count
							dropEnemy.append(currItem) # idItem, count
		pl.xp += randrange(1, 7)
		pl.money += randrange(0, 10)
		return dropEnemy

class Handler():
	def __init__(self):
		self.maxSlotsEnemy = 5
		self.slots = []
		for i in range(self.maxSlotsEnemy): self.slots.append(0)

	def spawnEnemy(self, loc):
		for i in range(self.maxSlotsEnemy):
			self.slots[i] = Enemy()
			self.slots[i].initEnemy(loc)
			for eL in items.equipFractions:
				if eL[0] == self.slots[i].info[3]:
					if pl.lvl in range(eL[1], eL[2]):
						for item in eL[3]:
							self.slots[i].inv.append(items.getItem(item[0]))
							if item[2] == 1:
								for eq in items.equipmentListInfo:
									if eq[0] == item[0]:
										self.slots[i].changeStats(eq[1], eq[2])
										break
	def getRangeToEnemy(self, slotId):
		return -(self.slots[slotId].coords[0] - pl.x) + (self.slots[slotId].coords[1] - pl.y)
	def getStatsEnemy(self, slotId):
		return self.slots[slotId].info[2]
	def getEnemyInfo(self, slotId):
		return self.slots[slotId].info
	def changeStatsEnemy(self, slotId, statId, value):
		self.slots[slotId].changeStats(statId, value)

class Enemy():
	def __init__(self):
		self.enemiesLists = [ [0, 50, 0, 1, 0, [ [0, "Полицейский", [40, 2, -5], 0, -30, 0], [1, "Чувак", [60, 4, -5], -1, 0, None]]],
					 	[0, 50, 2, 3, 1, [[2, "Наемник(Красный Орел)", [65, 3, -10], 1, 0, 1], [3, "Мирный(Красный Орел", [20, 1, -3], 1, -10, 1]]],
					 	[0, 50, 4, 5, 0, [[4, "Мирный(Полиция)", [35, 2, -4], 0, 0, 0], [5, "Вооруженный мирный", [35, 3, -7], 0, -2, 0]]],
					 	[0, 50, 5, 6, -2, [[5, "Странник", [35, 2, -4], -1, 0, -2], [6, "Вооруженный странник", [50, 2, -6], -1, 0, -2] ]]]
		# list enemies[minLvlNeed, maxLvlNeed, minIdEnemy, maxIdEnemy, locSpawn, [enemy[id, name, stats[startHp, defense, atk], fracId, minTrustForSpawn, locSpawnId], enemy2, enemy3... ] ]

	def getInfoEnemy(self, iD):
		for lst in self.enemiesLists:
			for enemy in lst[5]:
				if enemy[0] == iD:
					return enemy

	def clearEnemy(self,loc):
		self.info = [-1, None]
		self.effects = []
		self.inv = []
		self.equipSlots = [-1,-1,-1,-1,-1,-1]

	def initEnemy(self, loc):
		self.info = [-1, None]
		self.effects = []
		self.coords = [0, 0]
		self.inv = []
		self.equipSlots = [-1,-1,-1,-1,-1,-1]
		for enemylist in self.enemiesLists:
			if pl.lvl in range(enemylist[0], enemylist[1]) and loc[0] == enemylist[4]:
				idEnemy = randrange(enemylist[2], enemylist[3])
				for enemy in enemylist[5]:
					if enemy[5] != None:
						if loc[0] == enemy[5]:
							if enemy[3] != -1:
								if enemy[4] >= pl.trustLevel[enemy[3]][1]:
									if enemy[0] == idEnemy:
										self.info = enemy
										break
							else:
								self.info = enemy
								break
					else:
						if enemy[3] != -1:
							if enemy[4] >= pl.trustLevel[enemy[3]][1]:
									if enemy[0] == idEnemy:
										self.info = enemy
										break
							else:
								info = enemy
								break # Get enemy
						elif enemy[3] == -1:
							if enemy[0] == idEnemy:
								self.info = enemy
		if self.info[0] != -1:
			self.coords[0] = pl.x + randrange(-50, 50)
			if self.coords[0] < 1:
				self.coords[0] = 1
			self.coords[1] = pl.y + randrange(-50, 50)
			if self.coords[1] < 1:
				self.coords[1] = 1

	def setInv(self, num):
		iC = 0
		for equip in items.equipFractions:
			if self.info[3] == equip[0] and pl.lvl in range(equip[1], equip[2]):
				for item in equip[3]:
					self.invE.append(item)
					for i in self.invE:
						self.inv.append(items.getItem(i[0]))
					if item[2] == 1:
						print(self.inv[iC])
						items.useitem(iC, enemies[num])
					iC += 1

	def changeStats(self, statId, val):
		if(statId == 0):
			self.info[2][0] += val
		elif(statId == 1):
			self.info[2][1] += val
		elif(statId == 2):
			self.info[2][2] += val

class Player():
	def __init__(self, inv, itemsNames, stats):
		self.inv = inv
		self.itemsNames = itemsNames
		self.hp = stats[0]
		self.defense = stats[1] 
		self.atk = stats[2]
		self.money = 0
		self.equipSlots = [-1,-1,-1,-1,-1,-1] # item[id] (Right arm, left arm, helmet, chestplate, leggings, boots)
		self.lvl = 1
		self.points = 0 + stats[4]
		self.xp = 0
		self.totalXp = 0
		self.needXp = 100
		self.idCharacter = stats[3]
		self.x = 17
		self.y = 1
		self.speed = 3
		self.buffs = [[1, 1], [2, 1]] # buff[statId, value(coeff)]
		self.idFrac = -1
		self.trustLevel = [[0, 0], [1, 0], [2, 0], [3, 0]] # [fracId, lvl(-100 - 100)]
		self.worldTrustLevel = 0.0
		self.effects = []
		self.skills = [[0, "Зачарование", 0, 0], [1, "Оружие", 0, 0]]
		# [id, name, lvl, progressToNextLvl]

	def upLvl(self):
		self.lvl += 1
		self.xp -= self.needXp
		self.needXp += (self.needXp / 2 - randrange(0,50))

	def usePoints(self):
		if self.points > 0:	
			print(" У тебя есть {} очков прокачки".format(self.points))
			print(" Ты можешь использовать очки для:")
			print("1) +0.02 коэф. к атаке")
			print("2) +0.02 коэф. к защите")
			print("3) Продать одно и получить 450 монет")
			b = input()
			if int(b) == 1:
				pl.changeStats(32, 0.02)
				self.points -= 1
			elif int(b) == 2:
				self.points -= 1
				pl.changeStats(31, 0.02)
			elif int(b) == 3:
				self.points -= 1
				self.money += 450

	def hasItem(self, iD):
		for item in items.itemsList:
			if item[0] == iD:
				for i in self.inv:
					if item[0] == i[0] and item[0] == iD and item[3] > 0:
						return True
	def getItem(self, iD):
		for item in items.itemsList:
			if item[0] == iD:
				for i in self.inv:
					if item[0] == i[0] and item[0] == iD:
						return item
	def hasItemEquip(self, idSlot):
		if self.equipSlots[idSlot] == -1:
				return False
		for item in items.itemsList:
			if self.equipSlots[idSlot] == item[0]:
				return True
				break
	def getItemEquip(self, idSlot):
		if self.equipSlots[idSlot] == -1:
				return False
		for item in items.itemsList:
			if self.equipSlots[idSlot] == item[0]:
				return item
				break
	
	def getStats(self, statId):
		statsPl = [self.hp, self.defense, self.atk]
		return statsPl[statId]
	def changeStats(self, statId, val):
		if(statId == 0):
			self.hp += val 
		elif(statId == 1):
			val *= self.buffs[0][1]
			self.defense += val
			self.defense = round(self.defense, 2)
		elif(statId == 2):
			val *= self.buffs[1][1]
			self.atk += val
			self.atk = round(self.atk, 2)
		elif statId == 31:
			self.buffs[0][1] += val
		elif statId == 32:
			self.buffs[1][1] += val

	def playerAttack(self, enemy):
		enemy.changeStats(0, self.atk)
		print(str(self.atk) + " hp to enemy")

class UI():
	def __init__(self):
		self.letters = ['Й','Ц','У','К','Е','Н','Г','Ш','Щ','З',"Х",'Ъ','Ф','Ы','В','А','П',
		   'Р','О','Л','Д','Ж','Э','Я','Ч', 'С','М','И','Т','Ь','Б','Ю','Ё','й','ц','у','к','е','н','г','ш','щ','з',
		   'х','ъ','ф','ы','в','а','п','р', 'о', 'л','д','ж','э','я','ч',
		   'с','м','и','т','ь','б','ю','ё', '[', ']', '{', '}','!','@','#',
		   '$',"%","^",":",";","&","*","(",")","-","+","_","=","/","|"]
		self.specLetters = [' ', '[', ']', '{', '}','!','@','#','$',"%","^",":",";","&","*","(",")","-","+","_","=","/","|"]
		# self.scenes = [[0, "Начало", [ [ ["3 Июня 2019 Год, мексиканец - Кэмэл Аригато 19 лет. Лос-Анджелес.", "Я устроился работать уборщиком чтобы хоть как-то зарабатывать себе на жизнь",
					   				  # "14 Июня 2019 Год. После очередного дня я пошел снять комнату в одном хостеле.", "Под мостом собралась толпа людей с плакатами. Некоторые из них были вооружены. Они кричали 'Лос-Анджелес должен быть независимым городом Америки'. ",
					   				   # "Перед ними собралась орда отрядов спец. назначения", "*Выстрел*", "*Человек упал замертво*", "Началась маштабная битва."], ["1) Присоединиться к митингующим", "2) Бежать в хостел", "3) Пробежать под мостом", "4) Обойти митингующих"] ] ], 
					   				 # [[1, "Кэмэл надел на себя какие-то тряпки, отодрал палку и ринулся в атаку!", "Ему удалось не попасть под пули, т.к. полиция отступала за кусты, которые находились под мостом.", "Кэмэл решил побежать первым со словами 'ЗА НЕЗАВИСИМОСТЬ! ЗА СВОБОДУ СЛОВА!'", "Пробежав через кусты он в одно мгновение увидел летящую в его лицо дубинку из кустов и был вырублен."],
					   				  # [2, "Кэмэл побежал в хостел. Но там его подстерегали.", "Там собралась шайка мародёров с пистолетами. 'Эй, ты! Карманы выворачивай! Не то мозги тебе в кашу превращу!' - сказвл один из ниггеров"]] ] ]
		# [id, name, [[text], [actions]], [[id, text_after_action]]]
		# scen = json.load(open("scenes.json"))
		# print(scen)
		# input()
		# with open("scenes.json", "w") as f:
		# 	scen = json.dump(scen, f, ensure_ascii=False)
		# k = json.load(scen)
		# print(scen)
		# input()

	def save(self):
		plStats = [pl.hp, pl.atk, pl.defense, pl.money, pl.points, pl.lvl, pl.xp, pl.needXp, pl.idCharacter, pl.x, pl.y, pl.speed, pl.buffs]
		plInv = [pl.inv, pl.equipSlots]
		plQuests = quests.questBook
		plChunks = map1.chunks
		plLocUnlocked = []
		appLoc = []
		for loc in map1.locationsCoords:
			if loc[6] == 0:
				appLoc = [loc[0], loc[7]]
			plLocUnlocked.append(appLoc)
		with open('data', 'wb') as f:
			pickle.dump(plStats, f)
			pickle.dump(plInv, f)
			pickle.dump(plQuests, f)
			pickle.dump(plChunks, f)
			pickle.dump(plLocUnlocked, f)
			pickle.dump(map1.decor, f)
			pickle.dump(quests.tradersList, f)
			pickle.dump(pl.effects, f)

	def catScene(self, iD):
		os.system("cls")
		os.system("clear")
		for scene in self.scenes:
			if scene[0] == iD:
				print("          " + str(scene[1]))
				for text in scene[2]:
					for sentence in text[0]:
						print("  " + sentence)
						input()
					i = 0
					for act in text[1]:
						print(act)
						i += 1
					b = input()
					if int(b) in range(i):
						for TAA in scene[3]:
							if TAA[0] == int(b):
								for sent in TAA:
									print(str(sent))
									input()
		input()

	def menu(self):
		os.system("cls")
		os.system("clear")
		print("Короткое обучение :)")
		print("   Для атаки введите:")
		print("'Атаковать' И номер моба")
		print("   Для использования чего либа из инвентаря:")
		print("'использовать' и номер слота инвентаря")
		print("   Для передвижения по карте:")
		print("'вверх' or 'вниз' or 'влево' or 'вправо'")
		print("   Для сохранения введите:")
		print("'сохранить'")
		print("   Для отображения чего-либо:")
		print("'Показать (параметр)', Например: 'Показать НПС'")
		print("   Чтобы начать разговор с НПС:")
		print("'Диалог' И номер НПС(Чтобы узнать его введите 'Показать НПС')")
		print("   Для быстрого передвижения:")
		print("'Идти в' и название локации")
		print("")
		print("======================================")
		print("(Выберите цифру)")
		print("         1. НОВАЯ ИГРА")
		print("         2. Загрузить последнее сохранение")
		b = input()
		if int(b) == 1:
			print("Выберите персонажа:")
			print("1) Коллер(коэф 0,5 к атаке)")
			print("2) Дзен-ди(коэф 0,5 к защите)")
			print("3) Бранер(коэф 0,5 к получению золота)")
			b = input()
			if int(b) == 1:
				chrctr = 1
				bonus_points = 2
			if int(b) == 2:
				chrctr = 2
				bonus_points = 3
			if int(b) == 3:
				chrctr = 3
				bonus_points = 1
			# pl = Player([], items.itemsList, [100,5,-10,chrctr,bonus_points])
			pl.hp = 100
			pl.defense = 5
			pl.atk = -10
			pl.idCharacter = chrctr
			if pl.idCharacter == 1:
				pl.changeStats(32, 0.5)
			if pl.idCharacter == 2:
				pl.changeStats(31, 0.5)
			pl.points += bonus_points
		elif int(b) == 2 and os.path.isfile('save.txt') == True:
			# pl = Player([], items.itemsList, [0,0,0,0,0])
			if os.path.isfile('data') == False:
				print("Файл сохранения не существует")
				input()
				quit()
			with open('data', 'rb') as f:
				plStats = pickle.load(f)
				plInv = pickle.load(f)
				plQuests = pickle.load(f)
				plChunks = pickle.load(f)
				plLocUnlocked = pickle.load(f)
				map1.decor = pickle.load(f)
				quests.tradersList = pickle.load(f)
				pl.effects = pickle.load(f)
			pl.hp = plStats[0]
			pl.atk = plStats[1]
			pl.defense = plStats[2]
			pl.money = plStats[3]
			pl.points = plStats[4]
			pl.lvl = plStats[5]
			pl.xp = plStats[6]
			pl.needXp = plStats[7]
			pl.idCharacter = plStats[8]
			pl.x = plStats[9]
			pl.y = plStats[10]
			pl.speed = plStats[11]
			pl.buffs = plStats[12]
			pl.inv = plInv[0]
			pl.equipSlots = plInv[1]
			quests.questBook = plQuests
			map1.chunks = plChunks
			for loc in plLocUnlocked:
				for lc in map1.locationsCoords:
					if loc != []:
						if loc[0] == lc[0]:
							if lc[6] == 0: 
								lc[7] = loc[1]

	def quest(self, quests, iD):
		for dialog in quests.dialogForQuest:
			if dialog[0] == iD:
				cntinue = True
				for q in quests.arldyCompletedQuests:
					if iD == q:
						cntinue = False
				for q in quests.questBook:
					if q[0] == iD:
						cntinue = False
				if cntinue == True:
					QorA = dialog[2]
					i = 0
					for QandA in dialog[3]:
						if QorA[i] == 0:
							print(QandA)
						elif QorA[i] == 1:
							print(str(i) + ") " + str(QandA))
						elif QorA[i] == 11:
							print(str(i) + ") " + str(QandA))
							b = input()
							if int(b) == dialog[4]:
								quests.questBook.append(quests.questsInfo[dialog[0]])
							elif int(b) == dialog[5]:
								pass
						i += 1
				else:
					print("You can't get this quest")
					input()

		# print(quests.allQuests[iD][1])
		# print("=====================")
		# print(quests.allQuests[iD][2])
		# print("=====================")
		# print("1) Accept")
		# print("2) Decline")
		# b = input()
		# if int(b) == 1:
		# 	for q in quests.questsInfo:
		# 		if iD == q[0]:
		# 			qId = q[0]
		# 	quests.questBook.append(quests.questsInfo[qId])
		# if int(b) == 2:
		# 	pass

	def enchant(self):
		os.system("cls")
		os.system("clear")
		for lEnch in items.learnEnchantes:
			print("  Зачарование {} изучено на {}/100".format(lEnch[1], lEnch[2]))
		print("=====================")
		print("Вы можете зачаровать:")
		for item in pl.inv:
			if item[2] == 1 or item[2] == 2:
				print("  {}) {}".format(item[0], item[1]))
		b = input()
		for item in pl.inv:
			if int(b) == item[0]:
				print("Выберите зачарование:")
				i = 0
				if items.plEnchants != []:
					for plEnch in items.plEnchants:
						if plEnch[2] > 0:
							print("{}) {} (Уровень: {})(Необходимый дар для зачарования: {} общего доверия и {} золотых)".format(plEnch[0],plEnch[1], plEnch[2], plEnch[3], plEnch[4]))
							i += 1
				if i > 0:
					b = input()
					for plEnch in items.plEnchants:
						if plEnch[0] == int(b):
							if pl.worldTrustLevel >= plEnch[3] and pl.money >= plEnch[4]:
								for skill in pl.skills:
									if skill[0] == 0:
										val = round((skill[2] + plEnch[2]) / 1.5, 2)
								if plEnch[1] == "STUN": val // 2
								if plEnch[1] == "STUN" or plEnch[1] == "BURN":
									if item[2] == 2:
										print("Предмет будет зачарован на заклиание {} с силой {}, продолжить?".format(plEnch[1], val))
										print("1) Да")
										print("2) Нет")
										b = input()
										if int(b) == 1:
											pl.worldTrustLevel -= plEnch[3]
											pl.money -= plEnch[4]
											if item[2] == 1:
												pl.inv[pl.inv.index(item)][2] = 3
											elif item[2] == 2:
												pl.inv[pl.inv.index(item)][2] = 2.1
											for ench in items.enchantesList:
												if ench[0] == plEnch[0]:
													e = ench[1]
													if e[0] == "BURN": e[3] = val
													elif e[0] == "STUN": e[2] = val
													pl.inv[pl.inv.index(item)].append(e)
													break
											break
										elif int(b) == 2:
											pass
									else:
										print("Это зачарование только для оружия")
										input
										break
				else:
					print("У вас нет зачарований.")
					input()
					pass

	def main(self, pl, items, lastChunk):
		loc = map1.getLoc(pl)
		map1.checkCoords(pl, loc)
		strr = map1.getStructure(pl, loc) 
		os.system("cls")
		os.system("clear")
		print("Текущая локация: " + str(loc[1]))
		if lastChunk != []:
			if lastChunk[1] == 1:
				print("Этот чанк пуст")
		if strr[2] != "None":
			print("Вы в " + str(strr[2]))
		print("=======Квесты========")
		for q in quests.questBook:
			quests.getQuestInfo(q)
		print("=====Информация======")
		if pl.points > 0:
			print("    Ты можешь использовать очки прокачки(для этого введи: испОчки)")
		print("Твоя фракция: " + str(quests.getFraction(pl.idFrac)[1] ))
		print("Уровень: " + str(pl.lvl))
		print("Опыт: {}/{}".format(pl.xp, pl.needXp))
		print("Здоровье: " + str(pl.hp))
		print("Защита: " + str(pl.defense))
		print("Атака: " + str(-pl.atk))
		print("Монеты: " + str(pl.money))
		print("Координаты: X - {}, Y - {}".format(pl.x, pl.y))
		print("========Мобы=========")
		enmNum = 0
		for enemy in enemies:
			if enemy[0][2][0] != -1:
				print("{}) {}".format(enmNum, enemy[0][1]), end="")
				print("(HP: {})".format(enemy[0][2][0]))
			elif enemy[0][2][0] == -1:
				enemies.pop(enemies.index(enemy))
			enmNum += 1
		print("=====================")	
		b = input()
		b = b.upper()
		if re.search('ЗАЧАРОВАТЬ', b):
			self.enchant()
		if re.search('ДИАЛОГ', b):
			for l in self.letters:
				b = b.replace(l, "")
			nearNpc = quests.nearNpc(loc)
			for npc in nearNpc:
				if npc[0] == int(b):
					quests.dialog(npc[0], quests, pl, items)
					break
				else:
					print("Этот НПС не рядом")
		if re.search('ПОКАЗАТЬ', b):
			if re.search('НПС', b):
				nearNpc = quests.nearNpc(loc)
				for npc in nearNpc:
					print("{}) {}".format(npc[0], npc[1]))
				input()
			if re.search('ИНВ', b) or re.search('ИНВЕНТАРЬ', b):
				print("======Инвентарь======")
				items.getInv(pl)
				input()
			if re.search('ФРАКЦИИ', b):
				for f in quests.fractions:
					if f[0] != -1:
						print("  {}) {}(Доверие: {})".format(f[0], f[1], pl.trustLevel[f[0]][1]))
				print("Общий уровень доверия: " + str(pl.worldTrustLevel))
				input()
			if re.search('ПРЕДМЕТЫ', b):
				map1.getDecor(pl, loc)
			if re.search('ЭФФЕКТЫ', b):
				for eff in pl.effects:
					item = items.getItem(eff[0])
					print("{} - {}".format(item[1], eff[1][0]))
				input()
		if re.search('ОТКРЫТЬ', b):
			for l in self.letters:
				b = b.replace(l, "")
			if b != "":
				items.getInvDec(int(b), pl, loc)
		if re.search('ИДТИ В', b):
			b = b.replace(" ", "")
			map1.move(pl, loc, b[5:], enemies)
		if re.search("ИДТИВ", b):
			b = b.replace(" ", "")
			map1.move(pl, loc, b[4:], enemies)
		if re.search('ВНИЗ', b):
			map1.move(pl, loc, 'down')
		if re.search('ВПРАВО', b):
			map1.move(pl, loc, 'right', enemies)
		if re.search('ВЛЕВО', b):
			map1.move(pl, loc, 'left', enemies)
		if re.search('ВВЕРХ', b):
			map1.move(pl, loc, 'up', enemies)
		if re.search('АТАКОВАТЬ', b) or re.search('АТК', b):
			for l in self.letters:
				b = b.replace(l, "")
			num = int(b)
			if num <= (len(enemies) - 1):
				fight.defltFight(pl, enemies[num], enemies, items, int(num))
		if re.search('СОХРАНИТЬ', b):
			for l in self.letters:
				b = b.replace(l, "")
			ui.save()
		if re.search('ИСПОЧКИ', b):
			for l in self.letters:
				b = b.replace(l, "")
			pl.usePoints()
		if re.search('ИСПОЛЬЗОВАТЬ', b) or re.search('ИСП', b):
			for l in self.letters:
				b = b.replace(l, "")
			if b != "":
				if not int(b) > len(pl.inv) - 1:
					idSlot = int(b)
					items.useitem(idSlot, pl)
		if re.search('ВЫБРОСИТЬ', b):
			for l in self.letters:
				b = b.replace(l, "")
			if b != "":
				print('Какое количество?')
				c = input()
				if not int(b) > len(pl.inv) - 1:
					items.delItemFromInv(pl, pl.inv[int(b)][0], int(c))				

	def shop(self, pl, items, quests, npcId):
		for trader in quests.tradersList:
			if trader[0] == npcId:
				t = trader
		os.system("cls")
		os.system("clear")
		print("Ходов до обновления ассортимента: " + str(t[1]))
		print("Монет: " + str(pl.money))
		print("=====================")
		for item in t[2]:
			if item[1] > 0:
				print("{}) {} (кол-во: {}, цена за 1 штуку: {})".format(item[0], items.getItem(item[0])[1], item[1], item[2]))
		print("=====================")
		print("(Введите номер предмета)")
		b = input()
		if b != "":
			i = 0
			for item in t[2]:
				if int(b) == item[0] and item[1] > 0:
					if pl.money >= item[2]:
						print("Введите количество для покупки")
						b = input()
						if pl.money >= item[2] * int(b):
							items.addItemToInv(pl, item[0], int(b))
							quests.tradersList[quests.tradersList.index(t)][2][i][1] -= int(b)
							pl.money -= item[2] * int(b)
							break
				i += 1

class Fight():
	def __init__(self):
		self.turn = True # True - pl, False - enemy

	def defltFight(self, pl, enemy, enemies, items, num):
		enemy[0][2][0] = round(enemy[0][2][0], 0)
		enemy[0][2][1] = round(enemy[0][2][1], 0)
		enemy[0][2][2] = round(enemy[0][2][2], 0)
		if(self.turn == True):
			i = 0
			itemL = pl.getItemEquip(1)
			for i in range(1):
				if i == 0: itemR = pl.getItemEquip(1)
				if i == 1: itemR = pl.getItemEquip(0) # itemL

				if itemR != False:
					if itemR[2] == 2:
						dmg = int(pl.atk) + randrange(0, enemy[0][2][1])
						if dmg > -1:
							dmg = 0
						print("{} hp to enemy".format(dmg))
						enemy[0][2][0] += dmg
					if itemR[2] == 2.1:
						dmg = int(pl.atk) + randrange(0, enemy[0][2][1])
						if dmg > -1:
							dmg = 0
						print("{} hp to enemy".format(dmg))
						enemy[0][2][0] += dmg
						r = randrange(0, 100)
						if itemR[5][0] == "STUN":
							if r in range(itemR[5][1][0], itemR[5][1][1]):
								e = [itemR[5][0], itemR[5][2]]
								enemy[1].append(e)
						elif itemR[5][0] == "BURN":
							if r in range(itemR[5][1][0], itemR[5][1][1]):
								e = [itemR[5][0], itemR[5][2], itemR[5][3]]
								enemy[1].append(e)
					else:
						for item in items.equipmentListInfo:
							if itemR[0] == item[0]:
								if item[3] == 0.1:
									if pl.hasItem(item[4]) == True:
										items.delItemFromInv(pl, item[4], 1)
										dmg = int(pl.atk) + randrange(0, enemy[0][2][1])
										if dmg > -1:
											dmg = 0
										print("{} hp to enemy".format(dmg))
										enemy[0][2][0] += dmg
										break
									else:
										print("You don't have ammo")
										input()
										break

			if itemR == False and itemL == False:
				dmg = int(pl.atk) + randrange(0, enemy[0][2][1])
				if dmg > -1:
					dmg = 0
				print("{} hp to enemy".format(dmg))
				enemy[0][2][0] += dmg
			self.turn = False
			for effE in enemy[1]:
				if effE[0] == "STUN":
					if effE[1] < 1:
						enemy[1].pop(enemy[1].index(effE))
						self.turn = False
					elif effE[1] > 0:
						enemy[1][enemy[1].index(effE)][1] -= 1
						self.turn = True
						print("Enemy stunned")
				if effE[0] == "BURN":
					if effE[1] < 1:
						enemy[1].pop(enemy[1].index(effE))
					elif effE[1] > 0:
						enemy[1][enemy[1].index(effE)][1] -= 1
						enemy[0][2][0] += effE[2]
						print("Enemy burned")

		if(self.turn == False):
			dmg = enemy[0][2][2] + randrange(0, int(pl.defense))
			if dmg > -1:
				dmg = 0
			print("{} hp to player".format(dmg))
			pl.hp += dmg
			self.turn = True
		if enemy[0][2][0] < 1:
			drop = items.setDrop(enemy, pl)
			event = [enemy[0][0]]
			quests.questHandler(event, 0)
			for currDrop in drop:
				try:
					print("You got: " + str(items.getItem(currDrop[0])[1]) )
				except TypeError:
					pass
				if not currDrop[0]:
					items.addItemToInv(pl, currDrop[0], currDrop[1])
				else:
					pass
			fight = False
			if enemy[0][3] != -1:
				pl.trustLevel[enemy[0][3]][1] -= 1
			del enemies[num]
		if pl.hp < 1:
			print("Твое здоровье закончилось")
			quit()

	def fightTwo(self, pl, num):
		itemR = pl.getItemEquip(1)
		itemL = pl.getItemEquip(0)
		os.system("cls")
		print("Твое HP: " + str(pl.hp))
		print("HP противника: " + str(enemy[0][2][0]))
		print("-=-=-=-=-=-=-=-")
		for eq in items.equipmentListInfo:
			if eq[0] == itemR[0]:
				equip = eq
				break
			else:
				equip = [-1, "None"]	
		if itemR != False and equip[0] != -1:
			if itemR[3] == 0.1:
				dmg1 = 1
				if pl.hasItem(itemR[4]) == True:
					dmg1 = equip[2] + enemy[0][2][1]
					if dmg1 > -1: dmg1 = 0
					print("1) Выстрелить({} урона)".format(dmg1))
			if itemR[3] == 2:
				dmg2 = equip[2] + enemy[0][2][1]
				if dmg2 > -1: dmg2 = 0
				print("2) Ударить({} урона)".format(dmg2))
		elif itemR == False:
			dmg1 = pl.atk + enemy[0][2][1]
			if dmg1 > -1: dmg1 = 0
			print("0) Пнуть({} урона()")
		b = input()
		if int(b) == 0:
			handler.changeStatsEnemy(num, 0, dmg1)
		elif int(b) == 1 and dmg1 != 1:
			handler.changeStatsEnemy(num, 0, dmg1)
			items.delItemFromInv(pl, itemR[4], 1)
		elif int(b) == 2:
			handler.changeStatsEnemy(num, 0, dmg2)
lastChunk = []

def summon(pl, map1):
	global enemies, lastChunk
	currChunk = map1.getChunk(pl)
	if currChunk != -1:
		if enemies == []:
				map1.chunks[currChunk[0]][1] = 1
		if lastChunk != currChunk:
			if currChunk[1] == 0:
				enemies = []
				for i in range(0, 3): enemies.append(Enemy(items.itemsList))
				lastChunk = currChunk

handler = Handler()
enemies = []
items = Items()
fight = Fight()
quests = NPC()
map1 = Map1()
# enemyH = Enemy()
ui = UI()
pl = Player([], items.itemsList, [0,0,0,0,0])
# for a in range(0, 3):
# 	enemies.append(Enemy(items.itemsList))
ui.menu()
# summon(pl, map1)
# for i in range(0, 3): enemies.append(Enemy(items.itemsList))

# loc = map1.getLoc(pl)
# if enemies == []:
# 	for i in range(0, 3):
# 		enemies.append(Handler.spawnEnemy(loc))

# items.addItemToInv(pl, 0, 1, 0)
# items.useitem(0, pl)
# fight.fightTwo()

# items.addItemToInv(pl, 8, 1, 0)
# items.addItemToInv(pl, 9, 1, 0)
# items.useitem(0, pl)
# items.useitem(1, pl)

# loc = map1.getLoc(pl)
# handler.spawnEnemy(loc)
# for i in range(len(handler.slots) - 1):
# 	print(handler.getRangeToEnemy(i))
# 	print(handler.slots[i].info[2])
# 	print(handler.slots[i].inv)
# fight.fightTwo(pl, 0)
# print(handler.slots[0].info[2])

while True:
	loc = map1.getLoc(pl)
	items.upLvlEnch()
	# Handler.spawnEnemy(loc)
	currChunk = map1.getChunk(pl)
	if pl.xp >= pl.needXp:
		pl.upLvl()
	if currChunk != -1:
		ui.main(pl, items, currChunk)
	else:
		ui.main(pl, items, lastChunk)