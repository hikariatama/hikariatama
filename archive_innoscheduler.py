#from config import *
script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + "/"
fsm_path = script_path + 'fsm.json'

texts = {
	'rus': {
		'working_hours': '_Театр работает ежедневно с 9:00 до 19:00 😌_',
		'idk_answer': '🤷‍♂️ *Извините, я Вас не понимаю.* Пожалуйста, воспользуйтесь кнопочным меню. Если Вам нужна помощь, Вы можете обратиться в *Техническую поддержку театра*, написав на почту *support-tuz@bileton.ru* (_ежедневно с 8:00 до 20:00_)',
		'main_menu': '*Привет!* 👋 Я интерактивный бот-помощник *Казанского ТЮЗа!* Здесь Вы можете ознакомиться с информацией о нашем театре, узнать его историю, расписание работы, а также приобрести билеты.\n_Адрес: _[г. Казань, ул. Островского, 10](https://yandex.ru/maps/43/kazan/?from=api-maps&ll=49.113313%2C55.790875&mode=routes&rtext=~55.789389%2C49.113386&rtt=auto&ruri=~&utm_source=api-maps&z=16)\n\nТакже, у нас есть навык в голосовом помощнике Алиса! Чтобы запустить его, скажите "Алиса, запусти навык Театр Юного Зрителя"',
		'help': 'Если Вам нужна помощь, Вы можете обратиться в *Техническую поддержку театра*, написав на почту *support-tuz@bileton.ru* или позвонив по телефону *+7 (843) 292-18-75* (_ежедневно с 8:00 до 20:00_)',
		'lang_saved': '✅ Язык сохранен', 
		'invite': 'Привет! 👋 Приглашаю Вас пойти со мной на постановку *"@title@"* в Казанский ТЮЗ.\nОна будет проходить *@datetime@*.\nДлительность: *@time@*\nВозрастное ограничение: *@age_restriction@*!\n\n_Купить билеты можно на _[сайте ТЮЗа](@link@)_, или _*в новом Телеграм-боте: @innoscheduler_bot*',
		'session_info': 'Постановка "*@title@*"\n⌚️ Дата и время: *@datetime@*\n🕔 Продолжительность: *@time@*\n👨‍👩‍👦‍👦 Возрастное ограничение: *@age_restriction@*\n\nРекомендуем приобретать билеты и приходить на сеанс заранее! Приятного просмотра!',
		'buy_ticket': '🎟 Купить билет'
	}, 
	'eng': {
		'working_hours': '_TUZ is open every day from 9 a.m. to 7 p.m. 😌_',
		'idk_answer': '🤷‍♂️ *Sorry, I don’t understand You.* Please, use push-button menu. If You need any help, You can ask for it in *Technical Support of the TUZ* by writing to *support-tuz@bileton.ru* (_from 8 a.m. to 8 p.m. every day_)',
		'main_menu': '*Hi!* 👋 I am an interactive helper-bot of *Kazan TUZ!* Here You can find any information You may need about our theater, learn its history, working hours and also buy tickets.\nAddress: _[10, Ostrovskogo st., Kazan](https://yandex.ru/maps/43/kazan/?from=api-maps&ll=49.113313%2C55.790875&mode=routes&rtext=~55.789389%2C49.113386&rtt=auto&ruri=~&utm_source=api-maps&z=16)',
		'help': '🙋‍♂️ If You need any help, You can ask for it in *Technical Support of the TUZ* by writing to *support-tuz@bileton.ru* or calling to *+7 (843) 292-18-75* (_from 8 a.m. to 8 p.m. every day_)',
		'lang_saved': '✅ Language saved', 
		'invite': 'Hi! 👋 I invite You to go with me to the performance called *"@title@"* to Kazan TUZ.\nIt will take place on *@datetime@*.\nDuration: *@time@*\nAge restriction: *@age_restriction@*!\n\n_You can buy tickets on _[TUZ\'s official website](@link@)_ or using our _*new telegram-bot: @innoscheduler_bot*',
		'session_info': 'Performance "*@title@*"\n⌚️ Date and Time: *@datetime@*\n🕔 Duration: *@time@*\n👨‍👩‍👦‍👦 Age restriction: *@age_restriction@*\n\nWe recommend buying tickets and showing up to permormance in advance! Enjoy!',
		'buy_ticket': '🎟 Buy ticket'
	},
	'tat': {
		'working_hours': '_Эш расписаниесе: 9:00 — 19:00. Көн саен 😌_',
		'idk_answer': '🤷‍♂️ *Гафу итегез, мин сезне аңламыйм.* Зинһар, кнопкалы менюдан файдаланыгыз. Сезгә ярдәм кирәк булса, *support-tuz@bileton.ru* (_көн саен 8:00 дән 20:00_) хат язып *Театрга техник ярдәм* сорый аласыз.',
		'main_menu': '*Исәнмесез!* 👋 Мин *Казан яшьләр театрының* интерактив бот-ярдәмчесе! Монда сез безнең театр турында мәгълүмат таба аласыз, аның тарихын, эш вакытын белә аласыз, шулай ук билетлар сатып ала аласыз.\n_Адрес: _[г. Казань, ул. Островского, 10](https://yandex.ru/maps/43/kazan/?from=api-maps&ll=49.113313%2C55.790875&mode=routes&rtext=~55.789389%2C49.113386&rtt=auto&ruri=~&utm_source=api-maps&z=16)',
		'help': '🙋‍♂️ Сезгә ярдәм кирәк булса, *support-tuz@bileton.ru* адресына язып яки *+ 7 (843) 292-18-75* телефонына шалтыратып ярдәм өчен *Театрның техник ярдәме* белән мөрәҗәгать итә алагыз. (_көн саен 8:00 дән 20:00_).',
		'lang_saved': '✅ Тел сакланган', 
		'invite': 'Исәнмесез! 👋 Мин сезне минем белән Казан Яшьләр Театрында *"@title@"* спектакленә чакырам.\nУл *@datetime@* була.\nОзынлыгы: *@time@*\nЯшь чикләре: *@age_restriction@*!\n\n_Билетларны _[Яшьләр театры сайтында](@link@)_ яки яңа _*Телеграм ботында алырга мөмкин: @innoscheduler_bot*',
		'session_info': 'Куелыш "*@title@*"\n⌚️ Көн һәм вакыт: *@datetime@*\n🕔 Озынлыгы: *@time@*\n👨‍👩‍👦‍👦 Яшь чикләре: *@age_restriction@*\n\nБилетларны алдан сатып алырга hәм сеанска алдан килергә киңәш бирәбез! Бәхетле карау!',
		'buy_ticket': '🎟 Билет сатып алырга'
	}
}

