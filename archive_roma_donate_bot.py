"""
    Copyright 2021 t.me/innocoffee
    Licensed under the Apache License, Version 2.0
    
    Author is not responsible for any consequencies caused by using this
    software or any of its parts. If you have any questions or wishes, feel
    free to contact Dan by sending pm to @innocoffee_alt.

    This code is just for understanding the code-style of developer.
    Not for production or even development usage.
"""

import telebot
import json
import os
import time
import difflib
import re
import requests
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from random import randint

path = os.path.dirname(os.path.abspath(__file__)) + "/"

types = telebot.types
bot = telebot.TeleBot('<api-token>')

statuses = {
    'not_paid': "🚫 Не оплачен",
    'paid': "✅ Оплачен",
    'in_work': '⏱ В очереди',
    'done': '☑️ Завершен'
}


def create_swiftpay_payment(user_id, amount, order_id):
    token = "<api-token>"
    description = "Оплата услуг в <bot>"
    shop_id = "450"
    answer = json.loads(requests.post("https://api.swiftpay.ru/createOrder", data={
                        'amount': amount, 'description': description, 'order_id': order_id, 'token': token, 'data': '{"telegram_id": ' + str(user_id) + '}', 'shop_id': shop_id}).text)
    print(answer)
    return answer['data']['link']


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '/var/www/html/bot/sheets_service.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Название игры; описание; цена за еденицу валюты; еденица валюты (кратность покупки); процент за объем (кооф*сумма\еден.вал.)
# games = [['Call of Duty: Mobile', 'Старый, более дешевый метод. На ваш страх и риск!', 1500, 5000, 0.02, "🟠", "CP"], ['Call of Duty: Mobile', 'Новый метод с гарантией', 2500, 5000, 0, "🟠", "CP"]]
games = []
decode_game = {}


def read_games():
    result = sheet.values().get(spreadsheetId="<sheet-id>",
                                range="games!A2:Z1000").execute()
    values = result.get('values', [])
    for row in values:
        if len(row) < 10 or row[0] == '':
            break

        for i in range(3, 6):
            # print([re.sub(re.compile("[^0-9.]"), "", row[i])])
            row[i] = float(re.sub(re.compile("[^0-9.]"), "", row[i]))

        for i in range(8, 12):
            row[i] = True if row[i] == "TRUE" else False

        decode_game[row[0]] = row[1:]
        del row[0]

        games.append(row)


read_games()

# print(decode_game)

print("GAMES READ SUCCESS")
# print(games)

db = dict()

necessary_for_order = ['nickname', 'accdata']
order_steps = ['nickname', 'amount', 'accdata', 'comment']
changeble = ['nickname', 'accdata', 'comment']
labels = ['Никнейм', 'Данные для входа', 'Комментарий']


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def read_db():
    global db
    try:
        with open(path + "main_database.json", 'r') as f:
            temp = json.loads(f.read())
            db = dict()
            for key, value in temp.items():
                db[int(key)] = value

        ####### ВНИМАНИЕ! КОСТЫЛЬ! #########

        # for user, value in db.items():
        # 	if 'orders' in value:
        # 		for i in range(len(value['orders'])):
        # 			if type(value['orders'][i]['game']) == list:
        # 				value['orders'][i]['game'] = get_key(decode_game, value['orders'][i]['game'])
        # 				print(value['orders'][i]['game'])

        print("DATABASE READ SUCCESS")
    except Exception as e:
        db = dict()
        print("DATABASE READ ERROR")
        print(e)


read_db()


