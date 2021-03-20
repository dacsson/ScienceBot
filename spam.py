from main import *
import datetime
import time
import vk_api
import json
import datetime
import random
from vk_api.longpoll import VkLongPoll, VkEventType #для отправки и получения сообщений
from vk_api.keyboard import VkKeyboard, VkKeyboardColor #нативная клавиатура
from vk_api.upload import VkUpload

def time_to_spam():
	#время для рассылки
	set_day_to_spam = "19:51 on Saturday"
	print(set_day_to_spam)
	while True:
		if (datetime.datetime.now().strftime('%H:%M on %A') == set_day_to_spam):
			print("its time!'\n")
			with open("howmany.txt", "r") as hm:
				with open("subscribers.txt", "r") as UsersList:
					k = hm.readline()
					for i in range(int(k)):
						print("n" + "    " + k)
						line = UsersList.readline()
						print(line + "\n")
						user_id = int(line[0:9])
						random_id = random.getrandbits(64)
						vk.messages.send(
							user_id = user_id,
							random_id = random_id,
							message = 'Рассылка!',
							)
					i = 0
					time.sleep(120)
if __name__ == '__main__':
	time_to_spam()