import telebot
import json

from random import randint
import requests
from time import time, sleep
import difflib
from flask import Flask, request
import threading

app = Flask(__name__)
alice_id = '<alice-id>'
oauth = '<yandex-oauth>'


def similarity(s1, s2):
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


def generate_session_info_response(session):
    age = 'Для зрителей старше ' + session['age_restriction'][:-1] + ' лет'
    if session['age_restriction'][:-1] == '0':
        age = 'Без возрастных ограничений'
    return {
        "response": {
            "text": "Информация о спектакле " + session['title'] + '. Время представления: ' + session[
                'datetime'] + '. Длительность сеанса: ' + session['time'] + '. ' + age,
            "card": {
                "type": "BigImage",
                "image_id": session['ya_image_id'],
                "title": session['title'] + ' | ' + session['age_restriction'],
                "description": '⌚️ {0} | 🕔 {1}'.format(session['datetime'], session['time']),
                "button": {
                    "text": "Надпись",
                    "url": session['link'],
                    "payload": {}
                }
            },
            "end_session": True
        },
        "version": "1.0"
    }


easter = False


@app.route('/simpledimple', methods=['POST'])
def simpledimple():
    # //todo: АЛИСА: описание+фото, история+фото, маршрут, этика; БОТ: маршрут, описание+фото
    global easter
    command = json.loads(request.data)['request']['command']
    print('Alice: "' + command + '"')
    if command == "":
        response = {
            "response": {
                "text": "Привет! Я помогу вам ориентироваться по Казанскому ТЮЗу. Спросите у меня про афишу, сам театр или конкретную постановку.",
                "end_session": False
            },
            "version": "1.0"
        }
        return json.dumps(response, ensure_ascii=False, indent=2)

    if easter:
        response = {
            "response": {
                "text": "Добавляй",
                "end_session": True
            },
            "version": "1.0"
        }
        easter = False
        return json.dumps(response, ensure_ascii=False, indent=2)

    if 'что ты умеешь' in command or 'помощь' in command:
        response = {
            "response": {
                "text": "Ты можешь спросить меня об афише, театре, конкретной постановке, и я с удовольствием отвечу.",
                "end_session": True
            },
            "version": "1.0"
        }
        easter = False
        return json.dumps(response, ensure_ascii=False, indent=2)

    if ' бот' in command:
        response = {
            "response": {
                "text": "Узнавать информацию можно в нашем Телеграм боте. Нажмите на фото для перехода.",
                "card": {
                    "type": "BigImage",
                    "image_id": '1652229/3fcf72f85710f2c22527',
                    "title": 'InnoScheduler | Ваш помощник в Казанском ТЮЗе',
                    "description": 'Интерактивный бот-помощник в Телеграм',
                    "button": {
                        "text": "Надпись",
                        "url": 'https://t.me/innoscheduler_bot',
                        "payload": {}
                    }
                },
                "end_session": True
            },
            "version": "1.0"
        }
        return json.dumps(response, ensure_ascii=False, indent=2)

    activators = ['время работы', 'расписание работы', 'расписание тюза', 'расписание кассы']

    for key in activators:
        if key in command:
            response = {
                "response": {
                    "text": "Касса работает с 9:00 до 19:00 ежедневно.\nТехническая поддержка отвечает с 8:00 до 20:00",
                    "tts": 'Ежедневно с 9:00 до 19:00',
                    "end_session": True
                },
                "version": "1.0"
            }
            return json.dumps(response, ensure_ascii=False, indent=2)

    activators = ['описание театра', 'описание тюза', 'про тюз', 'о театре', 'о тюзе']

    for key in activators:
        if key in command:
            response = {
                "response": {
                    "text": "Первый спектакль состоялся 30 ноября 1932 года. Это один из первых театров России, получивший высшую театральную премию \"Золотая Маска\". В репертуаре театра - тридцать четыре спектакля. Адрес кассы: Казань, Островского, 10",
                    "tts": "Первый спектакль состоялся 30 ноября 1932 года. Это один из первых театров России, получивший высшую театральную премию \"Золотая Маска\". В репертуаре театра - тридцать четыре спектакля. Адрес кассы: Казань, Островского, 10",
                    "card": {
                        "type": "BigImage",
                        "image_id": '1540737/352b2c5a798fbbe0f9bf',
                        "title": 'Театр Юного Зрителя в Казани',
                        "description": 'Адрес кассы: Казань, Островского, 10'
                    },
                    "end_session": True
                },
                "version": "1.0"
            }
            return json.dumps(response, ensure_ascii=False, indent=2)

    if 'буфет' in command:
        response = {
            "response": {
                "text": "Буфет находится как раз на пути между гардеробом и коридором, ведущим в помещение со сценой. Очень много сладостей по демократическим ценам",
                "end_session": True
            },
            "version": "1.0"
        }
        return json.dumps(response, ensure_ascii=False, indent=2)

    activators = ['афиш', 'расписание', 'спектакли', 'постановки', 'сеансы']

    for key in activators:
        if key in command:
            afisha = ''
            found = []
            for session in sessions:
                if session['title'] in found:
                    continue
                found.append(session['title'])
                afisha += session['title'] + ' ' + session['age_restriction'] + ' | ' + session['datetime'][
                                                                                        :session['datetime'].find(
                                                                                            '(')] + session['datetime'][
                                                                                                    session[
                                                                                                        'datetime'].find(
                                                                                                        ')') + 2:] + '\n'

            afisha = afisha[:1000]

            print(afisha)

            response = {
                "response": {
                    "text": afisha,
                    "tts": 'Представляю Вам афишу',
                    "end_session": True
                },
                "version": "1.0"
            }
            return json.dumps(response, ensure_ascii=False, indent=2)

    if 'симпл димпл' in command:
        response = {
            "response": {
                "text": "Что ты мне дашь за этот симпл димпл?",
                "card": {
                    "type": "BigImage",
                    "image_id": '1521359/a9f58c14e935778c8023',
                    "title": 'Симпл Димпл',
                    "description": 'Это не попыт',
                    "button": {
                        "text": "Надпись",
                        "url": 'https://innostudy.ru',
                        "payload": {}
                    }
                },
                "end_session": False
            },
            "version": "1.0"
        }
        easter = True
        return json.dumps(response, ensure_ascii=False, indent=2)

    show_info = ['покажи информацию о сеансе', 'сеанс', 'спектакль', 'постановка', 'представление',
                 'информация о спектакле', 'информация о сеансе', 'покажи информацию о спектакле',
                 'покажи информацию о постановке', 'информация о постановке', 'расскажи о спектакле',
                 'расскажи о сеансе', 'покажи спектакль', 'покажи сеанс', 'расскажи о постановке', 'покажи постановку',
                 'расскажи про постановку', 'расскажи про спектакль', 'расскажи про сеанс']

    show_info.sort(key=len, reverse=True)

    for session in sessions:
        if similarity(command, session['title'].lower()) >= .7:
            response = generate_session_info_response(session)
            return json.dumps(response, ensure_ascii=False, indent=2)

    for key in show_info:
        if key in command:
            command = command[len(key) + 1:]
            for session in sessions:
                if similarity(command, session['title'].lower()) >= .7:
                    response = generate_session_info_response(session)
                    return json.dumps(response, ensure_ascii=False, indent=2)

    response = {
        "response": {
            "text": "Не понимаю Вас. Пожалуйста, попробуйте еще раз.",
            "end_session": False
        },
        "version": "1.0"
    }
    easter = False
    return json.dumps(response, ensure_ascii=False, indent=2)