def export_to_gsheets__orders():
    export_data = [['Последнее изменение: ' +
                    datetime.datetime.now().strftime("%d.%m.%Y %H:%M")]]
    for user, value in db.items():
        if 'orders' in value:
            for order in value['orders']:
                user_TID = user
                order_id = order['id']
                game = decode_game[order['game']][0]
                method = decode_game[order['game']][1]
                nickname = order['nickname']
                amount = decode_game[order['game']][5] + " " + \
                    str(order['amount']) + " " + decode_game[order['game']][6]
                amount_rub = round(decode_game[order['game']][2] * (order['amount'] // decode_game[order['game']][3]) * (
                    1.0 - (order['amount'] // decode_game[order['game']][3] - 1) * decode_game[order['game']][4]))
                login_data = order['accdata']
                comment = order['comment']
                status = statuses[order['status']]

                export_data.append([user_TID, order_id, game, method, nickname,
                                    amount, amount_rub, login_data, comment, status])

    sheet.values().clear(spreadsheetId="<sheet-id>", range="orders!A2:Z1000").execute()
    result = sheet.values().update(spreadsheetId="<sheet-id>", range="orders!A2:Z1000",
                                   valueInputOption='USER_ENTERED', body={"values": export_data}).execute()


def export_to_gsheets__users():
    export_data = [['Последнее изменение: ' +
                    datetime.datetime.now().strftime("%d.%m.%Y %H:%M")]]
    for user, value in db.items():
        TID = user
        user_obj = bot.get_chat_member(user, user).user
        alias = (
            '@' + user_obj.username) if isinstance(user_obj.username, str) else '🚫'
        name = user_obj.first_name + \
            ((' ' + user_obj.last_name) if isinstance(user_obj.last_name, str) else '')
        autofill = ' \\ '.join(
            [x[1] for x in value['autofill_data'].items()]) if 'autofill_data' in value else '🚫'

        # GETTING ORDERS' RANGE

        result = sheet.values().get(spreadsheetId="<sheet-id>",
                                    range="orders!A2:Z1000").execute()
        values = result.get('values', [])

        orders_label = '🌐 ' + \
            str((len(value['orders']) if 'orders' in value else 0)) + ' шт. '

        if not 'orders' in value or len(value['orders']) == 0:
            orders = orders_label
        else:
            try:
                orders_range = 'A' + str([x[0] for x in values].index(str(user)) + 2) + ':J' + str(
                    len(values) + 1 - [x[0] for x in values][::-1].index(str(user)))
                orders = '=HYPERLINK("https://docs.google.com/spreadsheets/d/<sheet-id>/edit#gid=1255082837&range=' + \
                    orders_range + '"; "' + orders_label + '")'
            except:
                orders = orders_label

        current_action = value['last_action']
        export_data.append(
            [TID, alias, name, autofill, orders, current_action])

    sheet.values().clear(spreadsheetId="<sheet-id>", range="users!A2:Z1000").execute()
    result = sheet.values().update(spreadsheetId="<sheet-id>", range="users!A2:Z1000",
                                   valueInputOption='USER_ENTERED', body={"values": export_data}).execute()
    # print(result)


def export_to_gsheets():
    export_to_gsheets__orders()
    export_to_gsheets__users()

    # print(values)


def save_db():
    global db
    with open(path + "main_database.json", 'w') as f:
        f.write(json.dumps(db))


def answer(destination, msg, reply_markup=None, parse_mode="Markdown", reply_to_message_id=None):
    if isinstance(destination, telebot.types.CallbackQuery):
        try:
            return bot.edit_message_text(chat_id=destination.message.chat.id, message_id=destination.message.message_id, text=msg, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=True)
        except telebot.apihelper.ApiException as e:
            print(e)
            bot.answer_callback_query(callback_query_id=destination.id)
    elif isinstance(destination, telebot.types.Message):
        return bot.send_message(chat_id=destination.chat.id, text=msg, reply_markup=reply_markup, parse_mode=parse_mode, reply_to_message_id=reply_to_message_id, disable_web_page_preview=True)
    elif isinstance(destination, int) or (isinstance(destination, str) and destination.startswith("@")):
        return bot.send_message(chat_id=destination, text=msg, reply_markup=reply_markup, parse_mode=parse_mode, reply_to_message_id=reply_to_message_id, disable_web_page_preview=True)

    # print(destination, type(destination), msg)


delord = []
for user, value in db.items():
    if 'orders' in value:
        for i in range(len(value['orders'])):
            if type(value['orders'][i]['game']) == list:
                value['orders'][i]['game'] = get_key(
                    decode_game, value['orders'][i]['game'])
                print('changed', value['orders'][i]
                      ['game'], value['orders'][i]['id'])

            if value['orders'][i]['game'] == None:
                answer(user, "*Заказ #" + str(value['orders'][i]['id']) +
                       " удален.*\n\n`Ошибка чтения идентификатора игры.`")
                answer("<admin-chat>", "*Заказ #" + str(
                    value['orders'][i]['id']) + " удален.*\n\n`Ошибка чтения идентификатора игры.`")
                delord.append([user, i])

    if 'autofill_data' in value:
        if type(value['autofill_data']['game']) == list:
            value['autofill_data']['game'] = get_key(
                decode_game, value['autofill_data']['game'])
            print('changed autofill data', value['autofill_data']['game'])

        if value['autofill_data']['game'] == None:
            answer(user, "*Данные автозаполнения удалены (*`USER TID: " +
                   str(user) + "`*).*\n\n`Ошибка чтения идентификатора игры.`")
            answer("<admin-chat>", "*Данные автозаполнения удалены (*`USER TID: " +
                   str(user) + "`*).*\n\n`Ошибка чтения идентификатора игры.`")
            del value['autofill_data']
            del value['autofill']

    if 'order_progress' in value and 'game' in value['order_progress']:
        if type(value['order_progress']['game']) == list:
            value['order_progress']['game'] = get_key(
                decode_game, value['order_progress']['game'])
            print('changed order_progress ', value['order_progress']['game'])

        if value['order_progress']['game'] == None:
            # answer(user, "*Данные текущего заказа удалены (*`USER TID: " + str(user) + "`*).*\n\n`Ошибка чтения идентификатора игры.`")
            answer("<admin-chat>", "*Данные текущего заказа удалены (*`USER TID: " +
                   str(user) + "`*).*\n\n`Ошибка чтения идентификатора игры.`")
            del value['order_progress']['game']


for usid, ordid in delord:
    del db[usid]['orders'][ordid]


save_db()


main_markup = types.InlineKeyboardMarkup(row_width=2)
main_markup.add(types.InlineKeyboardButton('👻 О нас', callback_data="about"),
                types.InlineKeyboardButton('ℹ️ F.A.Q', callback_data="faq0"))
main_markup.add(types.InlineKeyboardButton('💷 Тарифы', callback_data="rates"),
                types.InlineKeyboardButton('🧳 Заказать', callback_data="order"))
main_markup.add(types.InlineKeyboardButton(
    '🦾 Мои заказы', callback_data="my_orders"))
main_markup.add(types.InlineKeyboardButton('⭐️ Отзывы', url="<fb-link>"),
                types.InlineKeyboardButton("👀 Пруфы", url="<proofs-link>"))

confirm_markup = types.InlineKeyboardMarkup()
confirm_markup.add(types.InlineKeyboardButton("🚫", callback_data="confirm_no"),
                   types.InlineKeyboardButton("✅", callback_data="confirm_yes"))
confirm_markup.add(types.InlineKeyboardButton(
    "🏠 На главную", callback_data="home"))

cancel_markup = types.InlineKeyboardMarkup()
cancel_markup.add(types.InlineKeyboardButton(
    "🚫 ОТМЕНА 🚫", callback_data="home"))


def download_faq_list():
    result = sheet.values().get(spreadsheetId="<sheet-id>",
                                range="faq!A2:Z1000").execute()
    values = result.get('values', [])
    return values


def prepare_faq_list():
    faq_list_filename = "faq_list.json"
    faq_list_filepath = path + faq_list_filename
    faq_list_update_timeout = (60 * 60 * 6)  # раз в 6 часов
    if not os.path.isfile(faq_list_filepath) or int(os.path.getmtime(faq_list_filepath)) <= int(time.time() - faq_list_update_timeout):
        with open(faq_list_filepath, 'w') as f:
            f.write(json.dumps(download_faq_list()))

    with open(faq_list_filepath, 'r') as f:
        return json.loads(f.read())


def check_autofill(user_id):
    if 'autofill' in db[user_id] and db[user_id]['autofill'] and 'autofill_data' in db[user_id]:
        for setting in necessary_for_order:
            if not setting in db[user_id]['autofill_data']:
                return False

        return True

    return False


def get_autofill(user_id):
    result = []
    for setting in necessary_for_order:
        result.append(db[user_id]['autofill_data'][setting])

    return result


def get_pages_keyboard(current_page, total_pages, query_word, start=0):
    keyboard = types.InlineKeyboardMarkup()
    if current_page == start:
        keyboard.row(types.InlineKeyboardButton("➡️ Вперед", callback_data=query_word + str(current_page + 1)),
                     types.InlineKeyboardButton("⏭ В конец", callback_data=query_word + str(total_pages - 1)))
    elif current_page == total_pages - 1:
        keyboard.row(types.InlineKeyboardButton("⏮ В начало", callback_data=query_word + str(start)),
                     types.InlineKeyboardButton("⬅	 Назад", callback_data=query_word + str(current_page - 1)))
    else:
        keyboard.row(types.InlineKeyboardButton("⏮", callback_data=query_word + str(start)), types.InlineKeyboardButton("⬅️", callback_data=query_word + str(current_page - 1)),
                     types.InlineKeyboardButton("➡️", callback_data=query_word + str(current_page + 1)), types.InlineKeyboardButton("⏭", callback_data=query_word + str(total_pages - 1)))

    keyboard.row(types.InlineKeyboardButton(
        "🏠 На главную", callback_data="home"))

    return keyboard


start_message = "*Привет! 👋* Я помогу тебе приобрести игровую валюту во многих играх с большими скидками. Если остались вопросы, напиши нашему администратору - <admin> ☺️"


choose_game_markup = types.InlineKeyboardMarkup()
choose_game_markup.add(types.InlineKeyboardButton(
    "Выбрать игру", switch_inline_query_current_chat=""))
choose_game_markup.add(types.InlineKeyboardButton(
    "🏠 На главную", callback_data="home"))


def choose_game(destination):
    text = "*🎮 Выбери игру, чтобы продолжить:*\n\n_Если в списке нет нужной тебе игры - напиши _[администратору](<admin>)"
    answer(destination, text, choose_game_markup)


def proceed_user(usid):
    read_db()
    if not usid in db:
        db[usid] = dict()
        print("USER ADDED")
        save_db()

    if not 'last_action' in db[usid]:
        db[usid]['last_action'] = ""
        print("USER LAST ACTION CHANGED")
        save_db()


@bot.message_handler(commands=['start'])
def message(message):
    if message.chat.id < 0:
        return
    proceed_user(message.from_user.id)

    db[message.from_user.id]['last_action'] = ""

    answer(message, start_message, main_markup)

    save_db()


def set_order_status(order_id, status, silent=False):

    status_markup = types.InlineKeyboardMarkup()
    order_buttons = {
        'in_work': types.InlineKeyboardButton("☑️ Завершить заказ", callback_data="done_" + str(order_id)),
        'done': types.InlineKeyboardButton("🔻 Закончить отправку подтверждений", callback_data="order_confirm"),
        'paid': types.InlineKeyboardButton("✅ Приступить", callback_data="inwork_" + str(order_id)),
        'not_paid': types.InlineKeyboardButton("⏱ Ожидание оплаты", callback_data="waiting_pay")
    }

    status_markup.add(order_buttons[status])
    # print(order_id, db)
    for user, value in db.items():
        if 'orders' in value:
            for i in range(len(value['orders'])):
                if value['orders'][i]['id'] == order_id:
                    print(value['orders'][i])
                    value['orders'][i]['status'] = status

                    order_data = value['orders'][i]
                    print(order_data)
                    decoded_game = decode_game[order_data['game']]
                    text = "*👾 Заказ #{id} 👾*\n\nTID: {tid}\nНик в игре: *{nickname}*\nДанные для входа: `{accdata}`\nКол-во валюты: `{amount}`\nКомментарий: `{comment}`\nИгра: `{game}`\nМетод: `{method}`\nСтатус: `{status}`".format(
                        tid=user, status=statuses[order_data['status']], nickname=order_data['nickname'], accdata=order_data['accdata'], amount=order_data['amount'], comment=order_data['comment'], game=decoded_game[0], method=decoded_game[1], id=order_data['id'])

                    def send():
                        message_obj = bot.send_message(
                            "<admin-chat>", text, disable_web_page_preview=True, parse_mode="Markdown", reply_markup=status_markup)
                        value['orders'][i]['admin_message_id'] = message_obj.message_id

                    try:
                        if not 'admin_message_id' in order_data:
                            send()
                            save_db()
                            update_pinned_orders()

                            return
                        bot.edit_message_text(
                            chat_id="<admin-chat>", message_id=order_data['admin_message_id'], text=text, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=status_markup)
                    except Exception as e:
                        if not 'message is not modified' in str(e):
                            send()
                        else:
                            pass

                    save_db()

                    if not silent:
                        answer("<admin-chat>", "Статус заказа `#{id}` обновлен на \"{status}\"".format(
                            id=order_id, status=statuses[status]), status_markup, reply_to_message_id=value['orders'][i]['admin_message_id'])
                        answer(user, "Статус заказа `#{id}` обновлен на \"{status}\"".format(
                            id=order_id, status=statuses[status]))
                    update_pinned_orders()
                    return

# set_order_status(627018, 'not_paid', None)
# print(db)


def place_order_question(from_user, step):
    db[from_user.id]['order_step'] = step
    db[from_user.id]['last_action'] = "parse_order"
    print(order_steps[db[from_user.id]['order_step']])
    if order_steps[db[from_user.id]['order_step']] in list(db[from_user.id]['order_progress'].keys()):
        place_order_question(from_user, step + 1)
        return

    game = decode_game[db[from_user.id]['order_progress']['game']]
    questions = ['`Пользователь несет ответственность за правильность ввода данных!`\n\nВведи свой ник в игре {game}.'.format(
        game=game[0]), 'Введи количество валюты, которое ты хочешь приобрести. \nМинимум: {emoji} {odd} {exchange_name}\nДолжно быть кратно: {emoji} {odd} {exchange_name}\n\n*Введите ТОЛЬКО число. Например: *`1000`*. Иначе бот не сможет обработать ваш заказ!*'.format(odd=game[3], emoji=game[5], exchange_name=game[6]), "заглушка", "Напиши комментарий к заказу. Если нечего сказать - просто отправь '.'"]

    if step == len(order_steps) - 2:
        question = "*Введите данные для входа (одно из списка):*\n\n"
        accs = {
            7: '   👉 *Игровой вход*: _логин и пароль от игрового аккаунта_',
            8: '   👉 *Facebook*: _логин, пароль и коды_ ([что?](https://www.facebook.com/help/148104135383285?helpref=faq_content)) _для входа в аккаунт_',
            9: '   👉 *Google*: _логин, пароль и коды_ ([что?](https://support.google.com/accounts/answer/1187538?co=GENIE.Platform=Desktop&hl=ru)) _для входа в аккаунт_',
            10: '   👉 *VK*: _логин, пароль для входа в аккаунт_'

        }
        for i in range(7, 11):
            if decode_game[db[from_user.id]['order_progress']['game']][i]:
                question += accs[i] + "\n"

        question += "\n*Пример:*\n_Facebook. Логин: vasyapupkin, Пароль: vasyapupkin123, Коды для входа: 12345678, 87654321_\n\n_А также введите название сервера с новой строки, если необходимо._"

    else:
        question = questions[step]
    answer(from_user.id, question, cancel_markup)


def parse_order_info(message):
    if not 'order_progress' in db[message.from_user.id]:
        db[message.from_user.id]['last_action'] = ""
        answer(message, start_message, main_markup)
        return

    db[message.from_user.id]['order_progress'][order_steps[db[message.from_user.id]
                                                           ['order_step']]] = message.text

    if db[message.from_user.id]['order_step'] < len(order_steps) - 1:
        place_order_question(
            message.from_user, db[message.from_user.id]['order_step'] + 1)
    else:
        # print('before', db[message.from_user.id]['order_progress'])
        game = decode_game[db[message.from_user.id]['order_progress']['game']]
        # print('after', db[message.from_user.id]['order_progress'])

        db[message.from_user.id]['order_progress']['amount'] = int(re.sub(re.compile(
            "[^0-9]"), "", str(db[message.from_user.id]['order_progress']['amount'])))
        if db[message.from_user.id]['order_progress']['amount'] < game[3]:
            db[message.from_user.id]['order_progress']['amount'] = game[3]

        if db[message.from_user.id]['order_progress']['amount'] % game[3] != 0:
            if db[message.from_user.id]['order_progress']['amount'] % game[3] <= game[3] // 2:
                db[message.from_user.id]['order_progress']['amount'] = db[message.from_user.id]['order_progress']['amount'] - \
                    db[message.from_user.id]['order_progress']['amount'] % game[3]
            else:
                db[message.from_user.id]['order_progress']['amount'] = db[message.from_user.id]['order_progress']['amount'] % game[3] + game[3]

        order_data = db[message.from_user.id]['order_progress']
        payment_amount = round(game[2] * (order_data['amount'] // game[3])
                               * (1.0 - (order_data['amount'] // game[3] - 1) * game[4]))
        # payment_amount = 10

        try:
            with open(path + "orders_counter.json", 'r') as f:
                orders_count = int(f.read())
        except:
            orders_count = 0

        orders_count += 1

        with open(path + "orders_counter.json", 'w') as f:
            f.write(str(orders_count))

        if orders_count < 10:
            orders_count = '000' + str(orders_count)
        elif orders_count < 100:
            orders_count = '00' + str(orders_count)
        elif orders_count < 1000:
            orders_count = '0' + str(orders_count)
        else:
            orders_count = str(orders_count)

        db[message.from_user.id]['order_progress']['id'] = orders_count + \
            "_" + str(randint(1000, 9999))
        db[message.from_user.id]['order_progress']['status'] = "not_paid"
        db[message.from_user.id]['order_progress']['paylink'] = create_swiftpay_payment(
            message.from_user.id, payment_amount, int(re.sub(re.compile("[^0-9]"), "", order_data['id'])))
        order_data = db[message.from_user.id]['order_progress']

        # message_obj = bot.send_message("<admin-chat>", "*👾 Заказ #{id} 👾*\n\nНик в игре: *{nickname}*\nДанные для входа: `{accdata}`\nКол-во валюты: `{amount}`\nКомментарий: `{comment}`\nИгра: `{game}`\nМетод: `{method}`\nСтатус: `Не оплачено`".format(nickname=order_data['nickname'], accdata=order_data['accdata'], amount=order_data['amount'], comment=order_data['comment'], game=order_data['game'][0], method=order_data['game'][1], id=order_data['id']), disable_web_page_preview=True, parse_mode="Markdown", reply_markup=not_paid_markup)
        if not 'orders' in db[message.from_user.id]:
            db[message.from_user.id]['orders'] = []

        # db[message.from_user.id]['order_progress']['admin_message_id'] = message_obj.message_id

        db[message.from_user.id]['orders'].append(
            db[message.from_user.id]['order_progress'])
        # print('before', db[message.from_user.id]['order_progress'])
        set_order_status(order_data['id'], "not_paid")
        update_pinned_orders()
        # print('after', db[message.from_user.id]['order_progress'])

        # print(db)
        answer(message, "*👾 Ваш заказ #{id} 👾*\n\nНик в игре: *{nickname}*\nДанные для входа: `{accdata}`\nКол-во валюты: `{amount}`\nКомментарий: `{comment}`\nИгра: `{game}`\nМетод: `{method}`\nСтатус: `Не оплачено`\n\nУбедитесь, что все данные верны, а затем перейдите по [ссылке]({link}) для оплаты.\n_Если ссылка не работает, скопируй ее: _`{link}`_ и вставь в браузере._".format(
            nickname=order_data['nickname'], accdata=order_data['accdata'], amount=order_data['amount'], comment=order_data['comment'], game=game[0], method=game[1], id=order_data['id'], link=order_data['paylink']))
        if not 'autofill' in db[message.from_user.id] or not db[message.from_user.id]['autofill']:
            answer(
                message, "Сохранить данные (игра, ник, данные для входа) для последующих покупок?", confirm_markup)
            db[message.from_user.id]['last_action'] = "save_autofill_confirm"
        else:
            del db[message.from_user.id]['order_progress']

        del db[message.from_user.id]['order_step']

        # print(db[message.from_user.id]['orders'][-1])

    save_db()


def autoreply_changetext(message):
    autoreply_data = autoreply_read()

    autoreply_data['text'] = message.text
    autoreply_save(autoreply_data)
    autoreply_markup, autoreply_text = get_autoreply_markup()
    answer(message, "*Настройки автоответчика*\n\n_Текст автоответчика: _`" +
           autoreply_text + "`", autoreply_markup)


def autoreply_read():
    try:
        with open(path + "autoreply.json", 'r') as f:
            autoreply_data = json.loads(f.read())
    except:
        autoreply_data = {}

    return autoreply_data


def autoreply_save(autoreply_data):
    with open(path + "autoreply.json", 'w') as f:
        f.write(json.dumps(autoreply_data))


def update_pinned_orders():
    result = "🔺🔸 Текущие заказы 🔸🔺\n"
    orders = []

    for user, value in db.items():
        if 'orders' in value:
            for order in value['orders']:
                if order['status'] in ['paid', 'not_paid', 'in_work']:
                    orders.append(order)

    orders.sort(key=lambda x: x['status'])

    for order in orders:
        amount = round(decode_game[order['game']][2] * (order['amount'] // decode_game[order['game']][3]) * (
            1.0 - (order['amount'] // decode_game[order['game']][3] - 1) * decode_game[order['game']][4]))
        result += "\n   🔹 [#" + order['id'] + "](https://t.me/<admin-chat>/" + str(order['admin_message_id']) + ") | *" + decode_game[order['game']][0] + "* | *" + \
            decode_game[order['game']][5] + " " + str(order['amount']) + " " + decode_game[order['game']][6] + "* | *" + str(
                amount) + " RUB* | *" + statuses[order['status']] + "*"

    def send_new(msid):
        try:
            bot.delete_message("<admin-chat>", msid)
        except:
            pass

        new_sended = answer("<admin-chat>", result)
        pinned_message = bot.pin_chat_message(
            new_sended.chat.id, new_sended.message_id, disable_notification=True)
        try:
            bot.delete_message("<admin-chat>", pinned_message.message_id)
        except:
            pass
        with open(path + "pinned_message_id.json", "w") as f:
            f.write(str(new_sended.message_id))

    if os.path.isfile(path + "pinned_message_id.json"):
        with open(path + "pinned_message_id.json", "r") as f:
            try:
                pinned_message_id = int(f.read())

                try:
                    bot.edit_message_text(chat_id="<admin-chat>", message_id=pinned_message_id,
                                          text=result, parse_mode="Markdown", disable_web_page_preview=True)
                except Exception as e:
                    if not 'message is not modified' in str(e):
                        send_new(pinned_message_id)
                        print(e)
            except:
                send_new(0)
                pinned_message_id = 0


update_pinned_orders()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    read_db()
    proceed_user(call.from_user.id)
    # print(call.data)

    if call.data.startswith("autoreply"):
        if call.from_user.id in admins:
            action = call.data.split("_")[1]
            autoreply_data = autoreply_read()

            if action == "on":
                autoreply_data['on'] = True
                autoreply_save(autoreply_data)
                autoreply_markup, autoreply_text = get_autoreply_markup()
                answer(call, "*Настройки автоответчика*\n\n_Текст автоответчика: _`" +
                       autoreply_text + "`", autoreply_markup)

            elif action == "off":
                autoreply_data['on'] = False
                autoreply_save(autoreply_data)
                autoreply_markup, autoreply_text = get_autoreply_markup()
                answer(call, "*Настройки автоответчика*\n\n_Текст автоответчика: _`" +
                       autoreply_text + "`", autoreply_markup)

            elif action == "changetext":
                msg = answer(call, "Напиши текст для автоответчика: ")
                bot.register_next_step_handler(msg, autoreply_changetext)

        else:
            bot.answer_callback_query(
                callback_query_id=call.id, text="Тебе не разрешено это действие", show_alert=True)

    if call.data == 'about':
        answer(call, "*С 2015 года мы занимаемся продажей игровой валютой*, и уже заслужили авторитет перед игроками. *Низкие цены, быстрый результат*, грамотная техническая поддержка и огромный ассортимент игр делают нас просто незаменимыми. `Все риски указаны в описании метода. Если вы видите ⭐️ в его начале - мы гарантируем отсутствие бана`.", main_markup)
    elif call.data == 'home':
        db[call.from_user.id]['last_action'] = ""
        answer(call, start_message, main_markup)
    elif call.data == 'rates':
        db[call.from_user.id]['last_action'] = 'rates'
        choose_game(call)
    elif call.data == 'order':
        db[call.from_user.id]['last_action'] = 'order'
        if check_autofill(call.from_user.id):
            answer(
                call, "*🎦 Автозаполнить сохраненные данные заказа (игра, ник, данные авторизации)?*", confirm_markup)
            db[call.from_user.id]['last_action'] = 'confirm_order_autofill'
        else:
            choose_game(call)
    elif call.data == 'my_orders':
        orders_markup = types.InlineKeyboardMarkup(row_width=5)
        buttons = []
        if 'orders' in db[call.from_user.id] and len(db[call.from_user.id]['orders']) > 0:

            result = "🤛🏻 *Мои заказы* 🤜🏻\n\n"
            i = 1
            for order in db[call.from_user.id]['orders']:
                decoded_game = decode_game[order['game']]
                buttons.append(types.InlineKeyboardButton(
                    "🖋 " + str(i), callback_data="select_order_" + str(order['id'])))
                result += "📍 {i}. `#{id}` | *{game}* | *{emoji} {amount} {exchange_name} | {amount_rub} RUB* | {status}\n".format(id=order['id'], i=i, game=decoded_game[0], amount=order['amount'], amount_rub=round(
                    decoded_game[2] * (order['amount'] // decoded_game[3]) * (1.0 - (order['amount'] // decoded_game[3] - 1) * decoded_game[4])), status=statuses[order['status']], emoji=decoded_game[5], exchange_name=decoded_game[6])
                i += 1
        else:
            result = "🤛🏻 *У вас еще нет заказов* 🤜🏻"

        # print(buttons)

        for i in range(0, len(buttons), 5):
            orders_markup.row(*buttons[i:i+5])

        orders_markup.row(types.InlineKeyboardButton(
            "🏠 На главную", callback_data="home"))

        answer(call, result, orders_markup)

    elif call.data == 'waiting_pay':
        bot.answer_callback_query(
            callback_query_id=call.id, text="Ожидание оплаты от пользователя.", show_alert=True)
    elif call.data == "order_confirm":
        db[call.from_user.id]['last_action'] = ""
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "confirm_no":
        if db[call.from_user.id]['last_action'] == "save_autofill_confirm":
            answer(call, start_message, main_markup)
            del db[call.from_user.id]['order_progress']
        elif db[call.from_user.id]['last_action'] == "confirm_order_autofill":
            db[call.from_user.id]['autofill'] = False
            del db[call.from_user.id]['autofill_data']
            choose_game(call)
    elif call.data == "confirm_yes":
        if db[call.from_user.id]['last_action'] == "save_autofill_confirm":
            db[call.from_user.id]['last_action'] = ""
            db[call.from_user.id]['autofill'] = True
            db[call.from_user.id]['autofill_data'] = {'game': decode_game[db[call.from_user.id]['order_progress']['game']],
                                                      'nickname': db[call.from_user.id]['order_progress']['nickname'], 'accdata': db[call.from_user.id]['order_progress']['accdata']}
            answer(
                call, "*💾 Данные успешно сохранены для последующих заказов.*", main_markup)
            del db[call.from_user.id]['order_progress']
        elif db[call.from_user.id]['last_action'] == "confirm_order_autofill":
            db[call.from_user.id]['order_progress'] = {'game': db[call.from_user.id]['autofill_data']['game'],
                                                       'nickname': db[call.from_user.id]['autofill_data']['nickname'], 'accdata': db[call.from_user.id]['autofill_data']['accdata']}
            bot.delete_message(call.message.chat.id, call.message.message_id)
            place_order_question(call.from_user, 0)

    elif call.data.startswith("edit_"):
        order_id = '_'.join(call.data.split("_")[1:])
        buttons = []
        i = 0
        for setting in changeble:
            buttons.append(types.InlineKeyboardButton(
                labels[i], callback_data="sett_" + setting + "_" + str(order_id)))
            i += 1

        edit_markup = types.InlineKeyboardMarkup()

        for i in range(0, len(buttons), 3):
            edit_markup.row(*buttons[i:i+3])

        edit_markup.row(types.InlineKeyboardButton(
            "🏠 На главную", callback_data="home"))

        answer(call, "*Что ты хочешь изменить?*", edit_markup)

    elif call.data.startswith("sett_"):
        order_id = '_'.join(call.data.split("_")[2:])
        setting = call.data.split("_")[1]
        print([order_id, setting])

        db[call.from_user.id]['last_action'] = call.data

        answer(call, "Введи данные для поля " + labels[changeble.index(
            setting)] + ", заказа #" + str(order_id).replace("_", "\\_"), cancel_markup)

    elif call.data.startswith("delete_"):
        order_id = '_'.join(call.data.split("_")[1:])
        for user, value in db.items():
            if 'orders' in value:
                for j in range(len(db[user]['orders'])):
                    if db[user]['orders'][j]['id'] == order_id:
                        try:
                            bot.delete_message(
                                "<admin-chat>", value['orders'][j]['admin_message_id'])
                        except:
                            pass
                        del db[user]['orders'][j]
                        save_db()
                        delete_markup = types.InlineKeyboardMarkup()
                        delete_markup.row(types.InlineKeyboardButton(
                            "👈 К заказам", callback_data="my_orders"), types.InlineKeyboardButton("🚪 Выход", callback_data="home"))

                        answer(call, "*Заказ #" + str(order_id) +
                               " удален.*", delete_markup)
                        answer("<admin-chat>", "*Заказ #" +
                               str(order_id) + " удален.*")

                        return

    elif call.data.startswith("select_order_"):
        order_id = '_'.join(call.data.split("_")[2:])
        actions_markup = types.InlineKeyboardMarkup()

        for user, value in db.items():
            if 'orders' in value:
                for order in value['orders']:
                    if order['id'] == order_id:
                        statuses_actions = {
                            'not_paid': [types.InlineKeyboardButton("🖋 Редактировать", callback_data="edit_" + str(order_id)), types.InlineKeyboardButton("💴 Оплатить", url=order['paylink']), types.InlineKeyboardButton("🚫 Удалить", callback_data="delete_" + str(order_id))],
                            'paid': [types.InlineKeyboardButton("🖋 Редактировать", callback_data="edit_" + str(order_id)), types.InlineKeyboardButton("💂🏻‍♀️ Написать админу", url="<admin>")],
                            'in_work': [types.InlineKeyboardButton("💂🏻‍♀️ Написать админу", url="<admin>")],
                            'done': [types.InlineKeyboardButton("⭐️ Оставить отзыв", url="<fb-link>"), types.InlineKeyboardButton("🚫 Удалить", callback_data="delete_" + str(order_id))]
                        }

                        for i in range(0, len(statuses_actions[order['status']]), 2):
                            actions_markup.row(
                                *statuses_actions[order['status']][i:i+2])

                        actions_markup.row(types.InlineKeyboardButton(
                            "👈 К заказам", callback_data="my_orders"), types.InlineKeyboardButton("🚪 Выход", callback_data="home"))

        answer(
            call, "*Выбери действие для заказа #{id}*".format(id=order_id), actions_markup)
    elif call.data.startswith("done_"):
        # print(call.data)
        order_id = '_'.join(call.data.split("_")[1:])
        for user, value in db.items():
            if 'orders' in value:
                for i in range(len(value['orders'])):
                    if value['orders'][i]['id'] == order_id:
                        bot.answer_callback_query(
                            callback_query_id=call.id, text="Заказ завершен. Все фото и текст, отправленные в чат, будут отправлены покупателю!", show_alert=True)
                        db[call.from_user.id]['last_action'] = "send_" + \
                            str(user)
                        set_order_status(order_id, "done")

    elif call.data.startswith("inwork"):
        order_id = '_'.join(call.data.split("_")[1:])
        for user, value in db.items():
            if 'orders' in value:
                for i in range(len(value['orders'])):
                    if value['orders'][i]['id'] == order_id:
                        set_order_status(order_id, 'in_work')

    elif call.data.startswith('faq'):
        faq_list = prepare_faq_list()
        answers_per_page = 5

        current_page = int(call.data[3:])
        total_pages = len(faq_list) // 5 + (1 if len(faq_list) % 5 > 0 else 0)

        result = "*ℹ️ F.A.Q стр. {current_page} \\ {total_pages} ℹ️*\n\n".format(
            current_page=current_page + 1, total_pages=total_pages)

        for faq_item in faq_list[current_page * answers_per_page:(current_page + 1) * answers_per_page]:
            result += "❓ _" + \
                faq_item[0].replace("_", "\\_") + " _\n🗣 `" + \
                faq_item[1].replace("`", "\\`") + "`\n\n"

        answer(call, result, get_pages_keyboard(
            current_page, total_pages, "faq"))

    save_db()


@bot.message_handler(content_types=["photo"])
def verifyUser(message):
    if db[message.from_user.id]['last_action'].startswith("send_"):
        user_id = db[message.from_user.id]['last_action'].split("_")[1]
        bot.send_photo(user_id, photo=bot.download_file(bot.get_file(message.photo[0].file_id).file_path), caption=(
            message.caption if isinstance(message.caption, str) and message.caption != "" else "Подтверждение заказа"))


def get_autoreply_markup():
    autoreply_markup = types.InlineKeyboardMarkup()
    autoreply_data = autoreply_read()

    if not 'on' in autoreply_data or not autoreply_data['on']:
        autoreply_markup.add(types.InlineKeyboardButton(
            "🚫 Отключен", callback_data="autoreply_on"))
    else:
        autoreply_markup.add(types.InlineKeyboardButton(
            "✅ Включен", callback_data="autoreply_off"))

    autoreply_markup.add(types.InlineKeyboardButton(
        "📍 Изменить текст", callback_data="autoreply_changetext"))

    if not 'text' in autoreply_data:
        autoreply_data['text'] = "Автоответчик говорит: я не в сети!"
        autoreply_save(autoreply_data)

    return autoreply_markup, autoreply_data['text']


admins = [444638147, 943216990]


@bot.message_handler(content_types=['text'])
def plain_message(message):
    proceed_user(message.from_user.id)
    if db[message.from_user.id]['last_action'].startswith("send_"):
        user_id = db[message.from_user.id]['last_action'].split("_")[1]
        bot.send_message(user_id, message.text, disable_web_page_preview=True)
        return

    # print(db[message.from_user.id])

    if db[message.from_user.id]['last_action'] == "autoreply_code" and message.from_user.id in admins:
        try:
            int(message.text)

            with open(path + "code.json", 'w') as f:
                f.write(message.text)

            answer(message, "Код принят. Передаю автоответчику.")
            db[message.from_user.id]['last_action'] = ""
        except:
            answer(message, "Что-то не так! Мне нужен только код!")

    if message.from_user.id in admins and message.text.startswith(">"):
        if message.text.startswith(">send"):
            usid = int(message.text.split()[1])
            message = ' '.join(message.text.split()[2:])
            answer(usid, message, parse_mode="HTML")
            answer(message, "Отправлено")
        elif message.text == ">restart":
            os.popen("service innobot start")
            answer(message, "Перезагружаюсь")
            os.exit("Exited by chat")
        elif message.text == ">update_games":
            read_games()
            answer(message, "Обновлено")
        elif message.text == ">autoreply":
            autoreply_markup, autoreply_text = get_autoreply_markup()
            answer(message, "*Настройки автоответчика*\n\n_Текст автоответчика: _`" +
                   autoreply_text + "`", autoreply_markup)
        elif message.text.startswith(">set_ord_stat"):
            status = message.text.split(" ")[1]
            order_id = message.text.split(" ")[2]
            set_order_status(order_id, status)
        elif message.text == ">update_gsheets":
            export_to_gsheets()
            answer(message, "Успешно обновлено")
        elif message.text.startswith(">del_ord"):
            order_id = message.text.split(" ")[1]
            for user, value in db.items():
                if 'orders' in value:
                    for j in range(len(db[user]['orders'])):
                        if db[user]['orders'][j]['id'] == order_id:
                            try:
                                bot.delete_message(
                                    "<admin-chat>", value['orders'][j]['admin_message_id'])
                            except:
                                pass
                            del db[user]['orders'][j]
                            save_db()
                            delete_markup = types.InlineKeyboardMarkup()
                            delete_markup.row(types.InlineKeyboardButton(
                                "👈 К заказам", callback_data="my_orders"), types.InlineKeyboardButton("🚪 Выход", callback_data="home"))

                            answer(user, "*Заказ #" + str(order_id) +
                                   " удален администраторами.*", delete_markup)
                            answer("<admin-chat>", "*Заказ #" +
                                   str(order_id) + " удален администраторами.*")

                            return

    if message.chat.id < 0:
        return

    if db[message.from_user.id]['last_action'] == 'parse_order':
        parse_order_info(message)
        return

    if db[message.from_user.id]['last_action'].startswith("sett_"):
        setting = db[message.from_user.id]['last_action'].split("_")[1]
        order_id = '_'.join(db[message.from_user.id]
                            ['last_action'].split("_")[2:])

        for user, value in db.items():
            if 'orders' in value:
                for i in range(len(value['orders'])):
                    if value['orders'][i]['id'] == order_id:
                        db[user]['orders'][i][setting] = message.text
                        set_order_status(
                            order_id, value['orders'][i]['status'], silent=True)

        sett_markup = types.InlineKeyboardMarkup()
        sett_markup.row(types.InlineKeyboardButton("👈 К заказу", callback_data="select_order_" +
                                                   str(order_id)), types.InlineKeyboardButton("🚪 Выход", callback_data="home"))

        answer(message, "*Параметр *`" + labels[changeble.index(setting)] + "`* заказа *`#" + str(
            order_id) + "`* изменен на *`" + message.text + "`", sett_markup)
        answer("<admin-chat>", "*Параметр *`" + labels[changeble.index(
            setting)] + "`* заказа *`#" + str(order_id) + "`* изменен на *`" + message.text + "`")

    def valid_game(game):
        # print(game)
        if db[message.from_user.id]['last_action'] == "rates":
            db[message.from_user.id]['last_action'] = ""
            promo = ""
            game = decode_game[game]
            if game[4] > 0:
                promo = "\n\n*🤑 Акция 🤑*\n\n"
                for i in range(0, 4):
                    promo += "  *{emoji} {odd} {exchange_name} - 💷 {price} RUB*\n".format(price=round((game[2] * (
                        i + 1)) * (1 - game[4] * i)), odd=game[3] * (i + 1), emoji=game[5], exchange_name=game[6])
            answer(message, "Игра: 🎮 *{game_title}*\nМетод: 🎳 *{method}*\nМин.заказ: {emoji} *{odd}*\nЗаказ должен быть кратен {emoji} *{odd} {exchange_name}*\nЦена за {emoji} {odd} {exchange_name}: 💷 *{price} RUB*{promo}".format(
                game_title=game[0], method=game[1], price=game[2], odd=game[3], promo=promo, emoji=game[5], exchange_name=game[6]), main_markup)
            # bot.delete_message(message.chat.id, message.message_id)
        else:
            db[message.from_user.id]['order_progress'] = {'game': game}
            place_order_question(message.from_user, 0)

    if db[message.from_user.id]['last_action'] in ['rates', 'order']:
        valid_game_bool = False
        for game in decode_game.keys():
            if game == message.text:
                valid_game(game)
                valid_game_bool = True
        if not valid_game_bool:
            answer(
                message, "*Введите правильное название игры, или отмените операцию!*", choose_game_markup)

    save_db()


@bot.inline_handler(func=lambda query: True)
def query_text(inline_query):
    bot.answer_inline_query(inline_query.id, search_inline_query_results(
        inline_query.query, inline_query.from_user.id), cache_time=1)


def search_inline_query_results(quer, chat_id):
    global games
    result = []
    local_games = []
    for gmid, gmdata in decode_game.items():
        local_games.append(gmdata[0] + "$separator$" + gmdata[1] +
                           "$separator$" + gmdata[11] + "$separator$" + gmid)
    results = difflib.get_close_matches(quer, local_games, 30, cutoff=0)
    # print(results)

    result.append(
        types.InlineQueryResultArticle(
            id=time.time(),
            title="❌ Отмена",
            input_message_content=types.InputTextMessageContent(
                '/start',
                disable_web_page_preview=True
            ),
            description='Отменить последнее действие',
            thumb_height=1
        )
    )

    for game in results:
        game = game.split("$separator$")
        result.append(
            types.InlineQueryResultArticle(
                id=time.time(),
                title=game[0],
                input_message_content=types.InputTextMessageContent(
                    '`' + game[3] + '`',
                    disable_web_page_preview=True,
                    parse_mode="Markdown"
                ),
                thumb_url=game[2],
                description=(game[1] if len(game) >= 2 else ''),
                thumb_height=1
            )
        )
    return result


bot.polling(none_stop=True, timeout=10)
