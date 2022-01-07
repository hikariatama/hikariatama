import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import telebot
import json
import os
script_path = os.path.dirname(os.path.abspath(__file__)) + "/"

types = telebot.types
bot = telebot.TeleBot('<api-token>')

BUTTONS_IN_ROW = 1

questions = ['*В какой день и какое время вам удобна уборка?*',
             '*Введите контакт для связи*. Это может быть телефон или @username в Телеграм.']


def read_db():
    global db
    try:
        with open(script_path + "main_database.json", 'r') as f:
            temp = json.loads(f.read())
            db = dict()
            for key, value in temp.items():
                db[int(key)] = value

    except Exception as e:
        db = dict()
        print("DATABASE READ ERROR")
        print(e)


read_db()


def save_db():
    global db
    with open(script_path + "main_database.json", 'w') as f:
        f.write(json.dumps(db))


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '/var/www/html/bot/sheets_service.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId="<spreadsheet>",
                            range="user!A2:Z1000").execute()
values = result.get('values', [])

formatted_prices = {}
unformatted_prices = {}
for row in values:
    formatted_prices[row[0]] = row[3].format(n=row[2])
    unformatted_prices[row[0]] = row[2]


def log_msg(from_user, msg):
    pass


services_db = {
    '🏠 Уборка квартиры': {
        '🧹 Стандартная уборка: ' + formatted_prices['standart_clean']: ['➕ Стандартная уборка 🧹: ' + formatted_prices['standart_clean']],
        '🌀 Генеральная уборка: ' + formatted_prices['full_clean']: ['➕ Генеральная уборка 🌀: ' + formatted_prices['full_clean']],
        '🕎 Дополнительные услуги': [
            '➕ Отдельное мытье санузла: ' +
            formatted_prices['toilet_clean'],
            '➕ Генеральное мытье кухни: ' +
            formatted_prices['kitchen_clean'],
            '➕ Мытье СВЧ: ' + formatted_prices['shf_clean'],
            '➕ Мытье холодильника: ' +
            formatted_prices['fridge_clean'],
            '➕ Мытье духовки: ' + formatted_prices['oven_clean'],
            '➕ Мытье вытяжки: ' + formatted_prices['hood_clean']
        ]
    },
    '🛋 Химчистка мебели (с выездом)': [
        '➕ Диван прямой: ' + formatted_prices['sofa_direct'],
        '➕ Диван угловой: ' + formatted_prices['sofa_corner'],
        '➕ Матрац (1 сторона): ' + formatted_prices['mattress_solo'],
        '➕ Матрац (2 стороны): ' + formatted_prices['mattress_duo']
    ],
    '🖼 Мойка окон': [
        '➕ Мойка окон: ' + formatted_prices['windows']
    ],
    '💧 Химчистка постельного белья и штор': [
        '➕ Шторы: ' + formatted_prices['curtains'],
        '➕ Постельное белье: ' + formatted_prices['linens']
    ]
}

calculator_db = {
    '🧹 Стандартная уборка': unformatted_prices['standart_clean'],
    '🌀 Генеральная уборка': unformatted_prices['full_clean']
}

info_db = {
    '🧹 Стандартная уборка': 'standart_clean',
    '🌀 Генеральная уборка': 'full_clean'
}

additional_info = {
    '0_0': '💠 Влажная уборка пола и плинтусов (применение профессиональных средств)\n💠 Протирка пыли со всех поверхностей и предметов \n💠 Уборка санузла (мытье плитки, раковины, унитаза, ванны, смесителя, и.т.д)\n💠 Уборка кухни (кухонного гарнитура снаружи, внутри если предметы убраны, варочной панели, плиты, смесителей, вытяжки, мойка раковины, рабочей поверхности)\n💠 Вынос мусора до 10 кг',
    '0_1': '💠 Протирка пыли со всех поверхностей и предметов \n💠 Сухая уборка пылесосом (ковровые покрытия)\n💠 Влажная уборка пола и плинтусов (применение профессиональных средств)\n💠 Мытье дверей и дверных блоков, подоконников, зеркальных поверхностей\n💠 Влажная уборка фасадов шкафов и тумб снаружи (внутри если пусто)\n💠 Удаление пыли с потолочных светильников и люстр\n💠 Удаление пыли с выключателей, розеток и радиаторов\n💠 Уборка санузла (мытье плитки, раковины, унитаза, ванны, душевой кабины, смесителя, и.т.д)\n💠 Уборка кухни (кухонного гарнитура снаружи, внутри если предметы убраны, варочной панели, плиты, смесителей, вытяжки, мойка раковины, рабочей поверхности)\n💠 Вынос мусора до 10 кг'
}


