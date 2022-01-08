import requests
import random
import re
import sys
import threading
import time
import datetime
from flask import Flask, render_template, request, make_response, redirect, jsonify
import traceback
import sqlite3
from flask_sqlite_admin.core import sqliteAdminBlueprint
from functools import wraps
import json
import os
import telebot
import logging
from flask.logging import default_handler
from flask_recaptcha import ReCaptcha
from captcha.image import ImageCaptcha
import speech_recognition as sr
from pydub import AudioSegment
from nudenet import NudeDetector
import math
import subprocess




try:
    detector = NudeDetector(os.getenv("MODEL_NAME", "default"))

    def get_video_length(filename):
        output = subprocess.check_output(("ffprobe", "-v", "error", "-show_entries",
                                          "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename)).strip()
        video_length = int(float(output))
        return video_length

    def ceildiv(a, b):
        return int(math.ceil(a / float(b)))

    start_menu_message = "*😇 Привет, братик!*\nЯ помогу следить за твоим чатом.\n\n    - Удалю маты\n    - Поприветствую новых участников\n    - Защищу от рейдов, спамеров и арабов\n    - Добавлю много полезных команд\nДля защиты нужно приобрести подписку. Ты можешь получить демо-версию, нажав на кнопку ниже:"
    available_settings = ['censor', 'raid', 'captcha',
                          'spam', 'welcome', 'nsfw', 'voices']
    my_username = "<bot-username>"

    def truncate(msg, start, end):
        return msg[msg.find(start) + len(list(start)):msg.find(end, msg.find(start) + len(list(start)) + 1)]

    def randhash(length):
        pool = 'abcdefghijklmnopqrstuvwxyz1234567890'
        return ''.join(random.choice(pool) for i in range(length))

    def handle_err(trace):
        trace = str(trace)
        if 'During handling of the above exception, another exception occurred:' in trace:
            trace = trace[trace.find(
                'During handling of the above exception, another exception occurred:') + 68:]
        return trace

    def get_real_name(user):
        name = user.first_name
        if type(user.last_name) is str:
            name += ' ' + user.last_name

        if type(user.username) is str:
            name += ' @' + user.username

        return name

    class OCR:
        LT_P = 'пПnPp'
        LT_I = 'иИiI1uІИ́Їіи́ї'
        LT_E = 'еЕeEЕ́е́'
        LT_D = 'дДdD'
        LT_Z = 'зЗ3zZ3'
        LT_M = 'мМmM'
        LT_U = 'уУyYuUУ́у́'
        LT_O = 'оОoO0О́о́'
        LT_L = 'лЛlL'
        LT_S = 'сСcCsS'
        LT_A = 'аАaAА́а́'
        LT_N = 'нНhH'
        LT_G = 'гГgG'
        LT_CH = 'чЧ4'
        LT_K = 'кКkK'
        LT_C = 'цЦcC'
        LT_R = 'рРpPrR'
        LT_H = 'хХxXhH'
        LT_YI = 'йЙy'
        LT_YA = 'яЯЯ́я́'
        LT_YO = 'ёЁ'
        LT_YU = 'юЮЮ́ю́'
        LT_B = 'бБ6bB'
        LT_T = 'тТtT'
        LT_HS = 'ъЪ'
        LT_SS = 'ьЬ'
        LT_Y = 'ыЫ'

        exceptions = ('команд', 'рубл', 'премь', 'оскорб', 'краснояр', 'бояр', 'ноябр', 'карьер', 'мандат', 'употр', 'плох', 'интер', 'веер', 'фаер', 'феер', 'hyundai', 'тату', 'браконь', 'roup', 'сараф', 'держ', 'слаб', 'ридер', 'истреб', 'потреб', 'коридор', 'sound', 'дерг', 'подоб', 'коррид', 'дубл', 'курьер', 'экст', 'try', 'enter', 'oun', 'aube', 'ibarg', '16', 'kres', 'глуб', 'ebay', 'eeb', 'shuy', 'ансам', 'cayenne', 'ain', 'oin', 'тряс', 'ubu', 'uen', 'uip',
                      'oup', 'кораб', 'боеп', 'деепр', 'хульс', 'een', 'ee6', 'ein', 'сугуб', 'карб', 'гроб', 'лить', 'рсук', 'влюб', 'хулио', 'ляп', 'граб', 'ибог', 'вело', 'ебэ', 'перв', 'eep', 'ying', 'laun', 'чаепитие', 'озлоб', 'козолуп', 'грёб', 'греб', 'теб', 'себ', 'мандарин', 'сабля', 'колеб', 'облит', 'собл', 'хула', 'хульн', 'дробл', 'оглобл', 'глазолуп', 'двое', 'трое', 'ябед', 'яблон', 'яблоч', 'ипостас', 'скипидар', 'ветхую', 'бляш', 'хулит', 'епископ', 'хулив', )

        @staticmethod
        def censor(text, charset='UTF-8', exc=()):
            utf8 = 'UTF-8'

            if charset != utf8:
                text = text.decode(charset).encode(utf8)
            #спизжено
            m = re.findall(r'\b\d*('
                           '\w*[' + OCR.LT_P + '][' + OCR.LT_I + OCR.LT_E +
                           '][' + OCR.LT_Z + '][' + OCR.LT_D + ']\w*'  # пизда
                           '|(?:[^' + OCR.LT_I + OCR.LT_U + '\s]+|' + OCR.LT_N + OCR.LT_I + ')?(?<!стра)[' + OCR.LT_H + '][' + OCR.LT_U + '][' + OCR.LT_YI + \
                           OCR.LT_E + OCR.LT_YA + OCR.LT_YO + OCR.LT_I + OCR.LT_L + OCR.LT_YU + \
                           '](?!иг)\w*'  # хуй; не пускает "подстрахуй", "хулиган"
                           '|\w*[' + OCR.LT_B + '][' + OCR.LT_L + \
                           '](?:[' + OCR.LT_YA + ']+[' + \
                           OCR.LT_D + OCR.LT_T + ']?'
                           '|[' + OCR.LT_I + ']+[' + OCR.LT_D + OCR.LT_T + ']+'
                           # бля, блядь; не пускает "бляха"
                           '|[' + OCR.LT_I + ']+[' + OCR.LT_A + ']+)(?!х)\w*'
                           '|(?:\w*[' + OCR.LT_YI + OCR.LT_U + OCR.LT_E + OCR.LT_A + OCR.LT_O + OCR.LT_HS + OCR.LT_SS + OCR.LT_Y + OCR.LT_YA + '][' + OCR.LT_E + \
                           OCR.LT_YO + OCR.LT_YA + OCR.LT_I + \
                           '][' + OCR.LT_B + OCR.LT_P + \
                           '](?!ы\b|ол)\w*'  # не пускает "еёбы", "наиболее", "наибольшее"...
                           '|[' + OCR.LT_E + OCR.LT_YO + '][' + OCR.LT_B + ']\w*'
                           '|[' + OCR.LT_I + '][' + OCR.LT_B + \
                           '][' + OCR.LT_A + ']\w+'
                           '|[' + OCR.LT_YI + '][' + OCR.LT_O + '][' + \
                           OCR.LT_B + OCR.LT_P + ']\w*)'  # ебать
                           #'|\w*[' + OCR.LT_S + '][' + OCR.LT_C + ']?[' + OCR.LT_U + ']+(?:[' + OCR.LT_CH + ']*[' + OCR.LT_K + ']+'
                           # '|[' + OCR.LT_CH + ']+[' + OCR.LT_K + ']*)[' + OCR.LT_A + OCR.LT_O + ']\w*' # сука
                           '|\w*(?:[' + OCR.LT_P + '][' + OCR.LT_I + OCR.LT_E + '][' + OCR.LT_D + '][' + \
                           OCR.LT_A + OCR.LT_O + OCR.LT_E + \
                           ']?[' + OCR.LT_R + \
                           '](?!о)\w*'  # не пускает "Педро"
                           '|[' + OCR.LT_P + '][' + OCR.LT_E + '][' + OCR.LT_D + '][' + \
                           OCR.LT_E + OCR.LT_I + \
                           ']?[' + OCR.LT_G + OCR.LT_K + '])'  # пидарас
                           '|\w*[' + OCR.LT_Z + '][' + OCR.LT_A + OCR.LT_O + '][' + \
                           OCR.LT_L + '][' + OCR.LT_U + \
                           '][' + OCR.LT_P + ']\w*'  # залупа
                           '|\w*[' + OCR.LT_M + '][' + OCR.LT_A + '][' + OCR.LT_N + \
                           '][' + OCR.LT_D + '][' + OCR.LT_A + \
                           OCR.LT_O + ']\w*'  # манда
                           '|\w*[' + OCR.LT_G + '][' + OCR.LT_O + OCR.LT_A + '][' + OCR.LT_N + \
                           '][' + OCR.LT_D + '][' + OCR.LT_O + \
                           '][' + OCR.LT_N + ']\w*'  # гондон
                           ')', text)
            return m

    logging.basicConfig(
        filename="debug.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)
    logger = logging.getLogger(__name__)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'

    path = os.path.dirname(os.path.abspath(__file__)) + "/"

    conn = sqlite3.connect(path + "database.db", check_same_thread=False)
    db = conn.cursor()
    # db.execute("""CREATE TABLE users (tg_id INTEGER PRIMARY KEY, real_name TEXT, reg INTEGER, fsm TEXT, premium INTEGER, premium_expires INTEGER) """)
    # db.execute("""CREATE TABLE chats (tg_id INTEGER PRIMARY KEY, real_name TEXT, settings TEXT, admins TEXT, owner INTEGER) """)
    # db.execute("""CREATE TABLE banlist (tg_id INTEGER PRIMARY KEY, reason TEXT, bantime INTEGER, chat INTEGER) """)
    # db.execute("""CREATE TABLE sessions (session_id TEXT PRIMARY KEY, tg_id INTEGER, expires INTEGER, ip text) """)
    # db.execute("""CREATE TABLE spam (user text primary key, messages TEXT) """)
    # db.execute("""CREATE TABLE logs (chat_id integer primary key, logs TEXT) """)
    # conn.commit()

    session_ttl = 60 * 60 * 24 * 7
    session_ttl_auth = 60 * 30
    sessions_ip_limit = 3

    store_logs = 60 * 60 * 24 * 7

    class dbHelper():
        def __init__(self, db):
            self.db = db

        def check_existence(self, table, col, key):
            try:
                if type(key) is str:
                    key = "'" + key.replace("'", "\\'") + "'"
                c = self.db.execute(
                    'select exists(select 1 from %s where %s=%s) as c' % (table, col, key))
                return c.fetchone()[0] == 1
            except:
                logger.error(traceback.format_exc())
                return False

        def remove(self, table, col, val):
            try:
                if type(val) is str:
                    val = "'" + val.replace("'", "\\'") + "'"
                self.db.execute('delete from %s where %s=%s' %
                                (table, col, val))
                conn.commit()
            except:
                logger.error(traceback.format_exc())
                return False

        def update(self, table, col, val, col2, val2):
            try:
                if type(val) is str:
                    val = "'" + val.replace("'", "\\'") + "'"

                if type(val2) is str:
                    val2 = "'" + val2.replace("'", "\\'") + "'"
                res = self.db.execute('update %s set %s=%s where %s=%s' % (
                    table, col, val, col2, val2)).fetchone()
                conn.commit()
                return res
            except:
                logger.error(traceback.format_exc())
                return False

        def new_log(self, chat_id):
            try:
                self.db.execute('insert into logs values (?,"{}")', (chat_id,))
                conn.commit()
                return True
            except:
                logger.error(traceback.format_exc())
                return False

        def get_logs(self, chat_id):
            try:
                return db.execute('select * from logs where chat_id=? limit 1', (chat_id,)).fetchone()
            except:
                logger.error(traceback.format_exc())
                return False

        def log_msg(self, chat_id, log_prop):
            try:
                if not self.check_existence('logs', 'chat_id', chat_id):
                    self.new_log(chat_id)

                logs = self.get_logs(chat_id)
                try:
                    logs = json.loads(logs[1])
                except:
                    logs = {}

                if log_prop not in logs:
                    logs[log_prop] = []

                if len(logs[log_prop]) > 0:
                    first_time = logs[log_prop][0]
                else:
                    first_time = 0

                logs[log_prop].append(round(time.time()) - first_time)

                self.db.execute(
                    'update logs set logs=? where chat_id=?', (json.dumps(logs), chat_id))
                conn.commit()
                return True
            except:
                logger.error(traceback.format_exc())
                return False

        def _sessions_ip_limit(self, ip):
            try:
                rows = self.db.execute(
                    'select * from sessions where ip=?', (ip,)).fetchall()
                if len(rows) >= sessions_ip_limit:
                    self.remove('sessions', 'ip', ip)

                return True
            except:
                logger.error(traceback.format_exc())
                return False

        def new_session(self, session_id, ip):
            try:
                self._sessions_ip_limit(ip)
                self.db.execute('insert into sessions values (?,0,' +
                                str(round(time.time() + session_ttl)) + ', ?)', (session_id, ip))
                conn.commit()
                return True
            except:
                logger.error(traceback.format_exc())
                return False

        def auth_session(self, session_id, user_id):
            try:
                self.update('sessions', 'tg_id', user_id,
                            'session_id', session_id)
                return True
            except:
                logger.error(traceback.format_exc())
                return False

        def new_user(self, user_info):
            try:
                self.db.execute(
                    "INSERT into users values (?,?,?,?,?,?)", user_info)
                conn.commit()
                return True
            except:
                logger.error(traceback.format_exc())
                return False

        def new_spam_entrance(self, tg_id, chat):
            try:
                self.db.execute("INSERT into spam values (?,'[]')",
                                (str(tg_id) + '_' + str(chat),))
                conn.commit()
                return True
            except:
                logger.error(traceback.format_exc())
                return False

        def add_spam_entrance(self, tg_id, chat):
            try:
                spams = self.get_spam_entrances(tg_id, chat)
                try:
                    spams = spams[1]
                    spams = json.loads(spams)
                except:
                    spams = []

                if len(spams) > 0:
                    first_spam = spams[0]
                else:
                    first_spam = 0

                spams.append(round(time.time()) - first_spam)
                spams = json.dumps(spams)
                self.update('spam', 'messages', spams, 'user',
                            str(tg_id) + '_' + str(chat))
                return True
            except:
                logger.error(traceback.format_exc())
                return False

        def get_spam_entrances(self, tg_id, chat):
            try:
                return db.execute('select * from spam where user=? limit 1', (str(tg_id) + '_' + str(chat),)).fetchone()
            except:
                logger.error(traceback.format_exc())
                return False

        def update_user(self, from_user):
            try:
                if not self.check_existence('users', 'tg_id', from_user.id):
                    return False

                session_info = self.update(
                    'sessions', 'real_name', get_real_name(from_user), from_user.id)

                if type(session_info[1]) is int and session_info[1] > 0:
                    return True

                return False
            except:
                logger.error(traceback.format_exc())
                return False

        def verify_session(self, session_id):
            try:
                if not self.check_existence('sessions', 'session_id', session_id):
                    return False

                session_info = self.db.execute(
                    'select * from sessions where session_id=? limit 1', (session_id,)).fetchone()

                if type(session_info[1]) is int and session_info[1] > 0:
                    return True

                return False
            except:
                logger.error(traceback.format_exc())
                return False

        def get_chats(self, session=None):
            try:
                if session is not None:
                    if not self.verify_session(session):
                        return False

                    owner = self.db.execute(
                        'select * from sessions where session_id=? limit 1', (session,)).fetchone()[1]
                    chats = self.db.execute(
                        'select * from chats where owner=?', (owner,)).fetchall()
                    return chats
            except:
                logger.error(traceback.format_exc())
                return False

        def get_table(self, table):
            try:
                return self.db.execute('select * from %s' % (table)).fetchall()
            except:
                logger.error(traceback.format_exc())
                return False

        def check_banlist(self, user_id):
            return False

        def add_chat(self, chat, owner):
            try:
                if self.check_existence('chats', 'tg_id', chat.id):
                    return False

                chat_hash = "chat_" + randhash(30)

                self.db.execute('insert into chats values (?,?,?,?,?,?)', (chat.id,
                                                                           chat.title, "{}", "[" + str(owner) + "]", owner, chat_hash))
                conn.commit()
                return chat_hash
            except:
                logger.error(traceback.format_exc())
                return False

        def get_chat_info(self, chat_hash):
            try:
                chat_info = self.db.execute(
                    'select * from chats where (hash=? or tg_id=?) limit 1', (chat_hash, chat_hash)).fetchone()
                return chat_info
            except:
                logger.error(traceback.format_exc())
                return False

        def get_chat_settings(self, chat_hash):
            try:
                chat_info = self.get_chat_info(chat_hash)
                if chat_info is None or chat_info is False:
                    return False

                return chat_info[2]
            except:
                logger.error(traceback.format_exc())
                return False

        def set_chat_setting(self, chat_hash, setting, value):
            try:
                settings = self.get_chat_settings(chat_hash)
                try:
                    settings = json.loads(settings)
                except:
                    settings = {}

                values = {
                    'true': True,
                    'false': False
                }
                try:
                    value = values[value]
                except KeyError:
                    pass

                settings[setting] = value
                settings = json.dumps(settings)
                self.db.execute(
                    'update chats set settings=? where (hash=? or tg_id=?)', (settings, chat_hash, chat_hash))
                conn.commit()
                return True
            except:
                logger.error(traceback.format_exc())
                return False

    db_helper = dbHelper(db)

    types = telebot.types
    bot = telebot.TeleBot('<token>')

    def telegram_escape_html(html):
        html = html.replace('&', '&amp;')
        html = html.replace('<', '&lt;').replace('>', '&gt;')
        html = re.sub(r'(&lt;b&gt;)(.*)(&lt;\/b&gt;)',
                      r'<b>\2</b>', html, flags=re.M)
        html = re.sub(r'(&lt;i&gt;)(.*)(&lt;\/i&gt;)',
                      r'<i>\2</i>', html, flags=re.M)
        html = re.sub(r'(&lt;u&gt;)(.*)(&lt;\/u&gt;)',
                      r'<u>\2</u>', html, flags=re.M)
        html = re.sub(r'(&lt;s&gt;)(.*)(&lt;\/s&gt;)',
                      r'<s>\2</s>', html, flags=re.M)
        html = re.sub(r'(&lt;code&gt;)(.*)(&lt;\/code&gt;)',
                      r'<code>\2</code>', html, flags=re.M)
        html = re.sub(r'(&lt;pre&gt;)(.*)(&lt;\/pre&gt;)',
                      r'<pre>\2</pre>', html, flags=re.M)
        html = re.sub(r'&lt;a(.*?)&gt;(.*?)&lt;\/a&gt;',
                      r'<a\1>\2</a>', html, flags=re.M)
        # print(html)
        return html

    app = Flask(__name__, static_folder=path + 'static')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['RECAPTCHA_SITE_KEY'] = '<site>'
    app.config['RECAPTCHA_SECRET_KEY'] = '<secret>'
    app.config['RECAPTCHA_ENABLED'] = True
    app.config['RECAPTCHA_THEME'] = 'dark'
    app.config['RECAPTCHA_SIZE'] = 'compact'

    recaptcha = ReCaptcha(app=app)
    # recaptcha.init(app, '<site>', '<secret>', is_enabled=True)

    admins = ['<users-that-are-allowed-to-control-bot>']
    user_chat = '<chat>'
    debug = False

    mark = telebot.types.InlineKeyboardMarkup()
    mark.add(telebot.types.InlineKeyboardButton(
        '🐲 Premium', callback_data="premium"))
    mark.add(telebot.types.InlineKeyboardButton('🖋 Drawer', callback_data="drawer"),
             telebot.types.InlineKeyboardButton('🦊 Account', callback_data="account"))

    cancel = telebot.types.InlineKeyboardMarkup()
    cancel.add(telebot.types.InlineKeyboardButton(
        '🚫 Cancel', callback_data="cancel"))

    choose_lang = telebot.types.InlineKeyboardMarkup()
    choose_lang.add(telebot.types.InlineKeyboardButton(
        '🇷🇺 Русский', callback_data="setlang_ru"))
    choose_lang.add(telebot.types.InlineKeyboardButton(
        '🇺🇸 English', callback_data="setlang_en"))

    join = telebot.types.InlineKeyboardMarkup()
    join.add(telebot.types.InlineKeyboardButton(
        '🐲 To the chat', url="<chat-link>"))
    join.add(telebot.types.InlineKeyboardButton(
        '✅ Confirm', callback_data="cancel"))

    def answer(destination, msg, reply_markup=None, parse_mode="Markdown", reply_to_message_id=None):
        try:
            if isinstance(destination, telebot.types.CallbackQuery):
                try:
                    return bot.edit_message_text(chat_id=destination.message.chat.id, message_id=destination.message.message_id, text=msg, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=True)
                except telebot.apihelper.ApiException as e:
                    try:
                        bot.answer_callback_query(
                            callback_query_id=destination.id)
                        if 'there is no text' in str(e):
                            return bot.send_message(chat_id=destination.message.chat.id, text=msg, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=True)
                    except telebot.apihelper.ApiException as e2:
                        return bot.answer_callback_query(callback_query_id=destination.id)
            elif isinstance(destination, telebot.types.Message):
                return bot.send_message(chat_id=destination.chat.id, text=msg, reply_markup=reply_markup, parse_mode=parse_mode, reply_to_message_id=reply_to_message_id, disable_web_page_preview=True)
            elif isinstance(destination, int) or (isinstance(destination, str) and destination.startswith("@")):
                return bot.send_message(chat_id=destination, text=msg, reply_markup=reply_markup, parse_mode=parse_mode, reply_to_message_id=reply_to_message_id, disable_web_page_preview=True)
        except:
            logger.error(traceback.format_exc())
            return False

    def message_chat(func):
        @wraps(func)
        def decorator(message):
            try:
                if isinstance(message, telebot.types.Message) and message.chat.id > 0:
                    return

                if isinstance(message, telebot.types.Message) and message.chat.id == user_chat and not debug:
                    if message.text.startswith('/a') and message.from_user.id in admins:
                        if message.text.startswith('/a_mute'):
                            amount = message.text.split()[1]
                            if amount != '0':
                                until = time.time() + int(amount) * 60
                            else:
                                until = 0
                            bot.restrict_chat_member(
                                message.chat.id, message.reply_to_message.from_user.id, until_date=until)
                            restrict_markup = telebot.types.InlineKeyboardMarkup()
                            restrict_markup.add(telebot.types.InlineKeyboardButton(
                                '✨ Unmute', callback_data='unmute@' + str(message.reply_to_message.from_user.id)))
                            answer(message, '🎖 [Братик](tg://user?id=' + str(message.reply_to_message.from_user.id) + ')*, твой аккаунт ограничен на ' + amount +
                                   ' минут администратором. Пожалуйста, прочитай правила чата, и больше не нарушай их <3*', reply_to_message_id=message.reply_to_message.id, reply_markup=restrict_markup)
                            bot.delete_message(
                                message.chat.id, message.message_id)
                            bot.delete_message(
                                message.chat.id, message.reply_to_message.id)

                # if db_helper.check_banlist(message.from_user.id):
                #     bot.delete_message(message.chat.id, message.message_id)
                #     return
                db_helper.log_msg(message.chat.id, 'messages')
                return func(message)
            except:
                logger.error(traceback.format_exc())
                return False

        return decorator

    def authorization(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            session_id = request.cookies.get('session')
            if not db_helper.verify_session(session_id):
                return redirect('/auth', 302)
            return func(*args, **kwargs)
        return decorator

    def export_chat_settings(func):
        @wraps(func)
        def decorator(message):
            chat = db_helper.get_chat_info(message.chat.id)
            if chat is None:
                return func(message, None, None)

            try:
                settings = chat[2]
                settings = json.loads(settings)
            except:
                settings = {}

            return func(message, settings, chat)

        return decorator

    def message_user(func):
        @wraps(func)
        def decorator(message):
            global debug
            try:
                if isinstance(message, telebot.types.Message) and message.chat.id < 0:
                    return
                usid = message.from_user.id
                # if db_helper.check_existence('banlist', 'tg_id', usid):
                #     return

                if not db_helper.check_existence('users', 'tg_id', usid):
                    db_helper.new_user([usid, get_real_name(
                        message.from_user), round(time.time()), '', 0, 0])

                # try:
                #     if bot.get_chat_member(user_chat, message.from_user.id).status != "member" and message.from_user.id not in admins:
                #         answer(message, '*🥰 Для продолжения работы с ботом, вступи в чат*', reply_markup=join)
                #         return
                # except telebot.apihelper.ApiException:
                #     answer(message, '*🥰 Для продолжения работы с ботом, вступи в чат*', reply_markup=join)
                #     return

                if debug and message.from_user.id not in admins:
                    answer(message.from_user.id, "⚠️ *В боте ведутся технические работы! Возвращайтесь чуть позже.*\n_The bot is on maintenance. Please, return back later!_")
                    return

                return func(message)

            except:
                logger.error(traceback.format_exc())
                return

        return decorator

    def lead0(num):
        if num > 9:
            return str(num)
        else:
            return '0' + str(num)

    @app.route('/dashboard/<chat_hash>')
    @authorization
    def dashboard_router(chat_hash):
        try:
            chat = db_helper.get_chat_info(chat_hash)
            if chat is False or chat is None:
                return redirect('/', 302)
            settings = chat[2]
            try:
                settings = json.loads(settings)
            except:
                settings = {}

            logs = db_helper.get_logs(chat[0])
            try:
                logs = json.loads(logs[1])
            except:
                logs = {}

            def group_logs(arr):
                res = []
                labels = []
                arr = list(reversed(arr))
                for i in range(len(arr) - 1):
                    arr[i] += arr[-1]

                group_begin_time = arr[0]
                counter = 0
                for i in range(len(arr)):
                    if abs(arr[i] - group_begin_time) >= 60 * 60 or i == len(arr) - 1:
                        res.append(counter)
                        labels.append(
                            lead0(arr[i] % 3600 // 3600) + ':' + lead0(arr[i] % 3600 % 3600 // 60))
                        counter = 0
                        group_begin_time = arr[i]
                    else:
                        counter += 1

                return res, labels

            if 'messages' in logs:
                messages, messages_labels = group_logs(logs['messages'])
            else:
                messages, messages_labels = [], []

            if 'new_chat_members' in logs:
                new_chat_members, new_chat_members_labels = group_logs(
                    logs['new_chat_members'])
            else:
                new_chat_members, new_chat_members_labels = [], []

            if 'captchas' in logs:
                captchas, captchas_labels = group_logs(logs['captchas'])
            else:
                captchas, captchas_labels = [], []

            if 'defend' in logs:
                defend, defend_labels = group_logs(logs['defend'])
            else:
                defend, defend_labels = [], []

            print(defend, defend_labels)

            return render_template('panel.html', chat_name=chat[1], chat_hash=chat_hash, chat_settings=settings, total_messages=sum(messages), messages=messages, total_new_chat_members=sum(new_chat_members), new_chat_members=new_chat_members, total_captchas=sum(captchas), captchas=captchas, messages_labels=messages_labels, new_chat_members_labels=new_chat_members_labels, captchas_labels=captchas_labels, defend_stats=defend, defend_labels=defend_labels)
        except:
            logger.error(traceback.format_exc())
            return False

    @app.route('/new_chat')
    @authorization
    def newchat_router():
        try:
            return make_response(render_template('empty.html', title='<h1>У вас нет чатов</h1>', subtitle='Добавьте <a href="tg://resolve?domain=' + my_username + '&start=newchat">новый</a>.'))
        except:
            logger.error(traceback.format_exc())
            return False

    @app.route('/<templ>.html')
    @authorization
    def template_router(templ):
        try:
            return render_template(templ + '.html')
        except:
            logger.error(traceback.format_exc())
            return False

    @app.route('/auth')
    def auth_router():
        def new_session():
            session_id = randhash(32)
            db_helper.new_session(session_id, request.headers.get('X-Real-IP'))
            res = make_response(render_template('empty.html', title='<h1>Необходима авторизация</h1>',
                                                subtitle='Пройдите авторизацию <a href="tg://resolve?domain=' + my_username + '&start=login_' + session_id + '">здесь</a>'))
            res.set_cookie('session', session_id, max_age=session_ttl)
            return res

        if not request.cookies.get('session'):
            return new_session()
        else:
            session_id = request.cookies.get('session')
            if db_helper.verify_session(session_id):
                return redirect('/', 302)

            if db_helper.check_existence('sessions', 'session_id', session_id):
                return make_response(render_template('empty.html', title='<h1>Необходима авторизация</h1>', subtitle='Пройдите авторизацию <a href="tg://resolve?domain=' + my_username + '&start=login_' + session_id + '">здесь</a>'))
            else:
                return new_session()

    @app.route('/')
    @authorization
    def control_panel_router():
        try:
            chats = db_helper.get_chats(session=request.cookies.get('session'))
            if chats is False or chats is None:
                return redirect('/auth', 302)

            if len(chats) == 0:
                return redirect('/new_chat', 302)

            return redirect('/dashboard/' + str(chats[0][5]), 302)
        except:
            logger.error(traceback.format_exc())
            return False

    @app.route('/api/chat/<chat_hash>/settings/set/<setting>', methods=['POST'])
    @authorization
    def api_settings_router(chat_hash, setting):
        try:
            chat = db_helper.get_chat_info(chat_hash)
            print(chat)
            if chat is False or chat is None:
                return jsonify({'ok': False}), 404

            if '_text' in setting:
                if setting.split('_')[0] not in available_settings:
                    return jsonify({'ok': False}), 400

                if request.values.get('value') == "":
                    return jsonify({'ok': False}), 400
            else:
                if setting not in available_settings:
                    return jsonify({'ok': False}), 400

                if request.values.get('value') not in ['true', 'false']:
                    return jsonify({'ok': False}), 400

            db_helper.set_chat_setting(
                chat_hash, setting, request.values.get('value'))
            return jsonify({'ok': True})
        except:
            logger.error(traceback.format_exc())
            return False

    @app.route('/api/test_censor/<word>', methods=['POST'])
    @authorization
    def test_censor_router(word):
        try:
            return jsonify({'word': word, 'e': len(OCR.censor(word)) > 0})
        except:
            logger.error(traceback.format_exc())
            return False

    @app.route('/.well-known/acme-challenge/<challenge>')
    def acme_challenge(challenge):
        return "%s" % (open(path + '.well-known/acme-challenge/' + str(challenge), 'r').read())

    def flask():
        try:
            sqliteAdminBP = sqliteAdminBlueprint(dbPath=path + "database.db")
            app.register_blueprint(sqliteAdminBP, url_prefix='/sqlite')
            app.run(port=5252)
        except:
            logger.error(traceback.format_exc())
            return False

    @bot.message_handler(content_types=["new_chat_members"])
    @message_chat
    @export_chat_settings
    def handler_new_member(message, settings, chat):
        try:
            db_helper.log_msg(message.chat.id, 'new_chat_members')
            if 'welcome' not in settings or not settings['welcome']:
                return

            if 'welcome_text' not in settings or settings['welcome_text'] == "":
                return

            captcha = None

            msg = answer(message, ".")

            if 'captcha' in settings and settings['captcha']:
                captcha = telebot.types.InlineKeyboardMarkup()
                captcha.add(telebot.types.InlineKeyboardButton('🔰 Пройти капчу', url="https://t.me/" + my_username + "?start=captcha_" + str(
                    message.chat.id) + "_" + str(msg.message_id) + "_" + str(message.new_chat_members[0].id) + "_" + str(message.chat.id)))
                bot.restrict_chat_member(
                    message.chat.id, message.new_chat_members[0].id, until_date=0)
            elif 'raid' in settings and settings['raid'] and 'raid_text' in settings and settings['raid_text']:
                try:
                    settings['raid_text'] = int(settings['raid_text'])
                except:
                    settings['raid_text'] = 15
                bot.restrict_chat_member(message.chat.id, message.new_chat_members[0].id, until_date=int(
                    time.time() + settings['raid_text'] * 60))
            # print(telegram_escape_html(settings['welcome_text']).replace("{user}", '<a href="tg://user?id=' + str(message.new_chat_members[0].id) + '">' + message.new_chat_members[0].first_name + '</a>'))
            bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=telegram_escape_html(settings['welcome_text']).replace("{user}", '<a href="tg://user?id=' + str(
                message.new_chat_members[0].id) + '">' + message.new_chat_members[0].first_name + '</a>'), parse_mode="HTML", reply_markup=captcha, disable_web_page_preview=True)
        except:
            logger.error(traceback.format_exc())
            return False

    def captcha_kb(captcha_text, remain, unmute):
        captcha = telebot.types.InlineKeyboardMarkup()
        valid_row = random.randint(0, 3)
        for i in range(4):
            if i == valid_row:
                if random.randint(0, 1) == 1:
                    captcha.add(telebot.types.InlineKeyboardButton(randhash(6), callback_data="captcha_invalid_" + str(remain) +
                                                                   "_" + unmute), telebot.types.InlineKeyboardButton(captcha_text, callback_data="captcha_valid_" + unmute))
                else:
                    captcha.add(telebot.types.InlineKeyboardButton(captcha_text, callback_data="captcha_valid_" + unmute),
                                telebot.types.InlineKeyboardButton(randhash(6), callback_data="captcha_invalid_" + str(remain) + "_" + unmute))
                continue

            captcha.add(telebot.types.InlineKeyboardButton(randhash(6), callback_data="captcha_invalid_" + str(remain) + "_" + unmute),
                        telebot.types.InlineKeyboardButton(randhash(6), callback_data="captcha_invalid_" + str(remain) + "_" + unmute))
        return captcha

    def send_captcha(chat_id, remain, unmute):
        captcha_text = randhash(6)
        image_captcha = ImageCaptcha()
        data = image_captcha.generate(captcha_text)
        image_captcha.write(captcha_text, '/tmp/' + captcha_text + '.png')
        del image_captcha
        bot.send_photo(chat_id, photo=open('/tmp/' + captcha_text + '.png', 'rb'), caption="🔰 *Для вступления в чат, пожалуйста, реши капчу*\n`Осталось попыток: " +
                       str(remain) + "/3`", parse_mode="Markdown", reply_markup=captcha_kb(captcha_text, remain, unmute))

    @bot.message_handler(content_types=["text"], func=lambda message: message.chat.id > 0)
    @message_user
    def handle_text_message(message):
        if message.text == "/start":
            bot.send_photo(message.chat.id, photo=open('greeting.jpg', 'rb'))
            answer(message, start_menu_message, reply_markup=mark)
        elif message.text.startswith('/start login_'):
            session_id = message.text.split('_', 1)[1]
            if not db_helper.check_existence('sessions', 'session_id', session_id):
                answer(
                    message, "*🚫 Сессия истекла, либо ссылка неверная. Попробуйте авторозваться еще раз*")
                return

            if db_helper.auth_session(session_id, message.from_user.id):
                db_helper.update_user(message.from_user)
                answer(
                    message, "*✅ Аутентификация прошла успешно. Можете возвращаться на сайт.*")
                return
        elif message.text == "/start newchat":
            answer(message, "*🗣 Для добавления нового чата выполни следующие действия:*\n\n    `1. Добавь меня в чат`\n    `2. Дай права администратора - все, кроме \"Анонимность\"`\n    `3. Напиши команду /add_chat`\n\n*После выполнения действий ты получишь уведомление*")
        elif message.text.startswith("/start captcha_"):
            unmute = message.text.split("_", 3)[3]
            bot.delete_message(*message.text.split("_", 3)[1:3])
            send_captcha(message.chat.id, 3, unmute)

    @bot.callback_query_handler(func=lambda call: call.message.chat.id > 0)
    def callback(call):
        try:
            if call.data.startswith("captcha_valid"):
                user_id, chat_id = call.data.split('_')[2:4]
                bot.promote_chat_member(chat_id, int(user_id))
                answer(call, "*✅ Отлично, ты можешь писать в чате!*")
                bot.delete_message(call.message.chat.id,
                                   call.message.message_id)
            elif call.data.startswith("captcha_invalid"):
                db_helper.log_msg(int(call.data.split('_')[4]), 'captchas')
                remain = int(call.data.split('_')[2]) - 1
                unmute = '_'.join(call.data.split('_')[3:])
                if remain <= 0:
                    answer(
                        call, "*🚫 К сожалению, попытки решить капчу закончились. Обратись к Администратору чата для разблокировки.*")
                    return
                bot.delete_message(call.message.chat.id,
                                   call.message.message_id)
                send_captcha(call.message.chat.id, remain, unmute)
            elif call.data.startswith('aunmute') and call.from_user.id in admins:
                bot.promote_chat_member(
                    call.message.chat.id, int(call.data.split('_')[1]))
                bot.delete_message(call.message.chat.id,
                                   call.message.message_id)
        except:
            logger.error(traceback.format_exc())
            return False

    @bot.callback_query_handler(func=lambda call: call.message.chat.id < 0)
    def callback_chat(call):
        try:
            if call.data.startswith('aunmute') and call.from_user.id in admins:
                bot.promote_chat_member(
                    call.message.chat.id, int(call.data.split('_')[1]))
                bot.delete_message(call.message.chat.id,
                                   call.message.message_id)
        except:
            logger.error(traceback.format_exc())
            return False

    @bot.message_handler(content_types=["text"], func=lambda message: message.chat.id < 0)
    @message_chat
    @export_chat_settings
    def handle_text_message_chat(message, settings, chat):
        if message.text == "/add_chat":
            if message.from_user.id not in admins:
                return

            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass
            result = db_helper.add_chat(message.chat, message.from_user.id)
            if result is False:
                answer(message.from_user.id, '*🚫 Ошибка добавления чата *`' + message.chat.title.replace('`', '\\`') +
                       '`*.\nПожалуйста, убедись, что:*\n    `1. Ты выдал боту права администратора`\n    `2. Ты являешься администратором чата`\n    `3. Ты ранее не добавлял этот чат в бота`\n\n*Если добавить чат не удается, напиши в тех.поддержку*')
            else:
                dashboard = telebot.types.InlineKeyboardMarkup()
                dashboard.add(telebot.types.InlineKeyboardButton(
                    '📋 Панель управления чатом', url="https://moderator.innocoffee.ru/dashboard/" + result))
                answer(message.from_user.id, '*✅ Чат *`' + message.chat.title.replace('`', '\\`') +
                       '`* успешно добавлен в бота!*\nДля перехода в панель управления чатом, нажми на кнопку', reply_markup=dashboard)
        elif message.text.startswith('/a') and message.from_user.id in admins:
            if message.text == "/a del":
                bot.delete_message(
                    message.chat.id, message.reply_to_message.id)
                bot.delete_message(message.chat.id, message.message_id)

        if "spam" in settings and settings['spam'] and message.from_user.id not in json.loads(chat[3]):
            user = db_helper.get_spam_entrances(
                message.from_user.id, message.chat.id)
            if not user:
                db_helper.new_spam_entrance(
                    message.from_user.id, message.chat.id)
                user = [message.from_user.id, message.chat.id, "[]"]

            try:
                spams = json.loads(user[1])
            except:
                spams = []

            # spams = list(filter(lambda x: x >= time.time() - 60 * 60, spams))
            if len(spams) >= int(settings['spam_text']):
                bot.delete_message(message.chat.id, message.message_id)
                bot.restrict_chat_member(
                    message.chat.id, message.from_user.id, until_date=time.time() + (30 * 60))
                db_helper.log_msg(message.chat.id, "defend")
                unmute_btn = telebot.types.InlineKeyboardMarkup()
                unmute_btn.add(telebot.types.InlineKeyboardButton(
                    '🗿 Размутить', callback_data="aunmute_" + str(message.from_user.id)))
                answer(message, "*🤭 Я временно ограничил права *[" + get_real_name(message.from_user).replace('[', '\\[').replace(
                    ']', '\\]') + "](tg://user?id=" + str(message.from_user.id) + ")\nПричина: `SPAM`\nВремя ограничения: `30 минут`", reply_markup=unmute_btn)

            else:
                db_helper.add_spam_entrance(
                    message.from_user.id, message.chat.id)

        if "censor" in settings and settings["censor"] and message.from_user.id not in json.loads(chat[3]):
            if len(OCR.censor(message.text)) > 0:
                bot.delete_message(message.chat.id, message.message_id)
                # bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time() + (5 * 60))
                db_helper.log_msg(message.chat.id, "defend")
                unmute_btn = telebot.types.InlineKeyboardMarkup()
                unmute_btn.add(telebot.types.InlineKeyboardButton(
                    '🗿 Размутить', callback_data="aunmute_" + str(message.from_user.id)))
                answer(message, "*🗣 Я временно ограничил права *[" + get_real_name(message.from_user).replace('[', '\\[').replace(']', '\\]') + "](tg://user?id=" + str(
                    message.from_user.id) + ")\nПричина: `Explicit Content`\nВремя ограничения: `5 минут`", reply_markup=unmute_btn)

    @bot.message_handler(content_types=['voice'], func=lambda message: message.chat.id < 0)
    @export_chat_settings
    def voice_processing(message, settings, chat):
        try:
            if 'voices' not in settings or not settings['voices']:
                return

            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            filename = '/tmp/' + str(round(time.time()))
            with open(filename + '.ogg', 'wb') as new_file:
                new_file.write(downloaded_file)

            song = AudioSegment.from_ogg(filename + '.ogg')
            song.export(filename + '.wav', format="wav")
            msg = bot.reply_to(
                message, "<b>🗣 Распознаю голосовое сообщение...</b>", parse_mode="HTML")
            try:
                r = sr.Recognizer()
                with sr.AudioFile(filename + '.wav') as source:
                    audio_data = r.record(source)
                    text = r.recognize_google(audio_data, language='ru-RU')
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                          text='<b>👆 Текст этого войса:</b>\n<pre>' + text + '</pre>', parse_mode="HTML")
            except:
                logger.error(traceback.format_exc())
                bot.delete_message(msg.chat.id, msg.message_id)
        except:
            logger.error(traceback.format_exc())
            return False

    @bot.message_handler(content_types=['photo'], func=lambda message: message.chat.id < 0)
    @export_chat_settings
    def voice_processing(message, settings, chat):
        try:
            if 'nsfw' not in settings or not settings['nsfw']:
                return

            warn = answer(message, "🔞 *Проверяю файл на наличие NSFW...*",
                          reply_to_message_id=message.message_id)

            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            filename = '/tmp/' + str(round(time.time())) + '.jpg'
            with open(filename, 'wb') as new_file:
                new_file.write(downloaded_file)

            result = detector.detect(filename, mode="fast")
            # print(result)
            if len(result) > 0:
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except:
                    pass

                try:
                    bot.delete_message(warn.chat.id, warn.message_id)
                except:
                    pass
                bot.restrict_chat_member(
                    message.chat.id, message.from_user.id, until_date=time.time() + (30 * 60))
                db_helper.log_msg(message.chat.id, "defend")
                unmute_btn = telebot.types.InlineKeyboardMarkup()
                unmute_btn.add(telebot.types.InlineKeyboardButton(
                    '🗿 Размутить', callback_data="aunmute_" + str(message.from_user.id)))
                answer(message, "*🔞 Я временно ограничил права *[" + get_real_name(message.from_user).replace('[', '\\[').replace(
                    ']', '\\]') + "](tg://user?id=" + str(message.from_user.id) + ")\nПричина: `NSFW`\nВремя ограничения: `60 минут`", reply_markup=unmute_btn)

            try:
                bot.delete_message(warn.chat.id, warn.message_id)
            except:
                pass

        except:
            logger.error(traceback.format_exc())
            return False

    def check_nsfw(file_info, message):
        warn = answer(message, "🔞 *Проверяю файл на наличие NSFW...*\n*▱▱▱▱▱▱▱▱▱▱ 0%*",
                      reply_to_message_id=message.message_id)

        downloaded_file = bot.download_file(file_info.file_path)
        filename = '/tmp/' + str(round(time.time()))
        with open(filename + '.mp4', 'wb') as new_file:
            new_file.write(downloaded_file)

        frames = get_video_length(filename + '.mp4')
        split_cmd = ["ffmpeg", "-i", filename + '.mp4',
                     "-vf", "fps=1", filename + "%03d.png"]
        subprocess.run(split_cmd, check=True, capture_output=True)
        for n in range(0, frames):
            result = detector.detect(
                filename + '00' + str(n + 1) + ".png", mode="fast")
            if len(result) > 0:
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except:
                    pass

                try:
                    bot.delete_message(warn.chat.id, warn.message_id)
                except:
                    pass
                bot.restrict_chat_member(
                    message.chat.id, message.from_user.id, until_date=time.time() + (30 * 60))
                db_helper.log_msg(message.chat.id, "defend")
                unmute_btn = telebot.types.InlineKeyboardMarkup()
                unmute_btn.add(telebot.types.InlineKeyboardButton(
                    '🗿 Размутить', callback_data="aunmute_" + str(message.from_user.id)))
                answer(message, "*🔞 Я временно ограничил права *[" + get_real_name(message.from_user).replace('[', '\\[').replace(
                    ']', '\\]') + "](tg://user?id=" + str(message.from_user.id) + ")\nПричина: `NSFW`\nВремя ограничения: `60 минут`", reply_markup=unmute_btn)
                return
            try:
                bot.edit_message_text(chat_id=warn.chat.id, message_id=warn.message_id, text="🔞 *Проверяю файл на наличие NSFW...*\n*" + ('▰' * round(
                    (n + 1) / frames * 10)) + ('▱' * round(10 - (n + 1) / frames * 10)) + " " + str(round((n + 1) / frames * 100)) + "%*", parse_mode="Markdown")
            except:
                pass
        try:
            bot.delete_message(warn.chat.id, warn.message_id)
        except:
            pass

    @bot.message_handler(content_types=['video'], func=lambda message: message.chat.id < 0)
    @export_chat_settings
    def video_processing(message, settings, chat):
        try:
            if 'nsfw' not in settings or not settings['nsfw']:
                return

            file_info = bot.get_file(message.video[-1].file_id)
            check_nsfw(file_info, message)
        except:
            logger.error(traceback.format_exc())
            return False

    @bot.message_handler(content_types=['animation'], func=lambda message: message.chat.id < 0)
    @export_chat_settings
    def animation_processing(message, settings, chat):
        try:
            if 'nsfw' not in settings or not settings['nsfw']:
                return

            file_info = bot.get_file(message.document.file_id)
            check_nsfw(file_info, message)
        except:
            logger.error(traceback.format_exc())
            return False

    def db_worker():
        while True:
            try:
                spams = db_helper.get_table('spam')
                if spams:
                    for row in spams:
                        chat = row[0].split('_')[1]
                        chat_info = db_helper.get_chat_info(int(chat))
                        try:
                            settings = json.loads(chat_info[2])
                        except:
                            settings = {}
                        if not chat_info or 'spam' in settings or not settings['spam']:
                            db_helper.remove('spam', 'user', row[0])
                            continue

                        user_spams = json.loads(row[1])

                        def clear_first_entrance(returning=False):
                            if len(user_spams) > 0:
                                if time.time() - user_spams[0] > 60 * 60 * 24:
                                    if len(user_spams) > 1:
                                        user_spams[1] += user_spams[0]
                                        del user_spams[0]
                                        return clear_first_entrance(True)

                                    del user_spams[0]
                                    return True

                            return returning

                        if clear_first_entrance():
                            db_helper.update(
                                'sessions', 'sessions_id', row[0], json.dumps(user_spams))

                sessions = db_helper.get_table('sessions')
                if sessions:
                    for row in sessions:
                        if row[2] - session_ttl + session_ttl_auth < time.time() and row[1] == 0:
                            db_helper.remove('sessions', 'session_id', row[0])
            except:
                logger.error(traceback.format_exc())
                pass
            time.sleep(120)

    threading.Thread(target=flask).start()
    threading.Thread(target=db_worker).start()
    bot.polling(none_stop=True, timeout=10)
except:
    print(traceback.format_exc())
