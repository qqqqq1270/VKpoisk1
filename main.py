import bot
from datetime import date
import vk_api
import configparser
from vk_api.longpoll import VkLongPoll, VkEventType
import database
config = configparser.ConfigParser()
config.read('config.ini')
token =config['VK']['TOKEN']

list_of_favorites = []
vk = vk_api.VkApi(token=token)

nomer = 0
nomer_marker = 0
longpoll = VkLongPoll(vk)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        message = event.text.lower()
        nomer1 = 0
        if event.to_me:
            message = event.text.lower()
            id = event.user_id
            pfoto1 = bot.photos_partner(id)


            if (event.to_me) and (nomer_marker == 0):
                nomer_marker = 0
                qqqq = vk.method("users.get", {"user_ids": id, 'fields': 'city,relation, sex,photo_50,bdate'})
               # qqqq = (bot.user_data(id))
                bot.bot_write_foto(id, f"Здравствуйте, {qqqq[0]['first_name']}", 'none')
                bot.bot_write_foto(id, "Ищем среди новых или избранных ? (1/2)", 'none')
                try:
                    current_date = date.today()
                    date_of_birth = int(current_date.year) - int(qqqq[0]['bdate'][-4:]) #   Возраст пользователя( вычисляется не точно)
                    nomer_marker = nomer_marker + 1
                except BaseException:
                    nomer_marker = 0
                    bot.bot_write_foto(id, f"Ваш возраст ?", 'none')
                    if message.isdigit():
                         if (int(message) >= 16) and (int(message) < 100):
                              date_of_birth = int(message)
                              nomer_marker = nomer_marker + 1
            if (event.to_me) and (nomer_marker == 1):
                try:
                       if (qqqq[0]['sex'] == 2) :  # пол пользователя
                           sex_user = 1
                           nomer_marker = nomer_marker + 1
                       elif (qqqq[0]['sex']) == 1 :
                           sex_user = 2
                           nomer_marker = nomer_marker + 1
                       else:
                            nomer_marker = 0
                            if message.isdigit():
                               bot.bot_write_foto(id, "Вы мужчина или женщина (2/1)?", 'none')
                               if (qqqq[0]['sex'] == 2) :  # пол пользователя
                                  sex_user = 1
                                  nomer_marker = nomer_marker + 1
                               elif (qqqq[0]['sex'] == 1) :
                                  sex_user = 2
                                  nomer_marker = nomer_marker + 1
                except BaseException :
                   nomer_marker = 0
                   bot.bot_write_foto(id, "Вы мужчина или женщина (2/1)?", 'none')
                   if message.isdigit():
                      if message == 2 :  # пол пользователя
                         sex_user = 1
                         nomer_marker = nomer_marker + 1
                      elif message == 1 :
                         sex_user = 2
                         nomer_marker = nomer_marker + 1
            if (event.to_me) and (nomer_marker == 2):
                try:
                   city_user = qqqq[0]['city']['id']
                   nomer_marker = nomer_marker + 1
                except BaseException:
                   nomer_marker = 0
                   bot.bot_write_foto(id, "Введите название города", 'none')
                   city_name = message
                   city_user_search = bot.vk1.method("database.getCities", {"q": city_name, "count": 1, 'country_id': 1})
                   if city_user_search['count'] != 0:
                       city_user = city_user_search['items'][0]['id']
                       nomer_marker = nomer_marker + 1
                   else:
                        bot.bot_write_foto(id, "Город с таким названием не найден ", 'none')
            if (event.to_me) and (nomer_marker == 3):
               if int(database.select_count_0()[0][0]) < 5:
                  bot.partner_search(id, city_user, date_of_birth, sex_user, nomer)

        #################################################################################################


               elif message == "2":            # Избранное

                    if int(database.select_count_3()[0][0]) == 0:
                        bot.bot_write_foto(id, "Список избранных пуст", 'none')
                    else:
                        new_partners = database.select_users_partner(3)
                        bot.main_function(id,new_partners)
                        bot.bot_write_foto(id, "Что делаем с данным человеком ? ", 'none')
                        bot.bot_write_foto(id, " ....Поместить в  черный список ? :  w ", 'none')
                        bot.bot_write_foto(id, " ....Поместить в  избранное ?  :  e ", 'none')
                        bot.bot_write_foto(id, " ....Продолжить без изменений ?  :  q ", 'none')
                        
        ###########################################################################################
               elif message == "1":             # Новое
                   new_partners = database.select_users_partner(0)
                   bot.main_function(id, new_partners)
                   bot.bot_write_foto(id, "Что делаем с данным человеком ? ", 'none')
                   bot.bot_write_foto(id, " ....Поместить в  черный список ? :  w ", 'none')
                   bot.bot_write_foto(id, " ....Поместить в  избранное ?  :  e ", 'none')
                   bot.bot_write_foto(id, " ....Продолжить без изменений ?  :  q ", 'none')


       #######################################################################################################

               elif message == "q":
                   bot.database.update_users_partner(new_partners[0][0], 1)
                   bot.bot_write_foto(id, "Ищем среди новых или избранных ? (1/2)", 'none')
               elif message == "e":
                   bot.database.update_users_partner(new_partners[0][0], 3)
                   bot.bot_write_foto(id, "Перемещен в избранное ", 'none')
                   bot.bot_write_foto(id, "Ищем среди новых или избранных ? (1/2)", 'none')
               elif message == "w":
                   bot.database.update_users_partner(new_partners[0][0], 2)
                   bot.bot_write_foto(id, "Перемещен в черный список ", 'none')
                   bot.bot_write_foto(id, "Ищем среди новых или избранных ? (1/2)", 'none')
            else:
                bot.bot_write_foto(id, "Не поняла вашего ответа... Нажмите 'q' для поиска пары", 'none')