def get_item_by_path(path):
    unformatted_result = services_db

    if path[0] != "":
        for path_item in path:
            if type(unformatted_result) == dict:
                unformatted_result = list(unformatted_result.items())[
                    int(path_item)][1]
            elif type(unformatted_result) in [list, set]:
                unformatted_result = unformatted_result[int(path_item)]

    return unformatted_result


def get_kb(path='', user=None):
    path = path.split("_")
    unformatted_result = get_item_by_path(path)
    result = []

    result_markup = types.InlineKeyboardMarkup()
    i = 0

    joined_path = '_'.join(path) + "_" if '_'.join(path) != "" else ''

    def for_def(result_item, tmp, i):
        if type(tmp) in [list, dict, set]:
            # print(i)
            result.append(types.InlineKeyboardButton(
                result_item, callback_data='path_' + joined_path + str(i)))
        elif type(tmp) == str:
            result.append(types.InlineKeyboardButton(
                result_item, callback_data='order_' + joined_path + str(i)))
        elif tmp == None:
            result.append(types.InlineKeyboardButton(
                result_item, callback_data='order_' + joined_path + str(i)))

    if type(unformatted_result) == dict:
        for result_item, tmp in unformatted_result.items():
            for_def(result_item, tmp, i)
            i += 1
    else:
        for result_item in unformatted_result:
            for_def(result_item, None, i)
            i += 1

    for i in range(0, len(result), BUTTONS_IN_ROW):
        result_markup.add(*result[i:i+BUTTONS_IN_ROW])

    if path[0] != "":
        result_markup.add(types.InlineKeyboardButton(
            '👈 Назад', callback_data='path_' + '_'.join(path[:-1])))

    return result_markup


calculator_kb = types.InlineKeyboardMarkup()
i = 0
for iService, price in calculator_db.items():
    calculator_kb.add(types.InlineKeyboardButton(
        iService, callback_data="calculate_" + str(i)))
    i += 1
calculator_kb.add(types.InlineKeyboardButton('🚫 Отмена', callback_data='home'))


info_kb = types.InlineKeyboardMarkup()
i = 0
for iService, price in info_db.items():
    info_kb.add(types.InlineKeyboardButton(
        iService, callback_data="serviceinfo_" + str(i)))
    i += 1
info_kb.add(types.InlineKeyboardButton('🚫 Отмена', callback_data='home'))

cancel_markup = types.InlineKeyboardMarkup()
cancel_markup.add(types.InlineKeyboardButton('🚫 Отмена', callback_data="home"))

main_menu = get_kb()
# main_menu.add(types.InlineKeyboardButton('ℹ️ Инфо об уборке', callback_data="services_info"))
main_menu.add(types.InlineKeyboardButton('📱 Задать вопрос', callback_data="begin_question"),
              types.InlineKeyboardButton('⚖️ Расчет стоимости', callback_data="calculator"))

ordering_menu = types.InlineKeyboardMarkup()
ordering_menu.add(types.InlineKeyboardButton('▶️ Продолжить', callback_data="resume_order"),
                  types.InlineKeyboardButton('🛎 Оформить заказ', callback_data="enter_contacts"), )


labels = ['Дата и время уборки', 'Контакт для связи']


def process_user(usid):
    if not usid in db:
        db[usid] = {'order_in_process': False, 'order_items': []}


def place_next_question(usid):
    answer(usid, questions[db[usid]['order_step']], cancel_markup)
    db[usid]['order_step'] += 1