sessions = json.loads(open(script_path + 'sessions.json', 'r').read())['sessions']

bot = telebot.TeleBot(token='<api-token>')

try:
    fsm = json.loads(open(fsm_path, 'r').read())
except:
    fsm = {}

lang_kb = telebot.types.InlineKeyboardMarkup()
lang_kb.add(telebot.types.InlineKeyboardButton('🇷🇺 Русский', callback_data='setlang_rus'))
lang_kb.add(telebot.types.InlineKeyboardButton('🇺🇸 English', callback_data='setlang_eng'))
lang_kb.add(telebot.types.InlineKeyboardButton('🇭🇺 Татар теле', callback_data='setlang_tat'))


def save_db():
    open(fsm_path, 'w').write(json.dumps(fsm))


def ss(usid, status):
    global fsm
    usid = str(usid)
    if usid not in fsm:
        fsm[usid] = {'fsm': ''}

    fsm[usid]['fsm'] = status


def gs(usid):
    usid = str(usid)
    if usid not in fsm:
        return ''

    return fsm[usid]['fsm']


def get_main_kb(usid):
    lang = get_lang(str(usid))
    if not lang:
        return

    main_kb = telebot.types.InlineKeyboardMarkup()

    if lang == "rus":
        main_kb.add(telebot.types.InlineKeyboardButton('⌚️ Расписание работы', callback_data='working_hours'),
                    telebot.types.InlineKeyboardButton('❓ Помощь', callback_data='help'))
        main_kb.add(telebot.types.InlineKeyboardButton('💌 Отправить приглашение другу', switch_inline_query=''))
        main_kb.add(telebot.types.InlineKeyboardButton('📲 Все спектакли', switch_inline_query_current_chat=''))
    elif lang == "eng":
        main_kb.add(telebot.types.InlineKeyboardButton('⌚️ Working hours', callback_data='working_hours'),
                    telebot.types.InlineKeyboardButton('❓ Help', callback_data='help'))
        main_kb.add(telebot.types.InlineKeyboardButton('💌 Send invite to Your friend', switch_inline_query=''))
        main_kb.add(telebot.types.InlineKeyboardButton('📲 All sessions', switch_inline_query_current_chat=''))
    elif lang == "tat":
        main_kb.add(telebot.types.InlineKeyboardButton('⌚️ Эш расписаниесе', callback_data='working_hours'),
                    telebot.types.InlineKeyboardButton('❓ Ярдәм', callback_data='help'))
        main_kb.add(telebot.types.InlineKeyboardButton('💌 Дустыңа чакыру җибәргә', switch_inline_query=''))
        main_kb.add(telebot.types.InlineKeyboardButton('📲 Барлыгы спектакльләр', switch_inline_query_current_chat=''))

    return main_kb


