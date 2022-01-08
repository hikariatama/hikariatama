# -*- coding: utf-8 -*-

# Приветственное сообщение
import sys
from keyboards import *
from dutils import *
from tanks import *
from io import BytesIO
import datetime
import os
import re
from random import choice
import time
import requests
import json
from vk_api.upload import VkUpload
import vk_api.keyboard
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import imgkit
start_message = "Главное меню"
# ID сообщества бота (оно же сообщество клана, куда надо будет добавлять участников клана.)
clan_group_id = <int>
# Токен бота (нужно со всеми правами)
bot_token = "<token>"
# Задержка лонгполлинга. Если хост мощный и не жалко мощностей, то можно уменьшить.
longpool_sleep = .6

params = {u'Против': 'against', u'Тип': 'type', u'Дата': 'date', u'Время': 'time',
          u'Командир': 'komandor', u'Кол-во мест': 'main_q', u'Кол-во запасных': 'add_q'}

# ID админской конфы
admins_conversation = 2000000001
# ID конфы с участниками клана
main_conversation = 2000000001


# Это - чтобы нормально работали русские символы в коде.
reload(sys)
sys.setdefaultencoding('utf-8')

# Это - чтобы читать и писать файлы по абсолютному пути (/var/www/bot/example/file.txt)
path = os.path.dirname(os.path.abspath(__file__)) + "/"
print("Starting from directory " + path + "...")

# Объявляем сессию вк с токеном и т.д.
vk_session = vk_api.VkApi(token=bot_token)
longpoll = VkBotLongPoll(vk_session, clan_group_id)
vk = vk_session.get_api()


#####  ОПЕРАЦИИ С БАЗОЙ ДАННЫХ   #####

'''
	Две базы сделаны не просто так.
	База users.db независима от чата\\бота, ее не обязательно очищать при тестах
	Во время тестов, если вдруг ты уже пофиксил баг, но бот не работает, или ты не можешь понять, что тебе от него надо, просто стираешь ПУНКТ steps из main.db

'''


# Читаем базу из файла, если он конечно, существует
try:
    with open(path + "users.db", 'r') as f:
        users_database = json.loads(f.read())
except:
    users_database = dict()


# Читаем базу из файла, если он конечно, существует
try:
    with open(path + "main.db", 'r') as f:
        main_db = json.loads(f.read())
except:
    main_db = dict()

if not 'requests' in main_db:
    main_db['requests'] = dict()

if not 'tanks' in main_db:
    main_db['tanks'] = dict()

if not 'steps' in main_db:
    main_db['steps'] = dict()

if not 'events' in main_db:
    main_db['events'] = list()

if not 'events_archive' in main_db:
    main_db['events_archive'] = list()


old_db__users = {}
old_db__main_db = {}

# Выполняется в начале поллинга: база сохраняется в файл, отдельный, для дальнейшнего сравнения


def autosave_db_step_1():
    old_db__users = users_database
    old_db__main_db = main_db
# Выполняется в конце поллинга: база сравнивается со старой, и если что-то отличается - сохраняется в файл.


def autosave_db_step_2():
    if users_database != old_db__users:
        with open(path + "users.db", 'w') as f:
            f.write(json.dumps(users_database))

    if main_db != old_db__main_db:
        with open(path + "main.db", 'w') as f:
            f.write(json.dumps(main_db))


#####  КЛАВИАТУРЫ  #####

def get_keyboard_main(user_id):
    if check_admin(user_id):
        return get_keyboard__admin()

    if vk.groups.isMember(group_id=clan_group_id, user_id=user_id):
        return get_keyboard__group_member()

    return get_keyboard__user()


def get_tanks_kb(user_id):
    kb = {
        "one_time": True,
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "label": "🏠 Домой"
                },
                "color": "primary"
            }]
        ]
    }

    btns_in_row = 3

    current_tanks_db = tanks_db

    for step_key in main_db['tanks'][str(user_id)]['path']:
        try:
            current_tanks_db = current_tanks_db[step_key]
        except:
            pass

    if current_tanks_db != tanks_db:
        kb['buttons'].insert(0, {
            "action": {
                "type": "text",
                "label": "⬅️ Назад"
            },
            "color": "primary"
        })

    if type(current_tanks_db) is list:
        answer = "➖➖🔹 " + \
            main_db['tanks'][str(user_id)]['path'][-1] + \
            " 🔹➖➖\n" + current_tanks_db[0]

        vk.messages.send(
            peer_id=user_id,
            message=" ",
            random_id=get_random_id(),
            attachment="photo272097546_457242694"
        )

        vk.messages.send(
            peer_id=user_id,
            message=answer,
            random_id=get_random_id(),
            keyboard=json.dumps(kb, ensure_ascii=False)
        )

        return True

    for i in range(0, len(current_tanks_db), btns_in_row):
        row = []
        for j in range(0, btns_in_row):
            if len(current_tanks_db) > i + j:
                row.append({
                    "action": {
                        "type": "text",
                        "label": current_tanks_db.keys()[i + j]
                    },
                    "color": "secondary"
                })

        kb['buttons'].append(row)

    return json.dumps(kb, ensure_ascii=False)


# Проверка пользователя на наличие админских прав: делаем запрос к vk_api -> получаем участников беседы "Техника" -> удаляем дохренища ненужного говна из возвращенного словаря -> преобразуем в лист с одними id'шниками -> проверяем наличие в данном листе нашего пользователя -> Возвращаем True\False
def check_admin(usid):
    return usid in list(map(lambda x: x['member_id'], vk.messages.getConversationMembers(peer_id=2000000001)['items']))


def choose_players(event, evid):
    users_list = ""
    i = 1
    for user, data in users_database.items():
        user_inf = vk.users.get(
            user_ids=user, fields='first_name_nom', name_case='nom')[0]
        if not 'name' in data:
            data['name'] = user_inf['first_name'] + ' ' + user_inf['last_name']

        if not 'nickname' in data:
            data['nickname'] = 'unknown'

        users_list += str(i) + " 🔰 "
        if str(user) in list(map(lambda x: str(x[0]), main_db['events'][evid]['registered'])):
            users_list += "🎟 "

        users_list += data['nickname'] + " " + data['name'] + "\n"

        i += 1

    vk.messages.send(
        peer_id=event.obj.peer_id,
        message="Выберите тех, кто участвовал: \n\n" + users_list +
        "\n\nНапишите номера игроков через пробел, без запятых, например:\n1 3 4",
        random_id=get_random_id(),
        keyboard=get_keyboard_main(event.obj.peer_id)
    )


