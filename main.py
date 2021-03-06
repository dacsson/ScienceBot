import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

#-------------------------------------------------------------------------#

with open("config.json", "r") as read_file:
	token = json.load(read_file) #каждый бот имеет собственный токен для общение с API vk, импортируем этот токен в тутошний файл

#авторизируемся под видом бота
vk_session = vk_api.VkApi(token=token)

#необходимо для работы с сообщениями
longpoll = VkLongPoll(vk_session) 

vk = vk_session.get_api()
keyboard = VkKeyboard(one_time=True)

#все возможные сообщения, на которые бот будет отвечать
messages = ["привет", "пока", "подписка"]

#-------------------------------------------------------------------------#

def main():

	keyboard = VkKeyboard(one_time=True)
	keyboard.add_button('привет', color=VkKeyboardColor.SECONDARY)
	
	#основной алгоритм
	for event in longpoll.listen():
	    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:		
	        if event.text == messages[0]: #если написали заданную фразу
	            vk.messages.send(
	                user_id=event.user_id,
	                random_id=event.random_id,
	                message='Приветствую!'
					)
	        elif event.text == messages[1]:
	        	vk.messages.send(
	        		user_id = event.user_id,
	        		random_id = event.random_id,
	        		message = 'Досвидания!'
	        		)
	        elif event.text == messages[2]:
	        	vk.messages.send(
	        		user_id = event.user_id,
	        		random_id = event.random_id,
	        		message = 'Спасибо!\nТеперь вы подписаны на рассылку!'
	        		)
	        else:
	        	vk.messages.send(
	        		user_id = event.user_id,
	        		random_id = event.random_id,
	        		message = 'Никак не пойму, что вы написали...'
	        		)

#беседу пока не трогаю
#            elif event.from_chat: #если написали в Беседе
#               vk.messages.send(
#                   chat_id=event.chat_id,
#                   message='Ваш текст'
#		)

#-------------------------------------------------------------------------#

if __name__ == '__main__':
    main()