def get_go_kb(usid):
    lang = get_lang(str(usid))
    if not lang:
        return

    go_kb = telebot.types.InlineKeyboardMarkup()

    if lang == "rus":
        go_kb.add(telebot.types.InlineKeyboardButton('🎟 Перейти в бота', url='https://t.me/innoscheduler_bot'))
    elif lang == "eng":
        go_kb.add(telebot.types.InlineKeyboardButton('🎟 Go to bot', url='https://t.me/innoscheduler_bot'))
    elif lang == "tat":
        go_kb.add(telebot.types.InlineKeyboardButton('🎟 Ботны ачарга', url='https://t.me/innoscheduler_bot'))

    return go_kb


def answer(destination, msg, reply_markup=None, parse_mode="Markdown", reply_to_message_id=None):
    try:
        destination = int(destination)
    except:
        pass

    if isinstance(destination, telebot.types.CallbackQuery):
        try:
            return bot.edit_message_text(chat_id=destination.message.chat.id, message_id=destination.message.message_id,
                                         text=msg, reply_markup=reply_markup, parse_mode=parse_mode,
                                         disable_web_page_preview=True)
        except telebot.apihelper.ApiException as e:
            bot.answer_callback_query(callback_query_id=destination.id)
    elif isinstance(destination, telebot.types.Message):
        return bot.send_message(chat_id=destination.chat.id, text=msg, reply_markup=reply_markup, parse_mode=parse_mode,
                                reply_to_message_id=reply_to_message_id, disable_web_page_preview=True)
    elif isinstance(destination, int) or (isinstance(destination, str) and destination.startswith("@")):
        return bot.send_message(chat_id=destination, text=msg, reply_markup=reply_markup, parse_mode=parse_mode,
                                reply_to_message_id=reply_to_message_id, disable_web_page_preview=True)


