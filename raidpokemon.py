import telebot
from telebot import types
import json
import random


bot = telebot.TeleBot('979765263:AAELCFhUsKZWyjnvwLuAowk8ZNSAHgRxa7k')
user_dict = {}



class Raid():
    def __init__(self):
        self.idd = None
        self.pokemon = None
        self.owner = None
        self.fc = None
        self.players = []
        self.players_id = []
        self.pin = None



@bot.message_handler(commands=['start'])
def home(message):
    cid = message.chat.id

    with open('texts.json', 'r') as filee:
        texts = json.load(filee)

    text = ''
    if message.chat.type != 'group':
        text += texts["welcome1"]
    text += texts["welcome2"]

    bot.send_message(cid, text, parse_mode='HTML')



@bot.message_handler(commands=['add'])
def yourfc(message):
    cid = message.chat.id

    with open('texts.json', 'r') as filee:
        texts = json.load(filee)

    with open('friendcodes.json', 'r') as filee:
        data = json.load(filee)

    if message.text == '/add' or message.text == '/add@RaidDynamaxBot':
        bot.send_message(cid, texts["incomplete_fc_error"], parse_mode='HTML')
    else:
        fc = message.text.replace('/add', '')
        fc = fc.replace(' ', '')
        check = fc

        if 'SW-' in fc:
            fc = fc.replace('SW-', '')
        else:
            pass
        
        for block in range(3):
            if block != 0:
                if check[0] == '-':
                    check = check.replace(check[0], '', 1)
                else:
                    msg = bot.send_message(cid, texts["fc_error"])
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
                    msg = bot.send_message(cid, texts["fc_error"])
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
            text = texts['fc_add']

            if message.chat.type == 'group':
                data[cid] = {}
                data[cid][str(message.from_user.id)] = {fc:message.from_user.first_name}
                for idd in data[cid]:
                    if idd == str(message.from_user.id):
                        text = texts['fc_update']
            else:
                text = texts['not_available']

            bot.send_message(cid, text)

            with open('friendcodes.json', 'w') as filee:
                json.dump(data, filee, indent=4)



@bot.message_handler(commands=['show'])
def show_fc(message):
    cid = message.chat.id

    with open('friendcodes.json', 'r') as filee:
        data = json.load(filee)

    with open('texts.json', 'r') as filee:
        texts = json.load(filee)

    if message.chat.type != 'group':
        text = texts['not_available']
    else:

        for idd in data[str(cid)]:
            if idd == str(message.from_user.id):
                fc = [i for i in data[str(cid)][idd]][0]
                name = data[str(cid)][idd][fc]
                text = name + ': ' + fc + '\n'
                break

    try:
        bot.send_message(cid, text)
    except Exception:
        bot.send_message(cid, texts['no_fc'], parse_mode='HTML')



@bot.message_handler(commands=['showme'])
def show_my_fc(message):
    cid = message.chat.id

    with open('friendcodes.json', 'r') as filee:
        data = json.load(filee)

    for group in data.values():
        for person in group:
            if person == str(cid):
                fc = [i for i in person][0]
                name = person[fc]
                text = name + ': ' + fc
                break

    bot.send_message(cid, text)





@bot.message_handler(commands=['new'])
def new_raid(message):
    cid = message.chat.id

    raid = Raid()
    user_dict[message.from_user.id] = raid

    with open('texts.json', 'r') as filee:
        texts = json.load(filee)

    with open('friendcodes.json', 'r') as filee:
        data = json.load(filee)

    if message.text == '/new':
        bot.send_message(cid, texts['new_raid_error'], parse_mode='HTML')
    else:
        raid.idd = message.from_user.id
        raid.pokemon = message.text.replace('/new ', '')
        raid.owner = message.from_user.first_name
        try:
            raid.fc = list(data[str(message.from_user.id)].keys())[0]
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
        join = types.InlineKeyboardButton('✅Partecipa✅', callback_data='join_raid'+str(raid.idd))
        done = types.InlineKeyboardButton('🚫Chiudi🚫', callback_data='done'+str(raid.idd))
        markup.row(join)
        markup.row(done)

        bot.send_message(cid, text, parse_mode='HTML', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: 'join_raid' in call.data)
def join(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    raid = user_dict[int(call.data.replace('join_raid', ''))]

    with open('texts.json', 'r') as filee:
        texts = json.load(filee)

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

            text = texts['new_raid'].format(
                raid.pokemon,
                raid.owner,
                raid.fc,
                players[0],
                players[1],
                players[2]
            )

            markup = types.InlineKeyboardMarkup()
            join = types.InlineKeyboardButton('✅Partecipa✅', callback_data='join_raid'+str(raid.idd))
            done = types.InlineKeyboardButton('🚫Chiudi🚫', callback_data='done'+str(raid.idd))
            markup.row(join)
            markup.row(done)

            bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode='HTML')



@bot.callback_query_handler(func=lambda call: 'done' in call.data)
def done(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    raid = user_dict[int(call.data.replace('done', ''))]

    with open('texts.json', 'r') as filee:
        texts = json.load(filee)

    if call.from_user.id == raid.idd:
        markup = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton('✅Conferma✅', callback_data='yes'+str(raid.idd))
        no = types.InlineKeyboardButton('❌Indietro❌', callback_data='no'+str(raid.idd))
        markup.row(yes)
        markup.row(no)
        bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, texts['not_creator'], True)



@bot.callback_query_handler(func=lambda call: 'yes' in call.data)
def confirm(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    raid = user_dict[int(call.data.replace('yes', ''))]

    if call.from_user.id == raid.idd:
        with open('texts.json', 'r') as filee:
            texts = json.load(filee)

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



@bot.callback_query_handler(func=lambda call: 'no' in call.data)
def back(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    raid = user_dict[int(call.data.replace('no', ''))]

    with open('texts.json', 'r') as filee:
        texts = json.load(filee)

    if call.from_user.id == raid.idd:
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
        join = types.InlineKeyboardButton('✅Partecipa✅', callback_data='join_raid'+str(raid.idd))
        done = types.InlineKeyboardButton('🚫Chiudi🚫', callback_data='done'+str(raid.idd))
        markup.row(join)
        markup.row(done)

        bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode='HTML')
    else:
        bot.answer_callback_query(call.id, texts['not_creator'], True)




@bot.callback_query_handler(func=lambda call: 'password' in call.data)
def password(call):
    raid = user_dict[int(call.data.replace('password', ''))]

    with open('texts.json', 'r') as filee:
        texts = json.load(filee)

    if call.from_user.id in raid.players_id or call.from_user.id == int(call.data.replace('password', '')):
        bot.answer_callback_query(call.id, raid.pin, True)
    else:
        bot.answer_callback_query(call.id, texts["not_player"], True)



bot.polling()