def parse_last_question(usid, str_message):
    # print(str_message)
    if 'answers' in db[usid]:
        db[usid]['answers'].append(str_message)
    else:
        db[usid]['answers'] = [str_message]

    if len(db[usid]['answers']) > db[usid]['order_step']:
        db[usid]['answers'] = db[usid]['answers'][:db[usid]['order_step']]
    elif len(db[usid]['answers']) < db[usid]['order_step']:
        db[usid]['order_step'] = len(db[usid]['answers'])

    if db[usid]['order_step'] >= len(questions):
        order_data = ""
        i = 0
        for item in db[usid]['order_items']:
            order_data += "	*📍 " + get_item_by_path(item) + "*\n"
        order_data += "\n"
        for ans in db[usid]['answers']:
            order_data += "_" + labels[i] + "_: `" + ans + "`\n"
            i += 1

        answer(usid, "*Ваш заказ принят!*\n\n" + order_data, main_menu)
        # answer(admin_chat, "*Новый заказ*\n\n" + order_data)
        db[usid]['answers'] = []
        del db[usid]['order_step']
        del db[usid]['order_items']
        db[usid]['order_in_process'] = False
        log_msg(bot.get_chat_member(usid, usid).user, "Завершил заказ")
    else:
        place_next_question(usid)


start_message = 'Привет. Я представляю клининг-сервис "*Ай! Чисто*". Что вы хотели?'


def answer(destination, msg, reply_markup=None, parse_mode="Markdown", reply_to_message_id=None):
    if isinstance(destination, telebot.types.CallbackQuery):
        try:
            return bot.edit_message_text(chat_id=destination.message.chat.id, message_id=destination.message.message_id, text=msg, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=True)
        except telebot.apihelper.ApiException as e:
            # print(e)
            bot.answer_callback_query(callback_query_id=destination.id)
    elif isinstance(destination, telebot.types.Message):
        return bot.send_message(chat_id=destination.chat.id, text=msg, reply_markup=reply_markup, parse_mode=parse_mode, reply_to_message_id=reply_to_message_id, disable_web_page_preview=True)
    elif isinstance(destination, int) or (isinstance(destination, str) and destination.startswith("@")):
        return bot.send_message(chat_id=destination, text=msg, reply_markup=reply_markup, parse_mode=parse_mode, reply_to_message_id=reply_to_message_id, disable_web_page_preview=True)


@bot.message_handler(commands=['start'])
def start(message):
    read_db()
    log_msg(message.from_user, "Начал диалог с ботом")
    process_user(message.from_user.id)
    try:
        db[message.from_user.id]['last_action'] = ''
        del db[message.from_user.id]['order_items']
        del db[message.from_user.id]['order_step']
    except:
        pass
    bot.send_message(message.chat.id, start_message,
                     reply_markup=main_menu, parse_mode="Markdown")
    save_db()


def get_order_list(raw):
    items = []
    for item in raw:
        items.append(get_item_by_path(item))
    msg = "`"
    i = 1
    for item in items:
        msg += "`  `🌀 " + str(i) + ". " + item[2:] + "\n"
        i += 1
    msg += "`"
    return msg


def edit_msg(order_items):
    edit_markup = types.InlineKeyboardMarkup()
    edit_list = []
    items = []
    for item in order_items:
        items.append(get_item_by_path(item))
    i = 1
    for item in items:
        edit_list.append(types.InlineKeyboardButton(
            "❌ " + str(i), callback_data="remove_" + str(i - 1)))
        i += 1

    for i in range(0, len(edit_list), 3):
        edit_markup.add(*edit_list[i:i+3])

    edit_markup.add(types.InlineKeyboardButton('👈 К заказу', callback_data='path_' + '_'.join(str(x)
                                                                                              for x in order_items[:-1])), types.InlineKeyboardButton('🚫 Отменить заказ', callback_data='home'))
    edit_markup.add(types.InlineKeyboardButton(
        "🛎 Оформить заказ 🛎", callback_data="enter_contacts"))

    return edit_markup