def get_lang(usid):
    global fsm
    if usid not in fsm or 'lang' not in fsm[usid] or fsm[usid]['lang'] not in texts.keys():
        answer(usid,
               '*Пожалуйста, выберите язык для работы бота\nPlease, choose the language\nЗинһар, бот эшләсен өчен телне сайлагыз*',
               reply_markup=lang_kb)
        return False

    return fsm[usid]['lang']


def to_tatar(line):
    line = line.replace('понедельник', 'Дүшәмбе көнне').replace('вторник', 'Сишәмбе көнне').replace('среда',
                                                                                                    'чәршәмбе көнне')
    line = line.replace('четверг', 'Пәнҗешәмбе көнне').replace('пятница', 'Җомга көнне').replace('суббота',
                                                                                                 'Шимбә көнне').replace(
        'воскресенье',
        'Якшәмбедә көнне')
    line = line.replace('часа', 'сәгать').replace('часов', 'сәгать').replace('час', 'сәгать')
    line = line.replace('минута', 'минут').replace('минуты', 'минут').replace('минут', 'минут')
    line = line.replace('января', 'гыйнвар').replace('февраля', 'февраль').replace('марта', 'март')
    line = line.replace('апреля', 'апрель').replace('мая', 'май').replace('июня', 'июнь')
    line = line.replace('июля', 'июль').replace('августа', 'август').replace('сентября', 'сентябрь')
    line = line.replace('октября', 'октябрь').replace('ноября', 'ноябрь').replace('декабря', 'декабрь')
    return line


