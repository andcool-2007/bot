polit = "путин", "байден", "зеленский", "спецопераци", "войн", "путя", "байдэн"
nah = " кринж ", " боже ", " бож ", " чел "
link = "https://www.youtube.com", "https://www.youtube.ru", "https://vk.com", "https://github.com", "https://aliexpress.ru", "https://www.thingiverse.com"
import logging
from datetime import datetime, date, time, timedelta
from aiogram import Bot, Dispatcher, executor, types
import os
import numpy as np
import random
from temp import printTemp
import time
import fan
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import white_list
import top

#time.sleep(10)
import asyncio
import aioschedule
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
from contextlib import suppress


start_dir = os.getcwd()
try:
	os.chdir(sys._MEIPASS)
	from socialc import SocialScore, show, SocialScore_set, SocialScore_setp
	import magic_filter
except Exception:
	from socialc import SocialScore, show, SocialScore_set, SocialScore_setp
	import magic_filter

os.chdir(start_dir)

finded = False
triggered = False
#logging.basicConfig(level=logging.INFO)
up_c = 0
bot = Bot(token="5896801600:AAH9EgH0oAaH7C2kxsOsjqqNvj0IIEpr6V0")
dp = Dispatcher(bot)
last_id = 0
flood = 0


try:
	filt = open('/home/orangepi/bot/filt_l.txt', 'r', encoding = 'utf-8')
	
except Exception:
	filt = open('filt_l.txt', 'r', encoding = 'utf-8')
filt_s = filt.read().split("/")
print("Andcool Guard Bot приветствовать вас!\nВы добавить меня в группа и сделать админ.\nЯ навести там порядок!")

async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(content_types=['any'])

