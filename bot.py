import database
from datetime import date
import configparser
import vk_api
config = configparser.ConfigParser()
config.read('config.ini')
token = config['VK']['TOKEN']
vk = vk_api.VkApi(token=token)
access_token = config['VK']['ACCESS_TOKEN']
vk1 = vk_api.VkApi(token=access_token)


def bot_write_foto(id, text, url):
    if url == 'none':
        vk.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})
    else:
        vk.method('messages.send', {'user_id': id, 'message': text, "attachment": url, 'random_id': 0})


    #######################################

def photos_partner(id):
        partner_users = vk1.method("photos.get", {"owner_id": id, "rev": 1, "count": 3,
                                                  "offset": 0, "extended": 1, "album_id": 'wall'})
        phot = partner_users["items"]
       #print(partner_users['count']) # количество фото

        return partner_users['count'], phot, partner_users     # кол-во фото и ссылка на фото

def bdate_user(data, nomer_marker, message, id):
    try:
       current_date = date.today()
       date_of_birth = int(current_date.year) - int(data[0]['bdate'][-4:]) #   Возраст пользователя( вычисляется не точно)
       nomer_marker = nomer_marker + 1
    except KeyError:
       nomer_marker = 0
       bot_write_foto(id, f"Ваш возраст ?", 'none')
       if message.isdigit():
             if (int(message) >= 16) and (int(message) < 100):
                  date_of_birth = int(message)
                  nomer_marker = nomer_marker + 1
       else:
          date_of_birth = 100          #костыль
    return date_of_birth, nomer_marker


def city_user(data, nomer_marker, message, id):
    try:
        city_user = data[0]['city']['id']
        nomer_marker = nomer_marker + 1
    except BaseException:
        nomer_marker = 0
        bot_write_foto(id, "Введите название города", 'none')
        city_name = message
        city_user_search = vk1.method("database.getCities", {"q": city_name, "count": 1, 'country_id': 1})
        if city_user_search['count'] != 0:
            city_user = city_user_search['items'][0]['id']
            nomer_marker = nomer_marker + 1
        else:
            bot_write_foto(id, "Город с таким названием не найден ", 'none')

    return city_user, nomer_marker
def sex_user(data, nomer_marker, message, id):
   try:
       if (data[0]['sex'] == 2):  # пол пользователя
           sex_user = 1
           nomer_marker = nomer_marker + 1
       elif (data[0]['sex']) == 1:
           sex_user = 2
           nomer_marker = nomer_marker + 1
       else:
           nomer_marker = 0
           if message.isdigit():
               bot_write_foto(id, "Вы мужчина или женщина (2/1)?", 'none')
               if (data[0]['sex'] == 2):  # пол пользователя
                   sex_user = 1
                   nomer_marker = nomer_marker + 1
               elif (data[0]['sex'] == 1):
                   sex_user = 2
                   nomer_marker = nomer_marker + 1
   except BaseException:
       nomer_marker = 0
       bot_write_foto(id, "Вы мужчина или женщина (2/1)?", 'none')
       if message.isdigit():
           if message == 2:  # пол пользователя
               sex_user = 1
               nomer_marker = nomer_marker + 1
           elif message == 1:
               sex_user = 2
               nomer_marker = nomer_marker + 1
   return sex_user, nomer_marker

def user_data1(id):
    user = vk.method("users.get", {"user_ids": id, 'fields': 'city,relation, sex,photo_50, bdate'})
    first_name_user = user[0]['first_name']  # имя пользователя
    last_name_user = user[0]['last_name']  # фамилия пользовател

    try:
       current_date = date.today()
       date_of_birth = int(current_date.year) - int(user[0]['bdate'][-4:]) #   Возраст пользователя( вычисляется не точно)
    except:
        date_of_birth = "нет данных"

    try:
        sex_user = user[0]['sex']
    except:
        sex_user = "нет данных"

    try:
        city_user = user[0]['city']['title']                              #user[0]['city']['title']  # город пользователя
    except:
        city_user = "нет данных"

    try:
        relation_user = user[0]['relation']
    except:
        relation_user = "нет данных"
    photo_50_user = user[0]['photo_50']
    return first_name_user, last_name_user, date_of_birth, sex_user, city_user, relation_user, photo_50_user




def partner_search(id,city_user,date_of_birth,sex_user,nomer):           # поиск подходящих людей

    age_from = date_of_birth-5  # возростной диапазон
    age_to = date_of_birth+5
    user_partner = []
    max_reseah_partner = 10
    bot_write_foto(id, f"Немного подождите", 'none')
    for nomer in range(0, max_reseah_partner):
        user_partner = vk1.method("users.search", {'age_from': age_from, 'age_to': age_to, 'is_closed': "false",
                                               'count': 1000, 'sex':  sex_user, 'city': city_user, 'offset': nomer })

        if user_partner['items'][0]['is_closed']:
           nomer = nomer +1
        else:
          database.insert_users_partner(int(user_partner['items'][0]['id']), int(0))
    bot_write_foto(id, "Ищем среди новых или избранных ? (1/2)", 'none')




def main_function(id,new_partners):
        zzzz = photos_partner(new_partners[0][0])

        if int(zzzz[0]) >= 3:
            number_of_photo = 3
        else:
            number_of_photo = (int(zzzz[0]) - 1)
        qqqq = (user_data1(new_partners[0][0]))
        bot_write_foto(id, f"ЗНАКОМЬТЕСЬ:  {qqqq[0] + '    ' + qqqq[1]}", 'none')
        bot_write_foto(id, f"ЛЕТ :   {qqqq[2]}", 'none')
        bot_write_foto(id, f"Город :   {qqqq[4]}", 'none')
        bot_write_foto(id, f" Семейное положение :   {qqqq[5]}", 'none')
        bot_write_foto(id, f"Адрес страницы:  https://vk.com/id{new_partners[0][0]}", 'none')
        for j in range(0, number_of_photo):
            zzzz = photos_partner(new_partners[0][0])
            owner_id = zzzz[2]['items'][j]['owner_id']
            media_id = zzzz[2]['items'][j]['id']
            media = f'photo{owner_id}_{media_id}'
            bot_write_foto(id, f"ФОТО № {j + 1}", media)