def to_english(line):
    line = line.replace('понедельник', 'Mon').replace('вторник', 'Tue').replace('среда', 'Wed')
    line = line.replace('четверг', 'Thu').replace('пятница', 'Fri').replace('суббота', 'Sat').replace('воскресенье',
                                                                                                      'Sun')
    line = line.replace('часа', 'hrs').replace('часов', 'hrs').replace('час', 'hr')
    line = line.replace('минута', 'min').replace('минуты', 'min').replace('минут', 'min')
    line = line.replace('января', 'of January').replace('февраля', 'of February').replace('марта', 'of March')
    line = line.replace('апреля', 'of April').replace('мая', 'of May').replace('июня', 'of June')
    line = line.replace('июля', 'of July').replace('августа', 'of August').replace('сентября', 'of September')
    line = line.replace('октября', 'of October').replace('ноября', 'of November').replace('декабря', 'of December')
    return line


@bot.message_handler(commands=['start'])
def start_message(message):
    global fsm
    usid = str(message.from_user.id)

    if usid not in fsm:
        fsm[usid] = {'fsm': ''}
        save_db()

    lang = get_lang(usid)
    if not lang:
        return

    answer(message, texts[lang]['main_menu'], reply_markup=get_main_kb(usid))


@bot.message_handler(commands=['change_language'])
def change_language_router(message):
    global fsm
    usid = str(message.from_user.id)
    if usid in fsm and 'lang' in fsm[usid]:
        del fsm[usid]['lang']
        save_db()

    get_lang(usid)


admins = [659800858]


@bot.message_handler(commands=['sendall'])
def sendall(message):
    if message.from_user.id not in admins:
        return

    counter = 0
    for user, data in fsm.items():
        try:
            answer(user, message.text[9:])
            counter += 1
        except:
            pass

    answer(message, "Отправлено " + str(counter) + " пользователям")


@bot.message_handler(content_types=['text'])
def text_message(message):
    usid = str(message.from_user.id)
    lang = get_lang(usid)
    if not lang:
        return

    if 'event#' in message.text:
        event_id = message.text[message.text.find('event#') + 6:]
        for session in sessions:
            if session['id'] == event_id:
                session_info = texts[lang]['session_info'].replace('@title@', session['title']).replace('@datetime@',
                                                                                                        session[
                                                                                                            'datetime']).replace(
                    '@time@', session['time']).replace('@age_restriction@', session['age_restriction']).replace(
                    '@link@', session['link'])

                temp_kb = get_main_kb(usid)
                temp_kb.add(telebot.types.InlineKeyboardButton(texts[lang]['buy_ticket'], url=session['link']))

                bot.send_photo(chat_id=message.chat.id, photo=session['image_src'], caption=session_info,
                               reply_markup=temp_kb, parse_mode="Markdown")
                return

    answer(message, texts[lang]['idk_answer'], reply_markup=get_main_kb(usid))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global fsm
    usid = str(call.from_user.id)
    if not 'setlang' in call.data:
        lang = get_lang(usid)
        if not lang:
            return

    if call.data == "working_hours":
        answer(call, texts[lang]['working_hours'], reply_markup=get_main_kb(usid))
    elif call.data == "help":
        answer(call, texts[lang]['help'], reply_markup=get_main_kb(usid))
    elif call.data.startswith('setlang'):
        language = call.data.split('_')[1]
        if usid not in fsm:
            fsm[usid] = {'fsm': ''}
        fsm[usid]['lang'] = language
        save_db()
        bot.answer_callback_query(call.id, texts[language]['lang_saved'])
        answer(call, texts[language]['main_menu'], reply_markup=get_main_kb(usid))


