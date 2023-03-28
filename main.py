import bot
import vk_api
import configparser
from vk_api.longpoll import VkLongPoll, VkEventType
import database
config = configparser.ConfigParser()
config.read('config.ini')
token = config['VK']['TOKEN']

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
                users_data = vk.method("users.get", {"user_ids": id, 'fields': 'city,relation, sex,photo_50, bdate'})
               # qqqq = (bot.user_data(id))
                bot.bot_write_foto(id, f"Здравствуйте, {users_data[0]['first_name']}", 'none')
                bot.bot_write_foto(id, "Ищем среди новых или избранных ? (1/2)", 'none')
                date_of_birth = bot.bdate_user(users_data, nomer_marker, message, id)[0]
                nomer_marker = bot.bdate_user(users_data, nomer_marker, message, id)[1]
            if (event.to_me) and (nomer_marker == 1):
                sex_user = bot.sex_user(users_data, nomer_marker, message, id)[0]
                nomer_marker = bot.sex_user(users_data, nomer_marker, message, id)[1]
            if (event.to_me) and (nomer_marker == 2):
                city_user = bot.city_user(users_data, nomer_marker, message, id)[0]
                nomer_marker = bot.city_user(users_data, nomer_marker, message, id)[1]
            if (event.to_me) and (nomer_marker == 3):
               if int(database.select_count_0()[0][0]) < 5:
                  bot.partner_search(id, city_user, date_of_birth, sex_user, nomer)
                  nomer = nomer + 10
        #################################################################################################


               elif message == "2":            # Избранное

                    if int(database.select_count_3()[0][0]) == 0:
                        bot.bot_write_foto(id, "Список избранных пуст", 'none')
                    else:
                        new_partners = database.select_users_partner(3)
                        bot.main_function(id, new_partners)
                        bot.bot_write_foto(id, """Что делаем с данным человеком ? 
                                                   - Поместить в  черный список ? :  w 
                                                   - Поместить в  избранное ?  :  e 
                                                   - Продолжить без изменений ?  :  q """, 'none')
                        
        ###########################################################################################
               elif message == "1":             # Новое
                   new_partners = database.select_users_partner(0)
                   bot.main_function(id, new_partners)
                   bot.bot_write_foto(id, """Что делаем с данным человеком ? 
                                              - Поместить в  черный список ? :  w 
                                              - Поместить в  избранное ?  :  e 
                                              - Продолжить без изменений ?  :  q """, "none")


       #######################################################################################################

               elif message == "q":
                   bot.database.update_users_partner(new_partners[0][0], 1)
                   bot.bot_write_foto(id, "Ищем среди новых или избранных ? (1/2)", 'none')
               elif message == "e":
                   bot.database.update_users_partner(new_partners[0][0], 3)
                   bot.bot_write_foto(id, """Перемещен в "избранное "
                                             Ищем среди новых или избранных ? (1/2)""", 'none')
               elif message == "w":
                   bot.database.update_users_partner(new_partners[0][0], 2)
                   bot.bot_write_foto(id, """Перемещен в "черный список "
                                             Ищем среди новых или избранных ? (1/2)""", 'none')
            else:
                bot.bot_write_foto(id, "Не поняла вашего ответа... Нажмите 'q' для поиска пары", 'none')
