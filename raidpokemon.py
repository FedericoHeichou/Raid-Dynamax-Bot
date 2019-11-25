import telebot
from telebot import types
import json
import random



with open('token.txt', 'r') as filee:
    token = filee.read().replace('\n', '')

bot = telebot.TeleBot(token)
user_dict = {}



class Raid():
    def __init__(self):
        self.idd = None
        self.pokemon = None
        self.stars = None
        self.owner = None
        self.fc = None
        self.players = []
        self.players_id = []
        self.pin = None



@bot.message_handler(commands=['start'])
def home(message):
    try:
        cid = message.chat.id

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        text = ''
        if message.chat.type == 'private':
            text += texts["welcome1"]
        text += texts["welcome2"]

        bot.send_message(cid, text, parse_mode='HTML')

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.message_handler(commands=['add'])
def yourfc(message):
    try:
        cid = message.chat.id

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        if message.chat.type == 'private':
            text = texts['not_available']
            bot.send_message(cid, text, parse_mode='HTML')
        else:
            with open('friendcodes.json', 'r') as filee:
                data = json.load(filee)

            if message.text == '/add' or message.text == '/add@RaidDynamaxBot':
                bot.send_message(cid, texts["incomplete_fc_error"], parse_mode='HTML')
            else:
                fc = message.text.replace('/add', '')
                fc = fc.replace(' ', '')
                if 'SW-' in fc:
                    fc = fc.replace('SW-', '')
                else:
                    pass

                check = fc
                
                for block in range(3):
                    if block != 0:
                        if check[0] == '-':
                            check = check.replace(check[0], '', 1)
                        else:
                            msg = bot.send_message(cid, texts["fc_error"], parse_mode='HTML')
                            break

                    try:
                        if msg:
                            break
                    except Exception:
                        pass

                    for num in range(4):
                        if check[0] in '0123456789':
                            check = check.replace(check[0], '', 1)
                            continue
                        else:
                            msg = bot.send_message(cid, texts["fc_error"], parse_mode='HTML')
                            break
                
                    try:
                        if msg:
                            break
                    except Exception:
                        pass

                try:
                    if msg:
                        pass
                except Exception:
                    if message.chat.type != 'private' and check == '':
                        if str(message.from_user.id) not in data[str(cid)]:
                            text = texts['fc_add']

                        data[str(cid)].update({message.from_user.id:{fc:message.from_user.first_name}})
                        for idd in data[str(cid)]:
                            if idd == str(message.from_user.id):
                                try:
                                    if text:
                                        pass
                                except Exception:
                                    text = texts['fc_update']
                                break
                    else:
                        text = texts['not_available']

                    bot.send_message(cid, text, parse_mode='HTML')

                    with open('friendcodes.json', 'w') as filee:
                        json.dump(data, filee, indent=4)

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.message_handler(commands=['show'])
def show_fc(message):
    try:
        cid = message.chat.id

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        with open('friendcodes.json', 'r') as filee:
            data = json.load(filee)

        if message.chat.type == 'private':
            text = texts['not_available']
            bot.send_message(cid, text, parse_mode='HTML')
        else:
            if str(cid) not in data:
                bot.send_message(cid, texts['no_fcs'], parse_mode='HTML')
            else:
                text = texts['list']
                for idd in data[str(cid)]:
                    for i in data[str(cid)][idd].keys():
                        fc = i
                        break
                    for i in data[str(cid)][idd].values():
                        name = i
                        break
                    text += name + ': ' + fc + '\n'

                try:
                    bot.send_message(cid, text, parse_mode='HTML')
                except Exception:
                    bot.send_message(cid, texts['no_fcs'], parse_mode='HTML')

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.message_handler(commands=['showme'])
def show_my_fc(message):
    try:
        cid = message.chat.id

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        with open('friendcodes.json', 'r') as filee:
            data = json.load(filee)

        if message.chat.type == 'private':
            text = texts['not_available']
            bot.send_message(cid, text, parse_mode='HTML')
        else:
            if str(cid) not in data:
                bot.send_message(cid, texts['no_fc'], parse_mode='HTML')
            else:
                for idd in data[str(cid)]:
                    if idd == str(message.from_user.id):
                        fc = [i for i in data[str(cid)][idd]][0]
                        name = data[str(cid)][idd][fc]
                        text = name + ': ' + fc
                        break

                try:
                    bot.send_message(cid, text, parse_mode='HTML')
                except UnboundLocalError:
                    bot.send_message(cid, texts['no_fc'], parse_mode='HTML')

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.message_handler(commands=['new'])
def new_raid(message):
    try:
        cid = message.chat.id

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        if message.chat.type == 'private':
            text = texts['not_available']
            bot.send_message(cid, text, parse_mode='HTML')
        else:
            with open('friendcodes.json', 'r') as filee:
                data = json.load(filee)

            raid = Raid()
            user_dict[message.from_user.id] = raid

            if message.text == '/new' or message.text == '/new@RaidDynamaxBot':
                bot.send_message(cid, texts['new_raid_error'], parse_mode='HTML')
            else:
                raid.idd = message.from_user.id
                if '/new@RaidDynamaxBot ' in message.text:
                    raid.pokemon = message.text.replace('/new@RaidDynamaxBot ', '')
                else:
                    raid.pokemon = message.text.replace('/new ', '')
                raid.owner = message.from_user.first_name
                try:
                    raid.fc = list(data[str(cid)][str(message.from_user.id)].keys())[0]
                except Exception:
                    raid.fc = '-'

                players = ['-', '-', '-']
                n = 0
                for i in range(len(raid.players)):
                    players[n] = raid.players[n]
                    n = n + 1

                text = texts['new_raid'].format(
                    raid.pokemon,
                    raid.owner,
                    raid.fc,
                    players[0],
                    players[1],
                    players[2]
                )

                markup = types.InlineKeyboardMarkup()
                star1 = types.InlineKeyboardButton('⭐️', callback_data='1stars'+str(raid.idd))
                star2 = types.InlineKeyboardButton('⭐️⭐️', callback_data='2stars'+str(raid.idd))
                star3 = types.InlineKeyboardButton('⭐️⭐️⭐️', callback_data='3stars'+str(raid.idd))
                star4 = types.InlineKeyboardButton('⭐️⭐️⭐️⭐️', callback_data='4stars'+str(raid.idd))
                star5 = types.InlineKeyboardButton('⭐️⭐️⭐️⭐️⭐️', callback_data='5stars'+str(raid.idd))
                markup.row(star1, star2)
                markup.row(star3, star4)
                markup.row(star5)
                join = types.InlineKeyboardButton('🙋‍♂️Partecipa🙋‍♂️', callback_data='join_raid'+str(raid.idd))
                done = types.InlineKeyboardButton('🚫Chiudi🚫', callback_data='done'+str(raid.idd))
                markup.row(join)
                markup.row(done)

                bot.send_message(cid, text, parse_mode='HTML', reply_markup=markup)

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.callback_query_handler(func=lambda call: 'stars' in call.data)
def stars(call):
    try:
        cid = call.message.chat.id
        mid = call.message.message_id
        stars = call.data[0]
        call.data = call.data.replace(stars, '', 1)
        raid = user_dict[int(call.data.replace('stars', ''))]

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        if call.from_user.id != raid.idd:
            text = texts['not_creator']
            bot.answer_callback_query(call.id, text, True)

        else:
            emoji = ''
            for i in range(int(stars)):
                emoji += '⭐️'
            raid.stars = emoji

            players = ['-', '-', '-']
            n = 0
            for i in range(len(raid.players)):
                players[n] = raid.players[n]
                n = n + 1

            text = texts['new_raid'].format(
                raid.pokemon + ' ' + raid.stars,
                raid.owner,
                raid.fc,
                players[0],
                players[1],
                players[2]
            )

            markup = types.InlineKeyboardMarkup()
            join = types.InlineKeyboardButton('🙋‍♂️Partecipa🙋‍♂️', callback_data='join_raid'+str(raid.idd))
            done = types.InlineKeyboardButton('🚫Chiudi🚫', callback_data='done'+str(raid.idd))
            markup.row(join)
            markup.row(done)

            bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode='HTML')

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.callback_query_handler(func=lambda call: 'join_raid' in call.data)
def join(call):
    try:
        cid = call.message.chat.id

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        mid = call.message.message_id
        raid = user_dict[int(call.data.replace('join_raid', ''))]

        if len(raid.players) > 3:
            bot.answer_callback_query(call.id, texts['full_raid'], True)
        else:
            if call.from_user.first_name != raid.owner:
                if call.from_user.id not in raid.players_id:
                    if len(raid.players) < 3:
                        raid.players.append(call.from_user.first_name)
                        raid.players_id.append(call.from_user.id)
                else:
                    raid.players.remove(call.from_user.first_name)
                    raid.players_id.remove(call.from_user.id)

                players = ['-', '-', '-']
                n = 0
                for i in range(len(raid.players)):
                    players[n] = raid.players[n]
                    n = n + 1

                markup = types.InlineKeyboardMarkup()
                if raid.stars == None:
                    star1 = types.InlineKeyboardButton('⭐️', callback_data='1stars'+str(raid.idd))
                    star2 = types.InlineKeyboardButton('⭐️⭐️', callback_data='2stars'+str(raid.idd))
                    star3 = types.InlineKeyboardButton('⭐️⭐️⭐️', callback_data='3stars'+str(raid.idd))
                    star4 = types.InlineKeyboardButton('⭐️⭐️⭐️⭐️', callback_data='4stars'+str(raid.idd))
                    star5 = types.InlineKeyboardButton('⭐️⭐️⭐️⭐️⭐️', callback_data='5stars'+str(raid.idd))
                    markup.row(star1, star2)
                    markup.row(star3, star4)
                    markup.row(star5)

                    text = texts['new_raid'].format(
                        raid.pokemon,
                        raid.owner,
                        raid.fc,
                        players[0],
                        players[1],
                        players[2]
                    )
                else:
                    text = texts['new_raid'].format(
                        raid.pokemon + ' ' + raid.stars,
                        raid.owner,
                        raid.fc,
                        players[0],
                        players[1],
                        players[2]
                    )

                join = types.InlineKeyboardButton('🙋‍♂️Partecipa🙋‍♂️', callback_data='join_raid'+str(raid.idd))
                done = types.InlineKeyboardButton('🚫Chiudi🚫', callback_data='done'+str(raid.idd))
                markup.row(join)
                markup.row(done)

                bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode='HTML')

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.callback_query_handler(func=lambda call: 'done' in call.data)
def done(call):
    try:
        cid = call.message.chat.id

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        mid = call.message.message_id
        raid = user_dict[int(call.data.replace('done', ''))]

        if call.from_user.id == raid.idd:
            markup = types.InlineKeyboardMarkup()
            yes = types.InlineKeyboardButton('✅Conferma✅', callback_data='yes'+str(raid.idd))
            no = types.InlineKeyboardButton('❌Indietro❌', callback_data='no'+str(raid.idd))
            markup.row(yes)
            markup.row(no)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, texts['not_creator'], True)

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.callback_query_handler(func=lambda call: 'yes' in call.data)
def confirm(call):
    try:
        cid = call.message.chat.id

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        mid = call.message.message_id
        raid = user_dict[int(call.data.replace('yes', ''))]

        if call.from_user.id == raid.idd:
            players = ['-', '-', '-']
            n = 0
            for i in range(len(raid.players)):
                players[n] = raid.players[n]
                n = n + 1

            if raid.stars == None:
                text = texts['new_raid'].format(
                    raid.pokemon,
                    raid.owner,
                    raid.fc,
                    players[0],
                    players[1],
                    players[2]
                )
            else:
                text = texts['new_raid'].format(
                    raid.pokemon + ' ' + raid.stars,
                    raid.owner,
                    raid.fc,
                    players[0],
                    players[1],
                    players[2]
                )

            text += texts['raid_closed']

            pin = ''
            for i in range(4):
                pin += random.choice('0123456789')
            raid.pin = pin

            markup = types.InlineKeyboardMarkup()
            see_pin = types.InlineKeyboardButton('🔒Password🔒', callback_data='password'+str(raid.idd))
            markup.add(see_pin)

            bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode='HTML')
        else:
            bot.answer_callback_query(call.id, texts['not_creator'], True)

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.callback_query_handler(func=lambda call: 'no' in call.data)
def back(call):
    try:
        cid = call.message.chat.id

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        mid = call.message.message_id
        raid = user_dict[int(call.data.replace('no', ''))]

        if call.from_user.id == raid.idd:
            players = ['-', '-', '-']
            n = 0
            for i in range(len(raid.players)):
                players[n] = raid.players[n]
                n = n + 1

            markup = types.InlineKeyboardMarkup()
            if raid.stars == None:
                star1 = types.InlineKeyboardButton('⭐️', callback_data='1stars'+str(raid.idd))
                star2 = types.InlineKeyboardButton('⭐️⭐️', callback_data='2stars'+str(raid.idd))
                star3 = types.InlineKeyboardButton('⭐️⭐️⭐️', callback_data='3stars'+str(raid.idd))
                star4 = types.InlineKeyboardButton('⭐️⭐️⭐️⭐️', callback_data='4stars'+str(raid.idd))
                star5 = types.InlineKeyboardButton('⭐️⭐️⭐️⭐️⭐️', callback_data='5stars'+str(raid.idd))
                markup.row(star1, star2)
                markup.row(star3, star4)
                markup.row(star5)

                text = texts['new_raid'].format(
                    raid.pokemon,
                    raid.owner,
                    raid.fc,
                    players[0],
                    players[1],
                    players[2]
                )
            else:
                text = texts['new_raid'].format(
                    raid.pokemon + ' ' + raid.stars,
                    raid.owner,
                    raid.fc,
                    players[0],
                    players[1],
                    players[2]
                )

            join = types.InlineKeyboardButton('🙋‍♂️Partecipa🙋‍♂️', callback_data='join_raid'+str(raid.idd))
            done = types.InlineKeyboardButton('🚫Chiudi🚫', callback_data='done'+str(raid.idd))
            markup.row(join)
            markup.row(done)

            bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode='HTML')
        else:
            bot.answer_callback_query(call.id, texts['not_creator'], True)

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.callback_query_handler(func=lambda call: 'password' in call.data)
def password(call):
    try:
        raid = user_dict[int(call.data.replace('password', ''))]

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        if call.from_user.id in raid.players_id or call.from_user.id == int(call.data.replace('password', '')):
            bot.answer_callback_query(call.id, raid.pin, True)
        else:
            bot.answer_callback_query(call.id, texts["not_player"], True)

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



@bot.message_handler(commands=['credits'])
def credits(message):
    try:
        cid = message.chat.id

        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

        text = texts['credits']
        bot.send_message(cid, text)

    except Exception as e:
        bot.send_message(312012637, '`' + str(e) + '`', parse_mode='Markdown')



bot.polling(none_stop=True)