@bot.inline_handler(func=lambda query: True)
def query_text(inline_query):
    bot.answer_inline_query(inline_query.id, search_available_sessions(inline_query.query, inline_query.from_user.id),
                            cache_time=1)


def search_available_sessions(query, usid):
    usid = str(usid)
    if usid not in fsm:
        return [telebot.types.InlineQueryResultArticle(
            id=time(),
            title='You need to activate the bot!',
            input_message_content=telebot.types.InputTextMessageContent(
                '.'
            ),
            description='Перейдите в бота и нажмите START\nGo to bot and click START\nБот эчендә керегез һәм START басыгыз',
            thumb_height=1
        )]

    lang = get_lang(usid)
    if not lang:
        lang = 'eng'

    result = []
    if len(query) > 0:
        for session in sessions:
            if query.lower() not in session['title'].lower():
                continue
            if len(result) < 15:
                invite = texts[lang]['invite'].replace('@title@', session['title']).replace('@datetime@', session[
                    'datetime']).replace('@time@', session['time']).replace('@age_restriction@',
                                                                            session['age_restriction']).replace(
                    '@link@', session['link']) + '\n_event#' + str(session['id']) + '_'
                title = session['title'] + ' ' + session['age_restriction']
                desc = '⌚️ {0}\n🕔 {1}'.format(session['datetime'], session['time'])
                if lang == 'eng':
                    invite = to_english(invite)
                    title = to_english(title)
                    desc = to_english(desc)
                elif lang == 'tat':
                    invite = to_tatar(invite)
                    title = to_tatar(title)
                    desc = to_tatar(desc)

                result.append(
                    telebot.types.InlineQueryResultArticle(
                        id=time(),
                        title=title,
                        input_message_content=telebot.types.InputTextMessageContent(
                            parse_mode='Markdown',
                            message_text=invite,
                            disable_web_page_preview=True
                        ),
                        description=desc,
                        thumb_url=session['image_src'],
                        reply_markup=get_go_kb(usid)
                    )
                )
            else:
                break
    else:
        for session in sessions:
            if len(result) < 15:
                invite = texts[lang]['invite'].replace('@title@', session['title']).replace('@datetime@', session[
                    'datetime']).replace('@time@', session['time']).replace('@age_restriction@',
                                                                            session['age_restriction']).replace(
                    '@link@', session['link']) + '\n_event#' + str(session['id']) + '_'
                title = session['title'] + ' ' + session['age_restriction']
                desc = '⌚️ {0}\n🕔 {1}'.format(session['datetime'], session['time'])
                if lang == 'eng':
                    invite = to_english(invite)
                    title = to_english(title)
                    desc = to_english(desc)
                elif lang == 'tat':
                    invite = to_tatar(invite)
                    title = to_tatar(title)
                    desc = to_tatar(desc)

                result.append(
                    telebot.types.InlineQueryResultArticle(
                        id=time(),
                        title=title,
                        input_message_content=telebot.types.InputTextMessageContent(
                            parse_mode='Markdown',
                            message_text=invite,
                            disable_web_page_preview=True
                        ),
                        description=desc,
                        thumb_url=session['image_src'],
                        reply_markup=get_go_kb(usid)
                    )
                )
            else:
                break
    return result


def start_app():
    app.run(port=5000)


def start_bot():
    bot.polling(timeout=123, interval=0, none_stop=True)


def update_sessions():
    global sessions
    while True:
        sessions = json.loads(open(script_path + 'sessions.json', 'r').read())['sessions']
        sleep(120)


threading.Thread(target=start_app).start()
threading.Thread(target=start_bot).start()
threading.Thread(target=update_sessions).start()