def get_order_path(usid):
    if db[usid]['last_action'] == "order_in_process":
        return "\n\n`			  `🛎 *Корзина* 🛎\n" + get_order_list(db[usid]['order_items'])

    return ""


@bot.message_handler(content_types=['text'])
def text(message):
    read_db()
    process_user(message.from_user.id)
    try:
        if db[message.from_user.id]['last_action'] == "enter_contacts":
            parse_last_question(message.from_user.id, message.text)
        elif db[message.from_user.id]['last_action'].startswith("calculate_"):
            log_msg(message.from_user, "Рассчитал стоимость")
            # try:
            service_id = int(db[message.from_user.id]
                             ['last_action'].split("_")[1])
            answer(message, "*Услуга *`{}`* за {} м² будет стоить {} ₽*".format(list(calculator_db.items())
                                                                                [service_id][0], message.text, int(message.text) * int(list(calculator_db.items())[service_id][1])), main_menu)
            db[message.from_user.id]['last_action'] = ""
        elif db[message.from_user.id]['last_action'] == "question":
            log_msg(message.from_user, "Задал вопрос")
            # answer(admin_chat, "*Новый вопрос от @" + message.from_user.username + "*: `" + message.text.replace("`", "\\`") + "`")
            answer(message, "*Ваш вопрос принят. Пожалуйста, не удаляйте и не изменяйте свой @username, если вам нужна обратная связь!*", main_menu)
            db[message.from_user.id]['last_action'] = ""
    except KeyError:
        pass
    save_db()