async def echo(message: types.Message):
	top.add(message.from_user.id, message.chat.id)
	
	if message.chat.id == -1001647677200:
		await message.delete()
	if message.chat.type != "private":

		up_c = 0
		global last_id
		global flood
		triggered = False
		#------------------FLOOD----------------------
		if last_id == message.from_user.id:
			flood += 1
		else:
			flood = 0
		if flood >=10:
			await message.answer(message.from_user.first_name + ", прекратить спамить в этом чате!\n" + "Социальный рейтинг понижен на 50.")
			SocialScore(message.from_user.id, -50, message.chat.id)
			flood = 0
			if triggered == False:
				print(message.from_user.first_name + ', ' + message.text + " -> flood")
			triggered = True
		last_id = message.from_user.id
			#--------------------------------------------

		if message.content_type == "text":
			member = await bot.get_chat_member(message.chat.id, message.from_user.id)
			
		#----------------SCORE_SHOW------------------


			if message.reply_to_message:
				if member.is_chat_admin():

					if message.text == "/sc" or message.text == "/sc@andcool_bot":
						await message.reply("Социальный рейтинг пользователя " + message.reply_to_message.from_user.first_name + " равен " + str(show(message.reply_to_message.from_user.id, message.chat.id)))
					if message.text.find("/sc_set") != -1:
						sc_am = int(message.text[message.text.find("/sc_set") + 8:])
						SocialScore_set(message.reply_to_message.from_user.id, sc_am, message.chat.id)
					if message.text.find("/p_set") != -1:
						sc_am = int(message.text[message.text.find("/sc_set") + 7:])
						SocialScore_setp(message.reply_to_message.from_user.id, sc_am, message.chat.id)
					if message.text.find("/mute") != -1:
						mute_t = float(message.text[message.text.find("/mute") + 6:])
						dt = datetime.now() + timedelta(hours=mute_t)
						timestamp = dt.timestamp()
						flood = 0
						await message.delete()
						await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
					if message.text.find("/ban") != -1:
						await message.delete()
						await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id, revoke_messages=False)

					if message.text == "/white_list_add":
						done = white_list.add_to_whitelist(message.reply_to_message.from_user.id, message.chat.id)
						if done == False:
							await message.reply("Пользователь уже в белом списке")
					if message.text == "/white_list_remove":
						done = white_list.remove_from_whitelist(message.reply_to_message.from_user.id, message.chat.id)
						if done == False:
							await message.reply("Пользователя нет в белом списке")

			else:
				if message.from_user.id == 1197005557:
					
					if message.text == "/reboot":
						os.system("sudo reboot")
					if message.text == "/shutdown":
						os.system("sudo poweroff")
				#----------------SCORE_SHOW------------------
				if message.text == "/sc" or message.text == "/sc@andcool_bot":
					await message.delete()
					msg = await message.answer(message.from_user.first_name + ", ваш социальный рейтинг равен " + str(show(message.from_user.id, message.chat.id)))
					asyncio.create_task(delete_message(msg, 60))
				if message.text == "/top":
					topl, count = top.sort(message.chat.id)
					text = "Топ пользователей по количеству сообщений:\n"
					for x_top in range(count):
						member = await bot.get_chat_member(message.chat.id, round(topl[x_top][0]))
						text = text + f"{x_top + 1}. {member.user.first_name} - {round(topl[x_top][1])}\n"
					await message.reply(text)	
				if message.text.find("/sc_roulette") != -1:
					try:

						sc_n = show(message.from_user.id, message.chat.id)
						sc_tx = message.text[message.text.find("/sc_roulette") + 13:]
						if sc_tx.find("all") != -1:
							sc_rl = sc_n - 1
						else:
							sc_rl = int(sc_tx)
						print(type(sc_n))
						if sc_rl > 1 and sc_rl <= sc_n:
							rand_sc = random.randint(0, 5)
							if rand_sc == 2:
								await message.reply(message.from_user.first_name + " поставил " + str(sc_rl) + " социального рейтинга и выиграл!\n+" + str(sc_rl) + " социального рейтинга")
								SocialScore(message.from_user.id, sc_rl, message.chat.id)
							else:
								await message.reply(message.from_user.first_name + " поставил " + str(sc_rl) + " социального рейтинга и проиграл!\n-" + str(sc_rl) + " социального рейтинга")
								SocialScore(message.from_user.id, sc_rl * -1, message.chat.id)
						else:
							await message.reply("Введите число от 1 до " + str(show(message.from_user.id, message.chat.id)) + "\nПример: /sc_roulette " + str(random.randint(1, sc_n)))
					except Exception:
						await message.reply("Введите число от 1 до " + str(show(message.from_user.id, message.chat.id)) + "\nПример: /sc_roulette " + str(random.randint(1, sc_n)))

			#--------------------------------------------
			if white_list.is_in(message.from_user.id, message.chat.id) == False:
			#----------------CAPS_GUARD------------------
				for mess_ch in range(len(message.text)):
					if message.text[mess_ch].isupper():
						up_c += 1
				#--------------------------------------------

				mess = message.text.lower()
				#--------------------------------------------
				finded_link = False
				for i in range(len(link)):
					if mess.find(link[i]) != -1:
						finded_link = True
					if "https://" in mess and not finded_link:
						await message.answer("Партия запрещать присылать незнакомые ссылки! \nСоциальный рейтинг понижен на 50.")
						await message.delete()
						SocialScore(message.from_user.id, -50, message.chat.id)
						break

				finded_link = False
				#--------------------------------------------
				#----------------FILT------------------------
				try:
					for i in range(len(filt_s)):
						if mess.find(filt_s[i].lower()) != -1:
							answers1 = message.from_user.first_name + ", молчать!\n" + "Мат и оскорбления запрещать в этом чате!\n" + "Социальный рейтинг понижен на 100.", "Партия не поддерживать такие выражения!\nСоциальный рейтинг понижен на 100."
							await message.answer(answers1[random.randint(0, 1)])
							await message.delete()
							SocialScore(message.from_user.id, -100, message.chat.id)
							dt = datetime.now() + timedelta(minutes=15)
							timestamp = dt.timestamp()
							flood = 0
							#await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
							if triggered == False:
								print(message.from_user.first_name + ', ' + message.text + " -> swearing")
							triggered = True
							break
					#-------------------------------------------

					#---------------POLIT-----------------------
					for i in range(len(polit)):
						if mess.find(polit[i].lower()) != -1:
							await message.answer("Партия запрещать обсуждать политика в этом чате!\nСоциальный рейтинг понижен на 120.")
							await message.delete()
							SocialScore(message.from_user.id, -120, message.chat.id)
							if triggered == False:
								print(message.from_user.first_name + ', ' + message.text + " -> polit")
							triggered = True
							break
					for i in range(len(nah)):
						if mess.find(nah[i].lower()) != -1:
							await message.answer("Партия приказывать говорить правильно!\nСоциальный рейтинг понижен на 50.")
							await message.delete()
							SocialScore(message.from_user.id, -50, message.chat.id)
							if triggered == False:
								print(message.from_user.first_name + ', ' + message.text + " -> nah")
							triggered = True
							break
					#-------------------------------------------

					#-------------CAPS_GUARD--------------------
					if(up_c * 100) / len(message.text) >= 50 and len(message.text) >= 4:
						await message.reply("Партия понимать вас без капса!\n" + "Социальный рейтинг понижен на 10.")
						if triggered == False:
							print(message.from_user.first_name + ', ' + message.text + " -> CAPS")
						triggered = True
						SocialScore(message.from_user.id, -10, message.chat.id)
						flood = 0
					#-------------------------------------------
				except Exception:
					pass

			#---------------VOICE----------------
			elif message.content_type == "voice":
				#photo=open("voice.jpg", "rb")
				#await message.reply("Партия приказывать писать буквами!\nПрекратить говорить ртом!\nСоциальный рейтинг понижен на 50.")
				#await bot.send_photo(message.chat.id, photo)
				if triggered == False:
					print(message.from_user.first_name + " -> voice")
				triggered = True
				#SocialScore(message.from_user.id, -50, message.chat.id)
				flood = 0
			#-----------------------------------



		#------------------------------MUTE--------------------------------------------
		if os.path.exists("SocialScore" + str(message.chat.id) +".npy") == False:
			sc = np.zeros((3, 100))
			for sc_c_f in range(99):
				sc[1][sc_c_f] = 500

		else:
			sc = np.load("SocialScore" + str(message.chat.id) +".npy")

		for sc_c in range(99):
			#print(sc[1][sc_c])
			if sc[1][sc_c] == 0 or sc[1][sc_c] < 0:
				mutted = False
				member = await bot.get_chat_member(message.chat.id, sc[0][sc_c])
				print(member)
				if member.status == "member" or member.status == "restricted":
					sc[2][sc_c] += 1
					dt = datetime.now() + timedelta(hours=12 * sc[2][sc_c])

					timestamp = dt.timestamp()
					await message.answer(member.user.first_name + "!\nВы себя плохо вести!\n" + "Мут на " + str(round(12 * sc[2][sc_c])) + " часа!\n")
					mutted = await bot.restrict_chat_member(message.chat.id, sc[0][sc_c], types.ChatPermissions(False), until_date = timestamp)
					
				
				sc[1][sc_c] = 300
				np.save("SocialScore" + str(message.chat.id) +".npy", sc)
	else:
		
		txt = "Andcool Guard Bot приветствовать вас!\nВы добавить меня в группа и сделать админ.\nЯ навести там порядок!\n" + "Раздаю муты за:\n- Обсуждение политики\n- Нецензурные выражения\n- Сообщения капсом\n- Флуд (куча сообщений подряд)\n\n"
		txt1 = "Команды для админов (ответь на сообщение цели):\n/sc - социальный рейтинг пользователя\n/sc_set - установка социального рейтинга для пользователя\n/p_set - установка степени наказания для пользователя\n/ban - выгнать участника\n/mute 1 - замутить участника на 1 час\n"
		txt2 = "\nБелый список - привилегия, на необработку сообщений ботом\nКоманды белого списка (ответь на сообщение цели):\n/white_list_add - добавить пользователя в белый список\n/white_list_remove - удалить пользователя из белого списка"
		await bot.send_message(chat_id = message.from_user.id, text = txt + txt1 + txt2)

	#------------------------------------------------------------------------------


@dp.message_handler()
async def choose_your_dinner():
    try:
    	await bot.edit_message_text(chat_id = -1001647677200, message_id = 3, text = f"Температура {printTemp()} градусов")
    except Exception:
    	pass

    #msg1 = await bot.send_message(chat_id = -1001647677200, text = "Гов8")
    #print(msg1)


async def scheduler():
    aioschedule.every(5).seconds.do(choose_your_dinner)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(dp): 
    asyncio.create_task(scheduler())
if __name__ == "__main__":
	started = True
	while started:
		try:
			executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
			started = False
		except Exception:
			started = True
			print("An error has occurred, reboot in 10 seconds")
			time.sleep(10)
			print("rebooting...")


