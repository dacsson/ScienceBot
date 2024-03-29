import vk_api
import json
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType #для отправки и получения сообщений
from vk_api.keyboard import VkKeyboard, VkKeyboardColor #нативная клавиатура
from vk_api.upload import VkUpload

#----------------------------------------------------------------------------------------------------------------------------------#

#каждый бот имеет собственный токен для общение с API vk, импортируем этот токен в тутошний файл
with open("config.json", "r") as read_file:
	token = json.load(read_file) 

#авторизируемся под видом бота
vk_session = vk_api.VkApi(token=token)

#необходимо для работы с сообщениями
longpoll = VkLongPoll(vk_session) 

#чтобы легче обращаться к функциям апи
vk = vk_session.get_api()

#чтобы легче загружать
upload = VkUpload(vk)

#видимость клавиатуры
keyboard = VkKeyboard(one_time=True) 

#все возможные сообщения, на которые бот будет отвечать
messages = ["⚠ГДЕ Я?⚠", "❓ОСТАВИТЬ ОТЗЫВ❓", "✅ПОДПИСАТЬСЯ✅", "start" ,"старт", "Начать", "📚ОТОСЛАТЬ РЕШЕНИЕ📚"]

#----------------------------------------------------------------------------------------------------------------------------------#

#прикрепление(загрузка) фотки к сообщению
def upload_photo(upload, photo):
	response = upload.photo_messages(photo)[0]

	owner_id = response['owner_id'] #от кого берём фото
	photo_id = response['id']
	access_key = response['access_key'] #к сожалению у каждой фотки бота есть свой ключик доступа

	return owner_id, photo_id, access_key

#отправка фотки пользователю
def send_photo(vk, peer_id, random_id, owner_id, photo_id, access_key):
	attachment = f'photo{owner_id}_{photo_id}_{access_key}'
	vk.messages.send(
		user_id = peer_id,
		random_id = random_id,
		attachment=attachment
	)

#рисуем нативную клавиатуру
def create_keyboard():

	keyboard.add_button('⚠ГДЕ Я?⚠', color=VkKeyboardColor.SECONDARY)
	keyboard.add_button('❓ОСТАВИТЬ ОТЗЫВ❓', color=VkKeyboardColor.SECONDARY)
	keyboard.add_line()
	keyboard.add_button('✅ПОДПИСАТЬСЯ НА РАССЫЛКУ✅', color=VkKeyboardColor.NEGATIVE)
	keyboard.add_button('📚ОТОСЛАТЬ РЕШЕНИЕ📚', color=VkKeyboardColor.NEGATIVE)
	keyboard.get_keyboard()

def main():
	found = False;
	flag = 0 #флаг, который определяет дурачится ли пользователь вводя то, что бот не понимает или пишет отзыв про нас
	create_keyboard()
	
	#основной алгоритм
	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:		
			if event.text == messages[0]: #если написали заданную фразу
				vk.messages.send(
					user_id=event.user_id,
					random_id=event.random_id,
					message='Приветствую!👋\n\nНаше сообщество - это объединение студентов, которые хотят начать или успешно продолжить свою деятельность в научной сфере.📚\n\nВступая в группу, вы не только получаете информацию о новых интересных событиях, но и становитесь частью нашего комьюнити, где все рады вас видеть и всегда готовы помочь!💡',
					keyboard = keyboard.get_keyboard()
					)
				send_photo(vk, event.user_id, event.random_id, *upload_photo(upload, 'HelloWorld.jpg'))
			elif event.text == messages[1]:
				vk.messages.send(
					user_id = event.user_id,
					random_id = event.random_id,
					message = 'Напишите ваше пожелание, вопрос, жалобу!',
					keyboard = keyboard.get_keyboard()
					)
				flag = 1

			elif event.text == messages[2]:
				with open("subscribers.txt", "r") as SubList:
					for line in SubList:
						if str((str(event.user_id) + "\n")) in line:
							print(str((str(event.user_id) + "\n")))
							print("\n" + line)
							found = True
				if not found:
					vk.messages.send(
						user_id = event.user_id,
						random_id = event.random_id,
						message = 'Спасибо!\nТеперь вы подписаны на рассылку!',
						keyboard = keyboard.get_keyboard(),
						)
					with open("subscribers.txt", "a") as SubList:
						SubList.write(str(event.user_id) + "\n")
					with open("howmany.txt", "r") as hm:
						k = int(hm.readline())
						k +=1
					with open("howmany.txt", "w") as hm:
						hm.write(str(k))
					found = False
				else:
					vk.messages.send(
						user_id = event.user_id,
						random_id = event.random_id,
						message = 'Подождите, вы уже подписаны!',
						keyboard = keyboard.get_keyboard(),
						)					


			elif event.text == messages[3] or event.text == messages[4] or event.text == messages[5]:
				vk.messages.send(
					user_id = event.user_id,
					random_id = event.random_id,
					message = 'Итак, что тебе интересно?',
					keyboard = keyboard.get_keyboard()
					)
			elif event.text == messages[6]:
				flag = 2
				vk.messages.send(
					user_id = event.user_id,
					random_id = event.random_id,
					message = 'Пожалуйста, напишите ваше решение следующим сообщением.',
					keyboard = keyboard.get_keyboard()
					)				
			else:
				if flag == 0:
					#если пользователь дурачится
					vk.messages.send(
						user_id = event.user_id,
						random_id = event.random_id,
						message = 'Никак не пойму, что вы написали...' + datetime.datetime.now().strftime('%H:%M on %A'),
						keyboard = keyboard.get_keyboard()
						)
				if flag == 1:
					with open("messages.txt" ,"a") as FeedBack:
						FeedBack.write("\n" + event.text)
					flag = 0
					vk.messages.send(
						user_id = event.user_id,
						random_id = event.random_id,
						message = 'Спасибо за отзыв! Мы обязательно рассмотрим его.',
						keyboard = keyboard.get_keyboard()
						)
				if flag == 2:
					flag = 0
					user_get=vk.users.get(user_ids = event.user_id)
					user_get=user_get[0]
					first_name=user_get['first_name']
					last_name=user_get['last_name']
					full_name=first_name+" "+last_name
					full_message = full_name + " " + event.text
					vk.messages.send(
						user_id = event.user_id,
						random_id = event.random_id,
						message = 'Ваше решение принято, спасибо!',
						keyboard = keyboard.get_keyboard()
						)
					vk.messages.send(
						user_id = 612186252,
						random_id = event.random_id,
						message = full_message,
						keyboard = keyboard.get_keyboard()
						)
#					attachments1 = event.attachments.get('attach1_type', False)+event.attachments.get('attach1', False)
	#				vk.messages.send(
	#					user_id= 612186252,
	#					random_id = event.random_id,
	#					message = "",
	#					attachment = attachments1, 
	#					keyboard = keyboard.get_keyboard()
	#					)



			

#беседу пока не трогаю
#            elif event.from_chat: #если написали в Беседе
#               vk.messages.send(
#                   chat_id=event.chat_id,
#                   message='Ваш текст'
#		)

#----------------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
	main()