@bot.callback_query_handler(func=lambda call: True)
def call_handle(call):
    read_db()
    process_user(call.from_user.id)
    print(call.data)
    order_path = get_order_path(call.from_user.id)

    kb_path = call.data[5:] if call.data.startswith("path") else ''

    order_kb = get_kb(kb_path, call.from_user.id)
    if db[call.from_user.id]['last_action'] == "delete_photo":
        try:
            bot.delete_message(call.message.chat.id,
                               call.message.message_id - 1)
        except:
            pass

    if "delete_photo" in db[call.from_user.id] and db[call.from_user.id]['delete_photo'] == True:
        try:
            bot.delete_message(call.message.chat.id,
                               call.message.message_id - 1)
            db[call.from_user.id]['delete_photo'] = False
        except:
            pass

    if db[call.from_user.id]['last_action'] == "order_in_process":
        order_kb.add(types.InlineKeyboardButton('🚫 Отменить заказ', callback_data='home'),
                     types.InlineKeyboardButton("🛎 Оформить заказ 🛎", callback_data="enter_contacts"))
        order_kb.add(types.InlineKeyboardButton(
            '🖍 Редактировать заказ', callback_data='edit_order'))
    else:
        order_kb.add(types.InlineKeyboardButton(
            "🚪 Выход", callback_data="home"))

    if db[call.from_user.id]['last_action'].startswith("calculate"):
        answer(call, "*Введите размер квартиры в м²*", cancel_markup)
        db[call.from_user.id]['last_action'] = call.data

    if call.data == "begin_order":
        log_msg(call.from_user, "Начал заказ")
        answer(call, 'Нажмите на кнопку с префиксом ➕ для добавления к заказу.', order_kb)
    elif call.data == "begin_question":
        log_msg(call.from_user, "Начал задавать вопрос")
        if isinstance(call.from_user.username, str):
            answer(call, '*Отправьте ваш вопрос*.', cancel_markup)
            db[call.from_user.id]['last_action'] = 'question'
        else:
            answer(call, '*Я не могу принять ваш вопрос, так как у вас нет @username. Пожалуйста, свяжитесь с администратором по тел. +7 (939)-300-63-65*', main_menu)
    elif call.data.startswith("serviceinfo_"):
        service_id = int(call.data.split("_")[1])
        log_msg(call.from_user, "Запросил информацию об услуге " +
                list(info_db.items())[service_id][0])
        with open(script_path + "serviceinfo/" + list(info_db.items())[service_id][1] + ".jpg", 'rb') as f:
            bot.send_photo(call.from_user.id, photo=f)

        bot.delete_message(call.message.chat.id, call.message.message_id)
        db[call.from_user.id]['last_action'] = "delete_photo"
        answer(call.from_user.id, "*Информация об услуге *`" + list(info_db.items())
               [service_id][0] + "`*. Цена: *`" + formatted_prices[list(info_db.items())[service_id][1]] + "`", main_menu)
    elif call.data == "services_info":
        answer(call, "*Выберите услугу для показа информации*", info_kb)
    elif call.data == "calculator":
        answer(call, '*Выберите услугу для расчета стоимости.*', calculator_kb)
        db[call.from_user.id]['last_action'] = "calculate"
    elif call.data.startswith('path'):
        try:
            if call.data[5:] in additional_info:
                tmp_order_kb = order_kb
                tmp_order_kb.add(types.InlineKeyboardButton(
                    'Подробнее ↩️', callback_data='additional_' + call.data[5:]))
                answer(call, 'Нажмите на кнопку с префиксом ➕ для добавления к заказу.' +
                       order_path, tmp_order_kb)
            else:
                answer(
                    call, 'Нажмите на кнопку с префиксом ➕ для добавления к заказу.' + order_path, order_kb)
        except Exception as e:
            print(e)
            pass
    elif call.data.startswith('additional_'):
        path = call.data[11:]
        additional_info_kb = types.InlineKeyboardMarkup()
        additional_info_kb.add(types.InlineKeyboardButton('Добавить ➕', callback_data='order_' +
                                                          path + '_0'), types.InlineKeyboardButton('👈 Назад', callback_data='path_' + path))
        answer(call, additional_info[path], additional_info_kb)

    elif call.data.startswith('order'):
        if db[call.from_user.id]['last_action'] == "order_in_process" and call.data.split("_")[1:] in db[call.from_user.id]['order_items']:
            answer(call, "*Невозможно добавить позицию к заказу, так как она уже существует.*\n" +
                   get_order_list(db[call.from_user.id]['order_items']), ordering_menu)
            return

        if db[call.from_user.id]['last_action'] == "order_in_process":
            db[call.from_user.id]['order_items'].append(
                call.data.split("_")[1:])
        else:
            db[call.from_user.id]['order_items'] = [call.data.split("_")[1:]]
            db[call.from_user.id]['last_action'] = "order_in_process"

        answer(call, "*Добавлено к заказу.*\n" +
               get_order_list(db[call.from_user.id]['order_items']), ordering_menu)
    elif call.data == "home":
        try:
            db[call.from_user.id]['last_action'] = ''
            del db[call.from_user.id]['order_items']
            del db[call.from_user.id]['order_step']
        except:
            pass
        answer(call, start_message, main_menu)
    elif call.data == "resume_order":
        answer(call, 'Нажмите на кнопку с префиксом ➕ для добавления к заказу.' +
               order_path, order_kb)
    elif call.data == "enter_contacts":
        db[call.from_user.id]['last_action'] = 'enter_contacts'
        db[call.from_user.id]['order_step'] = 0
        answer(call, questions[db[call.from_user.id]
                               ['order_step']], cancel_markup)
        db[call.from_user.id]['order_step'] = 1

    elif call.data == "edit_order":
        answer(call, "*Редактирование заказа*\n_	Нажмите на кнопку с соответствующей позиции цифре, чтобы удалить ее._" +
               order_path, edit_msg(db[call.from_user.id]['order_items']))
    elif call.data.startswith("remove"):
        remove_i = int(call.data.split("_")[1])
        del db[call.from_user.id]['order_items'][remove_i]
        order_path = get_order_path(call.from_user.id)
        answer(call, "`✅ Позиция удалена.`\n\n*Редактирование заказа*\n_	Нажмите на кнопку с соответствующей позиции цифре, чтобы удалить ее._" +
               order_path, edit_msg(db[call.from_user.id]['order_items']))

    save_db()


bot.polling(none_stop=True, timeout=10)