#####  ОПЕРАЦИИ С WOTINFO  #####

def cleanhtml(raw_html):
    return re.sub(re.compile('<.*?>'), '', raw_html)


def get_clan_stats():
    r2 = requests.get(
        "http://wotinfo.net/ru/clanoverview?id=16251&server=XBOX").text
    # print(r2)
    info = []

    while not r2.find("<var>") == -1:
        cutted = cleanhtml(
            r2[r2.find("<var>") + 5:r2.find("</var>", r2.find("<var>"))])
        r2 = r2[r2.find("<var>") + 5:]
        cutted = re.sub(re.compile('[^0-9,]*'), '', cutted)
        if cutted == "" or cutted == "7" or cutted == "8":
            continue
        info.append(cutted)

    if len(info) < 3:
        return 'Нет связи с WoTinfo. Попробуйте еще раз позднее'

    answer = "Статистика клана N_ERA \"XBOX\":\n➖➖ Эффективность ➖➖\n		 🔸		" + \
        info[0] + "		🔸\n➖➖➖➖ WN7 ➖➖➖➖\n		🔸		" + info[1] + \
        "		🔸\n➖➖➖➖ WN8 ➖➖➖➖\n		🔸		" + info[2] + "		🔸\n➖➖➖➖➖➖➖➖➖➖"
    return answer

# Получение данных с WoTinfo, а именно проверка существования пользователя и получение информации


def check_if_player_exists(plr, server="XBOX"):
    r = requests.get("http://wotinfo.net/ru/efficiency",
                     params={'server': server, 'playername': plr}).text
    if " не найдено" in r:
        return False

    return True


def get_player_info(plr, server="XBOX"):

    r = requests.get("http://wotinfo.net/ru/efficiency",
                     params={'server': server, 'playername': plr}).text
    playerid = r[r.find("?playerid=") +
                 10:r.find("&server=", r.find("?playerid=") + 10)]
    r2 = r
    if " не найдено" in r:
        return False
    stats = dict()
    info = []
    while not r.find("<strong>") == -1:
        cutted = cleanhtml(
            r[r.find("<strong>") + 8:r.find("</strong>", r.find("<strong>"))])
        r = r[r.find("<strong>") + 8:]
        if cutted == "":
            continue
        info.append(cutted)

    while not r2.find("<var>") == -1:
        cutted = cleanhtml(
            r2[r2.find("<var>") + 5:r2.find("</var>", r2.find("<var>"))])
        r2 = r2[r2.find("<var>") + 5:]
        cutted = re.sub(re.compile('[^0-9,]*'), '', cutted)
        if cutted == "" or cutted == "7" or cutted == "8":
            continue
        info.append(cutted)

    keys = ['nickname', 'registered', 'last_seen', 'trees_fallen', 'avg_tanks_level', 'fights', 'wins_coof', 'accurance_coof', 'alived_coof', 'avg_damage_to_at', 'avg_damage_per_fight',
            'destroyed_per_fight', 'explored_per_fight', 'defensed_per_fight', 'captured_per_fight', 'frags_dead_coof', 'clan', 'join_clan_date', 'clan_post', 'efficiency', 'WN7', 'WN8']
    for i in range(len(info)):
        stats[keys[i]] = info[i]

    # Недавняя стата
    print(playerid)
    r3 = requests.get("http://wotinfo.net/ru/recent?playerid=" +
                      playerid + "&server=XBOX").text
    ef = []

    while not r3.find("<strong>") == -1:
        cutted = cleanhtml(
            r3[r3.find("<strong>") + 8:r3.find("<span", r3.find("<strong>"))])
        r3 = r3[r3.find("<strong>") + 8:]
        cutted = re.sub(re.compile('[^0-9,]*'), '', cutted)
        if cutted == "" or cutted == "7" or cutted == "8":
            continue
        ef.append(cutted)

    stats['w_efficiency'] = ef[0]
    stats['m_efficiency'] = ef[1]

    stats['w_wn7'] = ef[3]
    stats['m_wn7'] = ef[4]

    stats['w_wn8'] = ef[6]
    stats['m_wn8'] = ef[7]

    return stats


