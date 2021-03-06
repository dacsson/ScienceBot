class VkBot:

    def __init__(self, user_id):
    
        print("Создан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        
        self._COMMANDS = ["ПРИВЕТ", "ПОКА"]

    def _get_user_name_from_vk_id(self, user_id):
    	request = requests.get("https://vk.com/id"+str(user_id))
    	bs = bs4.BeautifulSoup(request.text, "html.parser")
    
    	user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
    
    	return user_name.split()[0]

    def new_message(self, message):

    	# Привет
    	if message.upper() == self._COMMANDS[0]:
        	return f"Привет-привет, {self._USERNAME}!"
    
    	# Пока
    	elif message.upper() == self._COMMANDS[1]:
        	return f"Пока-пока, {self._USERNAME}!"
    
    	else:
        	return "Не понимаю о чем вы..."