# Основной цикл. Когда возникает событие, оно приходит в виде переменной event
for event in longpoll.listen():
    autosave_db_step_1()
    # Если пришедшее событие - сообщение
    if event.type == VkBotEventType.MESSAGE_NEW:
        # Написали в лс боту? или нет?
        if event.obj.peer_id == event.obj.from_id:
            # Сразу получаем инфу о пользователе методом апишки
            userinfo = vk.users.get(
                user_ids=event.obj.peer_id, fields='first_name_nom', name_case='nom')[0]
            # Если пользователя еще не дай боже нет в базе, добавляем его
            if not str(event.obj.peer_id) in users_database:
                users_database[str(event.obj.peer_id)] = dict()

            if not str(event.obj.peer_id) in main_db['steps']:
                main_db['steps'][str(event.obj.peer_id)] = dict()
            # А дальше обычным ифом проверяем, что пользователь хочет от бота.
            if event.obj.text == "Начать" or event.obj.text == "🏠 Домой":
                logging(userinfo, "Начал диалог с ботом")
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message=start_message,
                    random_id=get_random_id(),
                    keyboard=get_keyboard_main(event.obj.from_id)
                )

                main_db['steps'][str(event.obj.from_id)]['last_action'] = ""
                main_db['steps'][str(event.obj.from_id)]['tanks'] = ""
            elif event.obj.text == "Подать заявку":
                logging(userinfo, "Начал подачу заявки")
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Укажите ваш игровой никнейм.\nПросьба указать правильный никнейм для получения информации о вашем аккаунте!',
                    random_id=get_random_id()
                )

                if not str(event.obj.peer_id) in main_db['steps']:
                    main_db['steps'][str(event.obj.peer_id)] = dict()

                main_db['steps'][str(event.obj.peer_id)
                                 ]['last_action'] = "leave_request"
            elif event.obj.text == "Моя статистика":
                try:
                    player_info = get_player_info(
                        users_database[str(event.obj.peer_id)]['nickname'])
                    player_info__str = "В игре с " + player_info['registered'] + "\nСыграно боев: " + player_info['fights'] + "\nПроцент побед: " + player_info['wins_coof'] + "\nМеткость: " + player_info['accurance_coof'] + "\nВыжил: " + player_info['alived_coof'] + "\nСредний урон: " + player_info['avg_damage_per_fight'] + "\nЭффективность: " + player_info['efficiency'] + \
                        "\nWN7: " + player_info['WN7'] + "\nWN8: " + player_info['WN8'] + "\n➖➖➖➖ Неделя ➖➖➖➖\nЭффективность: " + player_info['w_efficiency'] + "\nWN7: " + player_info['w_wn7'] + \
                        "\nWN8: " + player_info['w_wn8'] + "\n➖➖➖➖ Месяц ➖➖➖➖\nЭффективность: " + \
                        player_info['m_efficiency'] + "\nWN7:" + \
                        player_info['m_wn7'] + "\nWN8: " + player_info['m_wn8']
                    logging(userinfo, "Запросил свою стату")
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message=player_info__str,
                        random_id=get_random_id(),
                        keyboard=get_keyboard_main(event.obj.peer_id)
                    )
                except KeyError:
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Извините, вашего ника (почему-то) нет в базе данных. Вам нужно подать заявку на вступление в клан, чтобы указать необходимую информацию, для этого напишите "Подать заявку"',
                        random_id=get_random_id(),
                        keyboard=get_keyboard_main(event.obj.peer_id)
                    )
            elif event.obj.text == "Статистика клана":
                logging(userinfo, "Запросил стату клана")
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message=get_clan_stats(),
                    random_id=get_random_id(),
                    keyboard=get_keyboard_main(event.obj.peer_id)
                )
            elif event.obj.text == "Требования":
                logging(userinfo, "Запросил требования для вступления")
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message="‼️ Требования к кандидатам ‼️\n • Возраст — 18+\n • Умение слушать командира и правильно воспринимать критику.\n • От 5000 боёв и от 1300 WN8.\n • Положительная статистика за последнии 1000 боев.\n • Желание принимать участие в клановых мероприятиях.\n • Участвовать в развитии клана.\n • От 3 топов в ангаре.\n • Наличие связи.\n • Прайм-тайм с 21:00 по 00:00мск.\n • Уважительное отношение друг к другу❗️",
                    random_id=get_random_id(),
                    keyboard=get_keyboard_main(event.obj.peer_id)
                )
            elif event.obj.text == "О клане":
                logging(userinfo, "Запросил информации о клане")
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message="Клан «New Era» был основан 13.02.2020г. для любителей игры \"World of Tanks\" на XBOX One. Первый состав пополнили игроки из немалоизвестных кланов, что положительно повлияло на скорое развитие, и уже с первых дней бойцы активно принимают участие в межклановых сражениях.\nО больших победах еще говорить рано, но мы постоянно тренируем состав, разрабатывать сыгранность и соперничаем с более опытными кланами. Всегда максимально быстро вводим в курс дела новичков и ознакомляем их с миром танков. Мы показываем игру с другой стороны, где в первую очередь важна отлаженная командная работа, стратегия, а главное развитие и стремление стать лучшими!\nНа данный момент для нас самым важным является развитие и победы в межклановых боях! Но в будущем, возможно, клан будет расти и развиваться в других играх на консолях!",
                    random_id=get_random_id(),
                    keyboard=get_keyboard_main(event.obj.peer_id)
                )
            elif event.obj.text == "Правила":
                logging(userinfo, "Запросил правила")
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message="Заглушка Правила",
                    random_id=get_random_id(),
                    keyboard=get_keyboard_main(event.obj.peer_id)
                )
            elif event.obj.text == "Оборудование":
                logging(userinfo, "Запросил оборудование")
                main_db['steps'][str(event.obj.peer_id)
                                 ]['last_action'] = "tanks"
                main_db['tanks'][str(event.obj.peer_id)] = dict()
                main_db['tanks'][str(event.obj.peer_id)]['path'] = []

                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message="Выберите категорию:",
                    random_id=get_random_id(),
                    keyboard=get_tanks_kb(event.obj.peer_id)
                )
            elif event.obj.text == "⬅️ Назад":
                del main_db['tanks'][str(event.obj.peer_id)]['path'][-1]
                kb = get_tanks_kb(event.obj.peer_id)
                if not type(kb) is bool:
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message="Выберите " +
                        ("под-" * len(main_db['tanks']
                                      [str(event.obj.peer_id)]['path'])) + "категорию:",
                        random_id=get_random_id(),
                        keyboard=kb
                    )
            elif event.obj.text == "События":
                logging(userinfo, "Запросил события")
                kb = {
                    "one_time": True,
                    "buttons": [
                        [{
                            "action": {
                                "type": "text",
                                "label": "🏠 Домой"
                            },
                            "color": "primary"
                        }]
                    ]
                }

                if len(main_db['events']) == 0:
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Нет предстоящих событий',
                        random_id=get_random_id(),
                        keyboard=get_keyboard_main(event.obj.peer_id)
                    )
                    continue

                events_in_row = 1
                for i in range(0, len(main_db['events']), events_in_row):
                    row = []
                    for j in range(0, events_in_row):
                        if len(main_db['events']) > i + j:
                            if 'Сражения' in main_db['events'][i + j]['type']:
                                add_info = main_db['events'][i + j]['type'][0] + \
                                    " vs. " + \
                                    main_db['events'][i + j]['against']
                            else:
                                add_info = main_db['events'][i + j]['type']
                            row.append({
                                "action": {
                                    "type": "text",
                                    "label": str(i + j + 1) + ". " + add_info + " " + main_db['events'][i + j]['date'] + " " + main_db['events'][i + j]['time'] + " 👀"
                                }, "color": "secondary"})
                    kb['buttons'].append(row)

                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Выберите событие для подробной информации.',
                    random_id=get_random_id(),
                    keyboard=json.dumps(kb)
                )
            elif event.obj.text == "Создать событие":
                logging(userinfo, "Начал создавать событие")
                main_db['steps'][str(event.obj.peer_id)
                                 ]['last_action'] = 'creating_eventtype'
                kb = {
                    "one_time": True,
                    "buttons": [
                        [{
                            "action": {
                                "type": "text",
                                "label": "⚒ Сражения"
                            },
                            "color": "negative"
                        }, {
                            "action": {
                                "type": "text",
                                "label": "👨‍🏫 Тренировка"
                            },
                            "color": "secondary"
                        }],
                        [{
                            "action": {
                                "type": "text",
                                "label": "🗺 Разбор карты"
                            },
                            "color": "positive"
                        }]
                    ]
                }
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Выберите тип события',
                    random_id=get_random_id(),
                    keyboard=json.dumps(kb)
                )
            elif '👀' in event.obj.text:
                event_id = int(event.obj.text[:event.obj.text.find('.')]) - 1
                reged = "\n🎫 Зарегистрированы: "
                if len(main_db['events'][event_id]['registered']) == 0:
                    reged = "\n🎫 На данное событие еще никто не зарегистрирован"
                registered = False
                for user, member_type in main_db['events'][event_id]['registered']:
                    if user == event.obj.peer_id:
                        registered = True
                    useri = vk.users.get(
                        user_ids=user, fields='first_name_nom', name_case='nom')[0]

                    try:
                        namei = users_database[str(user)]['name']
                    except:
                        namei = useri['first_name'] + " " + useri['last_name']

                    try:
                        nicknamei = users_database[str(user)]['nickname']
                    except:
                        nicknamei = 'NONE'

                    member_typei = 'Основной' if member_type == 'main' else 'Запасной'

                    reged += "\n▪️▪️ ↪️ " + namei + \
                        " (" + nicknamei + "): " + member_typei
                answer = "➖▫️ Событие ▫️➖\n" + main_db['events'][event_id]['type'] + "\n📆 " + main_db['events'][event_id]['date'] + "\n⌚️ " + main_db['events'][event_id]['time'] + "-UTC+3\n🐺 Командир: " + main_db['events'][event_id]['komandor'] + \
                    "\n🎯 Против: " + main_db['events'][event_id]['against'] + "\n👨‍👩‍👧‍👦 Кол-во мест: " + str(
                        main_db['events'][event_id]['main_q']) + " (+" + str(main_db['events'][event_id]['add_q']) + ")" + reged

                if not registered:

                    kb = {
                        "one_time": True,
                        "buttons": [
                            [{
                                "action": {
                                    "type": "text",
                                    "label": "🏠 Домой"
                                },
                                "color": "secondary"
                            }],
                            [{
                                "action": {
                                    "type": "text",
                                    "label": "Участвую!"
                                },
                                "color": "positive"
                            }, {
                                "action": {
                                    "type": "text",
                                    "label": "Не прийду!"
                                },
                                "color": "negative"
                            }],
                            [{
                                "action": {
                                    "type": "text",
                                    "label": "Возможно учавствую."
                                },
                                "color": "primary"
                            }]
                        ]
                    }
                else:
                    kb = {
                        "one_time": True,
                        "buttons": [
                            [{
                                "action": {
                                    "type": "text",
                                    "label": "🏠 Домой"
                                },
                                "color": "secondary"
                            }]
                        ]
                    }

                    answer += "\n\n➖▫️ Вы зарегистрированы ☑️ ▫️➖"

                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message=answer,
                    keyboard=json.dumps(kb),
                    random_id=get_random_id()
                )

                main_db['steps'][str(event.obj.peer_id)
                                 ]['last_action'] = "regevent" + str(event_id)
            elif event.obj.text == "Статистика событий":
                logging(userinfo, "Запросил стату событий")
                final = ""

                search_db = main_db['events'] + main_db['events_archive']

                stats_data = ""

                for user, data in users_database.items():
                    user_inf = vk.users.get(
                        user_ids=user, fields='first_name_nom', name_case='nom')[0]
                    if not 'name' in data:
                        data['name'] = user_inf['first_name'] + \
                            ' ' + user_inf['last_name']

                    if not 'nickname' in data:
                        data['nickname'] = 'unknown'

                    row = "<tr><td class='small'>" + \
                        data['name'].split()[0] + "</td><td class='small'>" + \
                        data['nickname'] + "</td><td>"

                    ### GETTING STATS ###

                    total = 0
                    week = 0
                    month = 0
                    fights = 0
                    trainings = 0
                    maps = 0

                    for eventi in search_db:
                        if str(user) in list(map(lambda x: str(x[0]), eventi['registered'])):
                            if 'Сражения' in eventi['type']:
                                fights += 1

                            if 'Тренировка' in eventi['type']:
                                trainings += 1

                            if 'Разбор' in eventi['type']:
                                maps += 1

                            if time.time() - 604800 <= int(datetime.datetime.strptime(eventi['date'], '%d.%m.%Y').strftime("%s")):
                                week += 1
                            if time.time() - 2678400 <= int(datetime.datetime.strptime(eventi['date'], '%d.%m.%Y').strftime("%s")):
                                month += 1

                            total += 1

                    row += str(fights) + "</td><td>" + str(trainings) + "</td><td>" + str(maps) + "</td><td>" + \
                        str(week) + "</td><td>" + str(month) + \
                        "</td><td>" + str(total) + "</td></tr>"
                    stats_data += row

                imgkit.from_url("http://blinamalina.ru/bot/vk/test/stats.php?stats=" +
                                stats_data, 'out.jpg', options={"encoding": "utf-8", "xvfb": ""})
                answer = vk_api.VkUpload(vk_session).photo_messages(
                    photos='out.jpg', peer_id=event.obj.peer_id)[0]
                access_key = answer['access_key']
                for size in answer['sizes']:
                    if size['type'] == "z":
                        photo = size['url']
                        break

                attachment = 'photo{0}_{1}_{2}'.format(
                    answer['owner_id'], answer['id'], access_key)
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Воувоувоу',
                    random_id=get_random_id(),
                    keyboard=get_keyboard_main(event.obj.peer_id),
                    attachment=attachment
                )

            elif event.obj.text == "Управление событиями":
                logging(userinfo, "Запросил управление событиями")
                kb = {
                    "one_time": True,
                    "buttons": [
                        [{
                            "action": {
                                "type": "text",
                                "label": "🏠 Домой"
                            },
                            "color": "primary"
                        }]
                    ]
                }

                if len(main_db['events']) == 0:
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Нет предстоящих событий',
                        random_id=get_random_id(),
                        keyboard=get_keyboard_main(event.obj.peer_id)
                    )
                    continue

                events_in_row = 1
                for i in range(0, len(main_db['events']), events_in_row):
                    row = []
                    for j in range(0, events_in_row):
                        if len(main_db['events']) > i + j:
                            if 'Сражения' in main_db['events'][i + j]['type']:
                                add_info = main_db['events'][i + j]['type'][0] + \
                                    " " + main_db['events'][i + j]['against']
                            else:
                                add_info = main_db['events'][i + j]['type']

                            label = str(i + j + 1) + ". " + add_info + " " + \
                                main_db['events'][i + j]['date'] + " " + \
                                main_db['events'][i + j]['time'] + " ✏️"

                            if add_info > 25:
                                label = str(i + j + 1) + ". " + add_info[:23] + ".. " + main_db['events'][i +
                                                                                                          j]['date'][:-5] + " " + main_db['events'][i + j]['time'] + " ✏️"

                            print(label, len(label))

                            row.append({
                                "action": {
                                    "type": "text",
                                    "label": label
                                }, "color": "secondary"})
                    kb['buttons'].append(row)

                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Выберите событие',
                    random_id=get_random_id(),
                    keyboard=json.dumps(kb)
                )

            elif event.obj.text == '✏️':

                event_id = int(main_db['steps'][str(
                    event.obj.peer_id)]['last_action'][9:])
                kb = {
                    "one_time": True,
                    "buttons": [
                        [{
                            "action": {
                                "type": "text",
                                "label": "🏠 Домой"
                            },
                            "color": "secondary"
                        }]
                    ]
                }
                settings_in_row = 3
                for i in range(0, len(params.keys()) - 1, settings_in_row):
                    row = []
                    for j in range(settings_in_row):
                        if i + j < len(params.keys()) - 1:
                            row.append({
                                "action": {
                                    "type": "text",
                                    "label": params.keys()[i + j]
                                },
                                "color": "primary"
                            })
                    kb['buttons'].append(row)

                print(kb)

                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Выберите параметр для редактирования',
                    keyboard=json.dumps(kb),
                    random_id=get_random_id()
                )
            elif event.obj.text == "Состав клана":
                msg = "➖➖🔹 Состав клана 🔹➖➖\n"
                i = 1
                for user, data in users_database.items():
                    user_inf = vk.users.get(
                        user_ids=user, fields='first_name_nom', name_case='nom')[0]
                    if not 'name' in data:
                        data['name'] = user_inf['first_name']

                    if not 'nickname' in data:
                        data['nickname'] = 'unknown'

                    msg += str(i) + " 🔰 "
                    msg += data['nickname'] + \
                        " (" + data['name'].split()[0] + ")\n"

                    i += 1

                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message=msg,
                    keyboard=get_keyboard_main(event.obj.peer_id),
                    random_id=get_random_id()
                )
            elif event.obj.text == '🚫':
                logging(userinfo, "Удалил событие")
                event_id = int(main_db['steps'][str(
                    event.obj.peer_id)]['last_action'][9:])
                del main_db['events'][event_id]

                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Успешно удалено!',
                    keyboard=get_keyboard_main(event.obj.peer_id),
                    random_id=get_random_id()
                )
            elif event.obj.text == '❎':
                logging(userinfo, "Завершил событие")
                event_id = int(main_db['steps'][str(
                    event.obj.peer_id)]['last_action'][9:])
                ev_type = main_db['events'][event_id]['type']
                if 'Сражения' in ev_type:
                    main_db['steps'][str(event.obj.peer_id)]['last_action'] = 'confirmevent_outcome_' + \
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'][9:]

                    kb = {
                        "one_time": True,
                        "buttons": [
                            [{
                                "action": {
                                    "type": "text",
                                    "label": "✅ Победа"
                                },
                                "color": "positive"
                            }, {
                                "action": {
                                    "type": "text",
                                    "label": "❌ Поражение"
                                },
                                "color": "negative"
                            }], [{
                                "action": {
                                    "type": "text",
                                    "label": "⚔️ Ничья"
                                },
                                "color": "secondary"
                            }]
                        ]
                    }
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Исход события',
                        keyboard=json.dumps(kb),
                        random_id=get_random_id()
                    )
                elif 'Тренировка' in ev_type:
                    main_db['steps'][str(event.obj.peer_id)]['last_action'] = 'confirmevent_outcome_' + \
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'][9:]

                    kb = {
                        "one_time": True,
                        "buttons": [
                            [{
                                "action": {
                                    "type": "text",
                                    "label": "😁 Отлично"
                                },
                                "color": "positive"
                            }, {
                                "action": {
                                    "type": "text",
                                            "label": "✅ Хорошо"
                                },
                                "color": "positive"
                            }], [{
                                "action": {
                                    "type": "text",
                                    "label": "✌ Нормально"
                                },
                                "color": "secondary"
                            }], [{
                                "action": {
                                    "type": "text",
                                    "label": "☹️ Плохо"
                                },
                                "color": "negative"
                            }, {
                                "action": {
                                    "type": "text",
                                    "label": "😣 Ужасно"
                                },
                                "color": "negative"
                            }]
                        ]
                    }
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Оценка тренировки',
                        keyboard=json.dumps(kb),
                        random_id=get_random_id()
                    )
                else:
                    main_db['events'][event_id]['outcome'] = '☑️ Завершено'
                    choose_players(event, event_id)
                    main_db['steps'][str(event.obj.peer_id)]['last_action'] = 'confirmevent_final_' + \
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'][9:]

            elif '✏️' in event.obj.text:
                event_id = int(event.obj.text[:event.obj.text.find('.')]) - 1
                main_db['steps'][str(event.obj.peer_id)
                                 ]['last_action'] = 'editevent' + str(event_id)
                kb = {
                    "one_time": True,
                    "buttons": [
                        [{
                            "action": {
                                "type": "text",
                                "label": "🏠 Домой"
                            },
                            "color": "secondary"
                        }],
                        [{
                            "action": {
                                "type": "text",
                                "label": "✏️"
                            },
                            "color": "primary"
                        }, {
                            "action": {
                                "type": "text",
                                "label": "🚫"
                            },
                            "color": "negative"
                        },
                            {
                                "action": {
                                    "type": "text",
                                    "label": "❎"
                                },
                                "color": "positive"
                        }]
                    ]
                }

                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Выберите действие:\n✏️ Редактировать\n🚫 Удалить\n❎ Завершить',
                    keyboard=json.dumps(kb),
                    random_id=get_random_id()
                )
            else:
                try:
                    ev = main_db['steps'][str(
                        event.obj.peer_id)]['last_action']
                    if ev == "":
                        raise KeyError
                except KeyError:
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Я не знаю такой команды',
                        keyboard=get_keyboard_main(event.obj.peer_id),
                        random_id=get_random_id()
                    )
                    continue

                if ev == "leave_request":
                    to_edit = vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Проверка ника... Устанавливаю связь с серверами WoT...',
                        random_id=get_random_id()
                    )
                    if not check_if_player_exists(event.obj.text):
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Извините, данный ник неактивен! Пожалуйста, убедитесь в правильности ввода, а также в том, что игрок зарегистрирован на сервере "XBOX"',
                            keyboard=get_keyboard_main(event.obj.peer_id),
                            random_id=get_random_id()
                        )
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = ""
                    else:
                        users_database[str(event.obj.peer_id)
                                       ]['nickname'] = event.obj.text
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message_id=to_edit,
                            message='Ник сохранен.'
                        )

                        kb = {
                            "one_time": True,
                            "buttons": [
                                [{
                                    "action": {
                                        "type": "text",
                                        "label": userinfo['first_name'] + " " + userinfo['last_name']
                                    },
                                    "color": "primary"
                                }]
                            ]
                        }

                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message="Как вас зовут?",
                            random_id=get_random_id(),
                            keyboard=json.dumps(kb)
                        )
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = 'set_name'
                elif 'confirmevent_' in ev:
                    if ev.split('_')[1] == "outcome":
                        main_db['events'][int(
                            ev.split('_')[2])]['outcome'] = event.obj.text
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = "confirmevent_final_" + ev.split('_')[2]
                        choose_players(event, int(ev.split('_')[2]))
                    elif ev.split('_')[1] == "final":
                        main_db['events'][int(
                            ev.split('_')[2])]['registered'] = []
                        players = ""
                        for user in event.obj.text.split():
                            main_db['events'][int(ev.split('_')[2])]['registered'].append(
                                [users_database.keys()[int(user)-1], 'main'])
                            data = users_database[users_database.keys()[
                                int(user)-1]]
                            user_inf = vk.users.get(user_ids=users_database.keys()[int(
                                user)-1], fields='first_name_nom', name_case='nom')[0]
                            if not 'name' in data:
                                data['name'] = user_inf['first_name'] + \
                                    ' ' + user_inf['last_name']

                            if not 'nickname' in data:
                                data['nickname'] = 'unknown'

                            players += " 🔸 " + \
                                data['nickname'] + " (" + data['name'] + ")\n"

                        eventinfo = main_db['events'][int(ev.split('_')[2])]

                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Событие завершено!',
                            keyboard=get_keyboard_main(event.obj.peer_id),
                            random_id=get_random_id()
                        )

                        if 'Сражения' in eventinfo['type']:
                            vk.messages.send(
                                peer_id=main_conversation,
                                message='⚔️ Сражение завершено ⚔️\n⚔️ [N_ERA] vs. [' + eventinfo['against'] + '] ⚔️\n🧧 Исход боя: ' +
                                eventinfo['outcome'] + "\n🐺 Командир: " + eventinfo['komandor'] +
                                "\n👨‍👩‍👧‍👦 Участники события:\n\n" + players,
                                random_id=get_random_id()
                            )
                        elif 'Тренировка' in eventinfo['type']:
                            vk.messages.send(
                                peer_id=main_conversation,
                                message='⚔️ Тренировка завершена ⚔️\n⚔️ [N_ERA] vs. [' + eventinfo['against'] + '] ⚔️\n🧧 Исход боя: ' +
                                eventinfo['outcome'] + "\n🐺 Командир: " + eventinfo['komandor'] +
                                "\n👨‍👩‍👧‍👦 Участники события:\n\n" + players,
                                random_id=get_random_id()
                            )

                        main_db['events_archive'].append(
                            main_db['events'][int(ev.split('_')[2])])
                        del main_db['events'][int(ev.split('_')[2])]

                elif ev == "set_name":
                    users_database[str(event.obj.peer_id)
                                   ]['name'] = event.obj.text
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message="Вам необходимо подать заявку на вступление в группу. Если вы не сделаете этого, заявка будет отклонена! Нажмите на кнопку.",
                        random_id=get_random_id(),
                        keyboard=get_keyboard__request()
                    )
                    main_db['steps'][str(event.obj.peer_id)
                                     ]['last_action'] = 'group_request'
                elif ev == "group_request":
                    main_db['steps'][str(event.obj.peer_id)
                                     ]['last_action'] = ''
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message="Ваша заявка отправлена. Ожидайте рассмотрения 😉",
                        random_id=get_random_id(),
                        keyboard=get_keyboard_main(event.obj.peer_id)
                    )

                    emojies = [u'😀', u'😃', u'😄', u'😁', u'😆', u'😅', u'☺️', u'😊', u'😇', u'🙂', u'🙃', u'😉', u'😌', u'😍', u'😗', u'😙', u'😚', u'😋', u'😛', u'😝', u'😜', u'🤪', u'🤨', u'🧐', u'🤓', u'😎', u'🤩', u'🥳', u'😏', u'🤗', u'🥶', u'🥴', u'🤐', u'😷', u'🤠', u'🤑', u'🤤', u'🤡', u'😈', u'👻', u'🤖', u'👾', u'😺',
                               u'😸', u'😹', u'😻', u'😼', u'😽', u'🐶', u'🐱', u'🐭', u'🦊', u'🐻', u'🐼', u'🐨', u'🐯', u'🦁', u'🐮', u'🐷', u'🐽', u'🐸', u'🐵', u'🙈', u'🙉', u'🙊', u'🐒', u'🐧', u'🐦', u'', u'🐤', u'🐣', u'🐥', u'🦆', u'🦅', u'🦉', u'🐺', u'🐗', u'🐴', u'🦄', u'🐝', u'🐛', u'🦋', u'🐌', u'🐞', u'🐜', u'🦟', u'🦗']
                    choosed_emoji = choice(emojies)

                    while choosed_emoji in main_db['requests']:
                        choosed_emoji = choice(emojies)

                    main_db['requests'][choosed_emoji] = event.obj.peer_id
                    player_info = get_player_info(
                        users_database[str(event.obj.peer_id)]['nickname'])
                    player_info__str = "В игре с " + player_info['registered'] + "\nСыграно боев: " + player_info['fights'] + "\nПроцент побед: " + player_info['wins_coof'] + "\nМеткость: " + player_info['accurance_coof'] + "\nВыжил: " + player_info['alived_coof'] + "\nСредний урон: " + player_info['avg_damage_per_fight'] + "\nЭффективность: " + player_info['efficiency'] + \
                        "\nWN7: " + player_info['WN7'] + "\nWN8: " + player_info['WN8'] + "\n➖➖➖➖ Неделя ➖➖➖➖\nЭффективность: " + player_info['w_efficiency'] + "\nWN7: " + player_info['w_wn7'] + \
                        "\nWN8: " + player_info['w_wn8'] + "\n➖➖➖➖ Месяц ➖➖➖➖\nЭффективность: " + \
                        player_info['m_efficiency'] + "\nWN7:" + \
                        player_info['m_wn7'] + "\nWN8: " + player_info['m_wn8']

                    vk.messages.send(
                        peer_id=2000000001,
                        message="Получена новая заявка на вступление в клан 😉\n\nИгровой ник: " +
                        users_database[str(event.obj.peer_id)]['nickname'] + "\nИмя: " + users_database[str(
                            event.obj.peer_id)]['name'] + "\n➖➖➖➖➖➖➖➖➖➖➖➖\n" + player_info__str + "\n➖➖➖➖➖➖➖➖➖➖➖➖",
                        random_id=get_random_id(),
                        keyboard=get_keyboard__inline_requests(choosed_emoji)
                    )
                    logging(userinfo, "Оставил заявку")
                elif ev == "tanks":
                    main_db['tanks'][str(event.obj.peer_id)]['path'].append(
                        event.obj.text)
                    kb = get_tanks_kb(event.obj.peer_id)
                    if not type(kb) is bool:
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message="Выберите " +
                            ("под-" * len(main_db['tanks']
                                          [str(event.obj.peer_id)]['path'])) + "категорию:",
                            random_id=get_random_id(),
                            keyboard=kb
                        )

                elif 'creating_event' in ev:
                    if not 'path' in main_db['steps'][str(event.obj.peer_id)]:
                        main_db['steps'][str(
                            event.obj.peer_id)]['path'] = list()
                    main_db['steps'][str(event.obj.peer_id)]['path'].append(
                        event.obj.text)

                    kb = {
                        "one_time": True,
                        "buttons": [
                        ]
                    }

                    if ev[14:] == 'type':
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = "creating_eventagainst"
                        if "Тренировка" in event.obj.text:
                            kb['buttons'].append([{
                                "action": {
                                    "type": "text",
                                    "label": "Нашего клана"
                                },
                                "color": "positive"
                            }])
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Против кого выступаем?',
                            keyboard=json.dumps(kb),
                            random_id=get_random_id()
                        )
                    elif ev[14:] == 'against':
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = "creating_eventdate"
                        import datetime
                        kb['buttons'].append([{
                            "action": {
                                "type": "text",
                                "label": datetime.datetime.now().strftime("%d.%m.%Y")
                            },
                            "color": "secondary"
                        }])
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Когда отправляемся?',
                            keyboard=json.dumps(kb),
                            random_id=get_random_id()
                        )
                    elif ev[14:] == 'date':
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = "creating_eventtime"
                        kb['buttons'].append([{
                            "action": {
                                "type": "text",
                                "label": "21:00"
                            },
                            "color": "secondary"
                        }, {
                            "action": {
                                "type": "text",
                                "label": "22:00"
                            },
                            "color": "secondary"
                        }, {
                            "action": {
                                "type": "text",
                                "label": "23:00"
                            },
                            "color": "secondary"
                        }])
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='В какое время отправляемся?',
                            keyboard=json.dumps(kb),
                            random_id=get_random_id()
                        )
                    elif ev[14:] == 'time':
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = "creating_eventkomandor"
                        kb['buttons'].append([{
                            "action": {
                                "type": "text",
                                "label": "Wysmoke"
                            },
                            "color": "primary"
                        }])
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Кто командир?',
                            keyboard=json.dumps(kb),
                            random_id=get_random_id()
                        )
                    elif ev[14:] == 'komandor':
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = "creating_eventmain_q"
                        kb['buttons'].append([{
                            "action": {
                                "type": "text",
                                "label": "5"
                            },
                            "color": "primary"
                        }, {
                            "action": {
                                "type": "text",
                                "label": "10"
                            },
                            "color": "primary"
                        }])
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Количество мест?',
                            keyboard=json.dumps(kb),
                            random_id=get_random_id()
                        )
                    elif ev[14:] == 'main_q':
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = "creating_eventadd_q"
                        kb['buttons'].append([{
                            "action": {
                                "type": "text",
                                "label": "Не требуется"
                            },
                            "color": "primary"
                        }])
                        kb['buttons'].append([{
                            "action": {
                                "type": "text",
                                "label": "5"
                            },
                            "color": "primary"
                        }, {
                            "action": {
                                "type": "text",
                                "label": "10"
                            },
                            "color": "primary"
                        }])
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Количество запасных?',
                            keyboard=json.dumps(kb),
                            random_id=get_random_id()
                        )
                    elif ev[14:] == "add_q":
                        vk.messages.send(
                            peer_id=admins_conversation,
                            message='❗️ Внимание ❗️\nСостоится битва против ' + main_db['steps'][str(event.obj.peer_id)]['path'][1] + ". \nТип сражения: " + main_db['steps'][str(event.obj.peer_id)]['path'][0] + ".\n" + main_db['steps'][str(event.obj.peer_id)]['path'][2] + " " + main_db['steps'][str(
                                event.obj.peer_id)]['path'][3] + "-UTC+3\nМиссией командует:\n➖➖ " + main_db['steps'][str(event.obj.peer_id)]['path'][4] + " ➖➖\n" + main_db['steps'][str(event.obj.peer_id)]['path'][5] + " (+" + main_db['steps'][str(event.obj.peer_id)]['path'][6] + ")",
                            keyboard=json.dumps(kb),
                            random_id=get_random_id()
                        )

                        try:
                            int(str(main_db['steps']
                                    [str(event.obj.peer_id)]['path'][6]))
                        except ValueError:
                            main_db['steps'][str(
                                event.obj.peer_id)]['path'][6] = 0

                        main_db['events'].append({
                            'against': main_db['steps'][str(event.obj.peer_id)]['path'][1],
                            'type': main_db['steps'][str(event.obj.peer_id)]['path'][0],
                            'date': main_db['steps'][str(event.obj.peer_id)]['path'][2],
                            'time': main_db['steps'][str(event.obj.peer_id)]['path'][3],
                            'main_q': int(str(main_db['steps'][str(event.obj.peer_id)]['path'][5])),
                            'add_q': int(str(main_db['steps'][str(event.obj.peer_id)]['path'][6])),
                            'komandor': main_db['steps'][str(event.obj.peer_id)]['path'][4],
                            'registered': []
                        })

                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Событие создано!',
                            keyboard=get_keyboard_main(event.obj.peer_id),
                            random_id=get_random_id()
                        )

                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = ""
                        del main_db['steps'][str(event.obj.peer_id)]['path']
                elif 'regevent' in ev:
                    logging(userinfo, event.obj.text + " в событии")
                    event_id = int(ev[8:])
                    if event.obj.text == "Участвую!":
                        main_db['events'][event_id]['main_q'] -= 1
                        main_db['events'][event_id]['registered'].append(
                            [event.obj.peer_id, 'main'])
                    elif event.obj.text == "Не прийду!":
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message="Понял тебя.",
                            keyboard=get_keyboard_main(event.obj.peer_id),
                            random_id=get_random_id()
                        )
                        continue
                    else:
                        main_db['events'][event_id]['add_q'] -= 1
                        main_db['events'][event_id]['registered'].append(
                            [event.obj.peer_id, 'add'])

                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Принято! Ждем тебя в ' +
                        main_db['events'][event_id]['date'] + " " +
                        main_db['events'][event_id]['time'] +
                        " по мск в игре!",
                        keyboard=get_keyboard_main(event.obj.peer_id),
                        random_id=get_random_id()
                    )

                    main_db['steps'][str(event.obj.peer_id)
                                     ]['last_action'] = ""
                elif 'editevent' in ev:
                    if event.obj.text in params.keys():
                        main_db['steps'][str(
                            event.obj.peer_id)]['last_action'] = "setparam_" + params[event.obj.text] + "_" + ev[9:]

                        kb = {
                            "one_time": True,
                            "buttons": [
                                [{
                                    "action": {
                                        "type": "text",
                                        "label": "🏠 Домой"
                                    },
                                    "color": "secondary"
                                }]
                            ]
                        }

                        if params[event.obj.text] == 'type':
                            kb = {
                                "one_time": True,
                                "buttons": [
                                    [{
                                        "action": {
                                            "type": "text",
                                            "label": "🏠 Домой"
                                        },
                                        "color": "secondary"
                                    }], [{
                                        "action": {
                                            "type": "text",
                                            "label": "⚒ Сражения"
                                        },
                                        "color": "negative"
                                    }, {
                                        "action": {
                                            "type": "text",
                                            "label": "👨‍🏫 Тренировка"
                                        },
                                        "color": "secondary"
                                    }],
                                    [{
                                        "action": {
                                            "type": "text",
                                            "label": "🗺 Разбор карты"
                                        },
                                        "color": "positive"
                                    }]
                                ]
                            }

                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Введите значение',
                            keyboard=json.dumps(kb),
                            random_id=get_random_id()
                        )
                elif 'setparam_' in ev:
                    main_db['events'][int(ev.split('_')[2])][ev.split('_')[
                        1]] = event.obj.text
                    main_db['steps'][str(event.obj.peer_id)
                                     ]['last_action'] = ""
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Принято!',
                        keyboard=get_keyboard_main(event.obj.peer_id),
                        random_id=get_random_id()
                    )
                else:
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Я не знаю такой команды',
                        keyboard=get_keyboard_main(event.obj.peer_id),
                        random_id=get_random_id()
                    )
                    continue
        else:
            try:
                if "Принять" in event.obj.text:
                    if check_admin(event.obj.from_id):
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Принятие заявки',
                            random_id=get_random_id()
                        )
                        to_add = main_db['requests'][event.obj.text[event.obj.text.find(
                            "Принять") + 8:]]

                        vk.messages.send(
                            peer_id=to_add,
                            message='✅ Ваша заявка на вступление в клан принята! Через несколько минут вы будете добавлены в группу.',
                            random_id=get_random_id(),
                            keyboard=get_keyboard_main(to_add)
                        )
                        del main_db['requests'][event.obj.text[event.obj.text.find(
                            "Принять") + 8:]]
                    else:
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Недостаточно прав!',
                            random_id=get_random_id(),
                            keyboard=get_keyboard_main(event.obj.peer_id)
                        )
                elif "Отклонить" in event.obj.text:
                    if check_admin(event.obj.from_id):
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Отклонение заявки',
                            random_id=get_random_id()
                        )
                        to_add = main_db['requests'][event.obj.text[event.obj.text.find(
                            "Отклонить") + 9:]]

                        vk.messages.send(
                            peer_id=to_add,
                            message='⚠️ Ваша заявка на вступление в клан отклонена! Возможно, вы не вступили в группу, или не соответствуете требованиям.',
                            random_id=get_random_id(),
                            keyboard=get_keyboard_main(to_add)
                        )
                        del main_db['requests'][event.obj.text[event.obj.text.find(
                            "Отклонить") + 9:]]
                    else:
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='Недостаточно прав!',
                            random_id=get_random_id()
                        )
            except KeyError:
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Ошибка',
                    random_id=get_random_id()
                )

    autosave_db_step_2()

    time.sleep(longpool_sleep)
