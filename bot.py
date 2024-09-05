import time
import logging
import asyncio
import requests
import sqlite3 as sl
from yoomoney import Quickpay

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tkn import TOKEN

print("Запуск бота")
bot = Bot(TOKEN, parse_mode="HTML")
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop)
HELP = """
Для начала работы Вам необходимо создать аккаунт в нашей системе.

Если аккаунт уже имеется войдите в него по данному образцу.
🔑
/<b>login</b> ВАШ_ПАРОЛЬ
🔑
Войдя в аккаунт, вам откроется полный доступ к нашему сервису!
"""
HELPLOG = """
<strong>Вам доступны следующие команды:</strong>

1. 📊Отследить курс крипты в реальном времени:

2. 💎INVASION FEATURES:

3. 🌀Торговля криптой на демо-счете:

4. 💳Пополнить счет:

5. 🏦Узнать свой баланс:

6. 💸Вывод средств:

Чтобы выйти из аккаунта, введите команду: /<b>exit</b>
"""

keygame = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="хотите совершить другую сделку?"
    )
keyboardhelp1 = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="Введите интересующую вас команду"
        )
keyboardhelp = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="Регистрация"
        )
keyboardvalut = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="Хотите поторговать?"
        )
keyboardhlp = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Список команд"
    )
keyboardbalance = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="Операции с балансом"
        )
keyboardfeat = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="не хватает средств"
        )
keyboardupdown = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="куда пойдет курс?"
        )
keyboardchoice = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="выбор монеты"
        )
keyboardx = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="плечо сделки"
        )
keyboardyes = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="Подтвеждение"
        )
bu = types.KeyboardButton(text="✅")
bu1 = types.KeyboardButton(text="❌")
keyboardyes.row(bu)
keyboardyes.row(bu1)
ikm = InlineKeyboardMarkup(row_width=2)
close1 = InlineKeyboardButton(text="Закрыть сделку.", callback_data=f"CLOSE")
ikm.add(close1)
ikmda = InlineKeyboardMarkup(row_width=1)
ye = InlineKeyboardButton(text="Да", callback_data="yes")
no = InlineKeyboardButton(text="Нет", callback_data="no")
ikmda.row(ye)
ikmda.row(no)
butfet0 = types.KeyboardButton(text="1X")
butfet = types.KeyboardButton(text="10X")
butfet1 = types.KeyboardButton(text="20X")
butfet2 = types.KeyboardButton(text="50X")
butbtc = types.KeyboardButton(text="BTC")
buteth = types.KeyboardButton(text="ETH")
butsol = types.KeyboardButton(text="SOL")
buttons1 = types.KeyboardButton(text="📊Узнать курс валют📊")
buttons2 = types.KeyboardButton(text="💎INVASION FEATURES💎")
buttons3 = types.KeyboardButton(text="🌀Торговать на демо-счете🌀")
buttons4 = types.KeyboardButton(text="🏦Узнать свой баланс🏦")
buttons5 = types.KeyboardButton(text="💳Пополнить счет💳")
buttons6 = types.KeyboardButton(text="💸Вывод средств💸")
buttonhelp = types.KeyboardButton(text="📢Список команд📢")
butup = types.KeyboardButton(text="Вверх")
butdown = types.KeyboardButton(text="Вниз")
butreg = types.KeyboardButton(text="Регистрация.")
keygame.row(buttons3)
keygame.row(buttonhelp)
keyboardhelp1.row(buttons1, buttons2, buttons3)
keyboardhelp1.row(buttons5, buttons4, buttons6)
keyboardhelp.row(butreg)
keyboardvalut.row(buttons2, buttons3)
keyboardvalut.row(buttons1)
keyboardvalut.row(buttonhelp)
keyboardhlp.row(buttonhelp)
keyboardbalance.row(buttons5, buttons6)
keyboardbalance.row(buttonhelp)
keyboardfeat.row(buttons3, buttons5)
keyboardfeat.row(buttonhelp)
keyboardupdown.row(butup)
keyboardupdown.row(butdown)
keyboardchoice.row(butbtc)
keyboardchoice.row(buteth, butsol)
keyboardx.row(butfet0)
keyboardx.row(butfet, butfet1)
keyboardx.row(butfet2)
crypto = dict.fromkeys(['btc', 'eth', 'sol', 'matic', 'near', 'aptos'], '')
cryptoold = dict.fromkeys(['btcold', 'ethold', 'solold', 'maticold', 'nearold', 'aptosold'], '')
abalance = 'balance'
abtc = 'btc'
aeth = 'eth'
asol = 'sol'
amatic = 'matic'
anear = 'near'
aaptos = 'aptos'
abtcold = 'btcold'
aethold = 'ethold'
asolold = 'solold'
amaticold = 'maticold'
anearold = 'nearold'
aaptosold = 'aptosold'

con = sl.connect('logg.db')
cur = con.cursor()

cur.execute("SELECT * FROM userinfo")
result = cur.fetchall()
print(result)


machine = []
aa = 0
for a in result:
    machine.append(dict.fromkeys(['userid', 'currentregister', 'sec', 'userbuy', 'userset', 'xxx', 'crypt', 'updown', 'mymessage', 'pribil', 'balance', 'login', 'pay']))
    machine[aa]['userid'] = result[aa][0]
    machine[aa]['balance'] = result[aa][3]
    machine[aa]['login'] = 0
    machine[aa]['currentregister'] = 0
    aa += 1
for a in machine:
    print(a)


async def find(user):
    for i in range(len(machine)):
        if machine[i]['userid'] == user:
            return i


async def getalll():
    global crypto
    global cryptoold
    cryptoold['btcold'] = crypto['btc']
    cryptoold['solold'] = crypto['sol']
    cryptoold['ethold'] = crypto['eth']
    cryptoold['maticold'] = crypto['matic']
    cryptoold['nearold'] = crypto['near']
    cryptoold['aptosold'] = crypto['aptos']
    r = requests.get('https://api.binance.com/api/v3/ticker/bookTicker')
    a = r.json()
    for i in a:
        if i['symbol'] == 'BTCUSDT':
            crypto['btc'] = i['bidPrice'][:8]
        elif i['symbol'] == 'ETHUSDT':
            crypto['eth'] = i['bidPrice'][:7]
        elif i['symbol'] == 'SOLUSDT':
            crypto['sol'] = i['bidPrice'][:5]
        elif i['symbol'] == 'MATICUSDT':
            crypto['matic'] = i['bidPrice'][:6]
        elif i['symbol'] == 'NEARUSDT':
            crypto['near'] = i['bidPrice'][:5]
        elif i['symbol'] == 'APTUSDT':
            crypto['aptos'] = i['bidPrice'][:7]


async def getall():
    while True:
        await getalll()
        await asyncio.sleep(1)


async def geturl(summ):
    quickpay = Quickpay(
        receiver="g",#здесь писать получателя
        quickpay_form="shop",
        targets="Donation",
        paymentType="SB",
        sum=summ,
        label="aaaaaaaaaa"
    )
    return quickpay.redirected_url


async def game(info, messageid):
    print(info)
    for i in range(600):
        if info['updown'] == "up":
            info['pribil'] = int(float(info['userset']) * float(info['xxx']) * (float(crypto[info['crypt']]) / float(info['userbuy']) - 1))
        else:
            info['pribil'] = int(float(info['userset']) * float(info['xxx']) * (float(info['userbuy']) / float(crypto[info['crypt']]) - 1))
        await messageid.edit_text(f"Вы зашли  на  <b>{info['crypt'].upper()} ${info['userbuy']}</b>\n\n"
                                  f"Текущий курс <b>{info['crypt'].upper()} ${crypto[info['crypt']]}</b>\n\n"
                                  f"Ваша текущая прибыль: <b>{info['pribil']}</b>\n\n"
                                  f"Осталось <b>{info['sec']}</b> сек.", reply_markup=ikm)
        info['sec'] -= 1
        if info['currentregister'] == 77:
            break
        await asyncio.sleep(1)
    await getalll()
    await messageid.edit_text("&#60 - - - -")
    await messageid.edit_text("&#60 &#60 - - -")
    await messageid.edit_text("&#60 &#60 &#60 - -")
    await messageid.edit_text("&#60 &#60 &#60 &#60 -")
    await messageid.edit_text("&#60 &#60 &#60 &#60 &#60")
    await messageid.edit_text("ЗАВЕРШЕНО")
    await messageid.delete()
    if info['updown'] == "up":
        info['pribil'] = int(
            float(info['userset']) * float(info['xxx']) * (float(crypto[info['crypt']]) / float(info['userbuy']) - 1))
    else:
        info['pribil'] = int(
            float(info['userset']) * float(info['xxx']) * (float(info['userbuy']) / float(crypto[info['crypt']]) - 1))
    ke = f"""
    Поздравляем! Вы выиграли {info['pribil']}р.

Теперь на вашем демо-счете:
[{info['pribil'] + info['balance']}р.]
Хотите совершить другую сделку?
    """
    kelose = f"""
Вы проиграли {info['pribil']}р.

Теперь на вашем демо-счете:
[{info['pribil'] + info['balance']}р.]
Хотите совершить другую сделку?
    """
    if info['updown'] == "up":
        if crypto[info['crypt']] > info['userbuy']:
            cur.execute(f"""UPDATE userinfo SET userbalance = {info['pribil'] + info['balance']} WHERE userid={info['userid']}""")
            info['balance'] += info['pribil']
            await bot.send_message(info['userid'], "📈")
            await bot.send_message(info['userid'], ke, reply_markup=keygame)
        else:
            cur.execute(f"""UPDATE userinfo SET userbalance = {info['pribil'] + info['balance']} WHERE userid={info['userid']}""")
            info['balance'] += info['pribil']
            await bot.send_message(info['userid'], "📉")
            await bot.send_message(info['userid'], kelose, reply_markup=keygame)
    else:
        if crypto[info['crypt']] < info['userbuy']:
            cur.execute(f"""UPDATE userinfo SET userbalance = {info['pribil'] + info['balance']} WHERE userid={info['userid']}""")
            info['balance'] += info['pribil']
            await bot.send_message(info['userid'], "📈")
            await bot.send_message(info['userid'], ke, reply_markup=keygame)
        else:
            cur.execute(f"""UPDATE userinfo SET userbalance = {info['pribil'] + info['balance']} WHERE userid={info['userid']}""")
            info['balance'] += info['pribil']
            await bot.send_message(info['userid'], "📉")
            await bot.send_message(info['userid'], kelose, reply_markup=keygame)

    cur.execute(f"""UPDATE userinfo SET currentregister = '0' WHERE userid={info['userid']}""")
    cur.execute(f"""UPDATE userinfo SET userbuy = '0' WHERE userid={info['userid']}""")
    cur.execute(f"""UPDATE userinfo SET updown = '0' WHERE userid={info['userid']}""")
    cur.execute(f"""UPDATE userinfo SET userset = '0' WHERE userid={info['userid']}""")
    cur.execute(f"""UPDATE userinfo SET crypt = '0' WHERE userid={info['userid']}""")
    cur.execute(f"""UPDATE userinfo SET close = '0' WHERE userid={info['userid']}""")
    info['currentregister'] = 0
    con.commit()


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    infom = await find(message.from_user.id)
    if infom == None:
        cur.execute(f"""INSERT INTO userinfo VALUES({message.from_user.id}, '0', '0', '100000', '0', '0', '0', '0', '0', '0', '0', '0')""")
        con.commit()
        machine.append(dict.fromkeys(['userid', 'currentregister', 'sec', 'userbuy', 'userset', 'xxx', 'crypt', 'updown', 'mymessage', 'pribil', 'balance', 'login', 'pay']))
        machine[-1]['userid'] = message.from_user.id
        machine[-1]['balance'] = 100000
        machine[-1]['login'] = 0
        await message.answer("📣<b>CRYPTO INVASION приветствует Вас!</b>📣\nДля помощи с работой нашей биржи откройте <b>список команд!</b>", reply_markup=keyboardhlp)
        await message.delete()
    else:
        await message.answer("И снова здравствуйте!", reply_markup=keyboardhlp)
        await message.delete()
    con.commit()


@dp.message_handler(text="📢Список команд📢")
async def help_handler(message: types.Message):
    if machine[await find(message.from_user.id)]['login'] == 1:
        await message.answer(HELPLOG, reply_markup=keyboardhelp1)
    else:
        await message.answer(HELP, reply_markup=keyboardhelp)
    await message.delete()


@dp.message_handler(text="📊Узнать курс валют📊")
async def price_handler(message: types.Message):
    if machine[await find(message.from_user.id)]['login'] == 1:
        price = f'<strong>📊 Текущий курс монет 📊\n\n' \
                f'BTC ${crypto[abtc]} &#60 &#60 ${cryptoold[abtcold]}\n\n' \
                f'ETH ${crypto[aeth]} &#60 &#60 ${cryptoold[aethold]}\n\n' \
                f'SOL ${crypto[asol]} &#60 &#60 ${cryptoold[asolold]}\n\n' \
                f'MATIC ${crypto[amatic]} &#60 &#60 ${cryptoold[amaticold]}\n\n' \
                f'NEAR ${crypto[anear]} &#60 &#60 ${cryptoold[anearold]}\n\n' \
                f'APTOS ${crypto[aaptos]} &#60 &#60 ${cryptoold[aaptosold]}</strong>'
        await message.answer(price, reply_markup=keyboardvalut)
        await message.delete()
    else:
        await message.answer("Вам отказано в доступе! Войдите под своим аккаунтом.")
        await message.delete()


@dp.message_handler(text="Регистрация.")
async def register_handler(message: types.Message):
    cur.execute(f"SELECT userpassword FROM userinfo WHERE userid = {message.from_user.id}")
    reg = cur.fetchone()
    if reg[0] != '0':
        await message.answer("<b>Вы уже зарегистрированы!</b>\n\n🗝Войдите с помощью команды /login <strong>ВАШ_ПАРОЛЬ</strong>", reply_markup=types.ReplyKeyboardRemove())
    else:
        machine[await find(message.from_user.id)]['currentregister'] = 1
        sql = f"""UPDATE userinfo SET currentregister = '1' WHERE userid = {message.from_user.id}"""
        cur.execute(sql)
        con.commit()
        await message.answer("✏️Придумайте пароль для Вашего аккаунта. Логином будет служить Ваш Telegram аккаунт.", reply_markup=types.ReplyKeyboardRemove())
    await message.delete()
    con.commit()


@dp.message_handler(commands=['login'])
async def login_handler(message: types.Message):
    print(machine[await find(message.from_user.id)])
    if machine[await find(message.from_user.id)]['login'] == 0:
        f = message.get_args()
        cur.execute(f"SELECT * FROM userinfo WHERE userid = {message.from_user.id}")
        log = cur.fetchone()
        if f == log[1]:
            machine[await find(message.from_user.id)]['login'] = 1
            sql = f"""UPDATE userinfo SET useraccess = '1' WHERE userid = {message.from_user.id}"""
            cur.execute(sql)
            con.commit()
            await message.answer("<b>✅Вы успешно авторизовались!</b>\n\nВведите /<b>help</b>, чтобы узнать все доступные для Вас команды.", reply_markup=keyboardhlp)
        else:
            await message.answer("<b>⛔️Вы ввели неправильные данные! Попробуйте еще раз! Восстановить аккаунт можно через нашу тех. поддержку: t.me/deadmetiz</b>")
    else:
        await message.answer("<b>Вы уже авторизованы!</b>\nЕсли хотите выйти из аккаунта введите /<b>exit</b>", reply_markup=keyboardhlp)
    await message.delete()
    con.commit()


@dp.message_handler(commands=['exit'])
async def exit_handler(message: types.Message):
    sql = f"""UPDATE userinfo SET useraccess = '0' WHERE userid = {message.from_user.id}"""
    cur.execute(sql)
    con.commit()
    machine[await find(message.from_user.id)]['login'] = 0
    await message.answer("<b>Вы вышли из своего аккаунта.</b>", reply_markup=keyboardhlp)


@dp.message_handler(text="🏦Узнать свой баланс🏦")
async def balance_handler(message: types.Message):
    if machine[await find(message.from_user.id)]['login'] == 1:
        await message.answer(f'На вашем демо-счет балансе <b>[{machine[await find(message.from_user.id)][abalance]}р.]</b>\nНа вашем реальном балансе <b>[0р.]</b>', reply_markup=keyboardbalance)
    else:
        await message.answer("Вам отказано в доступе! Войдите под своим аккаунтом.")
    await message.delete()
    con.commit()


@dp.message_handler(text="💎INVASION FEATURES💎")
async def trd_handler(message: types.Message):
    if machine[await find(message.from_user.id)]['login'] == 1:
        await message.answer("⚠️<b>Пополните свой баланс!</b>⚠️", reply_markup=keyboardfeat)
    else:
        await message.answer("Вам отказано в доступе!")
    await message.delete()


@dp.message_handler(text="🌀Торговать на демо-счете🌀")
async def trade_handler(message: types.Message):
    if machine[await find(message.from_user.id)]['login'] == 1 and machine[await find(message.from_user.id)]['currentregister'] == 0:
        machine[await find(message.from_user.id)]['currentregister'] = 2
        cur.execute(f"UPDATE userinfo SET currentregister = '2' WHERE userid = {message.from_user.id}")
        await message.answer("Выберите монету для сделки:\nВ <b>данный</b> момент доступны BTC, ETH, SOL.", reply_markup=keyboardchoice)
    else:
        await message.answer("Вы уже торгуете! Подождите пока ваша сделка завершится")
    await message.delete()
    con.commit()


@dp.message_handler(text="💳Пополнить счет💳")
async def money_handler(message: types.Message):
    if machine[await find(message.from_user.id)]['login'] == 1 and machine[await find(message.from_user.id)]['currentregister'] == 0:
        machine[await find(message.from_user.id)]['currentregister'] = 15
        await message.answer(f"На <b>Вашем</b> балансе:\n"
                             f"<b>[0р.]</b>\n"
                             f"Сумма пополнения <b>должна быть выше 700р.</b>\n"
                             f"Напишите сумму пополнения числом.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(f"Пока что вы не можете пополнить баланс", reply_markup=keyboardhlp)


@dp.callback_query_handler()
async def close_handler(callback: types.callback_query):
    if callback.data == 'CLOSE':
        await callback.answer("Вы закрыли сделку!")
        machine[await find(callback.from_user.id)]['currentregister'] = 77
        cur.execute(f"""UPDATE userinfo SET close = 1 WHERE userid = {callback.from_user.id}""")
        con.commit()
    elif callback.data == "yes":
        ikmpop = InlineKeyboardMarkup(row_width=1)
        yes = InlineKeyboardButton(text="💸ОПЛАТА💸", url=f"{await geturl(machine[await find(callback.from_user.id)]['userset'])}")
        no = InlineKeyboardButton(text="❌ОТКАЗ❌", callback_data="no")
        ikmpop.row(yes)
        ikmpop.row(no)
        await machine[await find(callback.from_user.id)]['pay'].edit_text(f"<b>К ОПЛАТЕ:</b>\n"
                                                                          f"<b>{machine[await find(callback.from_user.id)]['userset']}р.</b>", reply_markup=ikmpop)
    elif callback.data == "no":
        machine[await find(callback.from_user.id)]['currentregister'] = 0
        await machine[await find(callback.from_user.id)]['pay'].delete()
        await bot.send_message(callback.from_user.id, "Вы <b>отказались</b> от пополнения.", reply_markup=keyboardhlp)
        await callback.answer("Отказ")


@dp.message_handler()
async def log_handler(message: types.Message):
    if machine[await find(message.from_user.id)]['currentregister'] == 1:
        if ' ' in message.text or len(message.text) <= 5:
            await message.answer('Ваш пароль слишком короткий, либо в нем содержатся пробелы.\n<b>Придумайте более безопасный пароль.</b>')
        else:
            machine[await find(message.from_user.id)]['currentregister'] = 0
            sql = f"""UPDATE userinfo SET userpassword = '{message.text}' WHERE userid = {message.from_user.id}"""
            cur.execute(sql)
            sql = f"""UPDATE userinfo SET currentregister = '0' WHERE userid = {message.from_user.id}"""
            cur.execute(sql)
            await message.answer(f'Вот Ваш пароль: {message.text}\nДля входа в аккаунт используйте команду\n\n/<b>login</b> ВАШ_ПАРОЛЬ\n\nИзменить его можно будет <strong>ТОЛЬКО</strong> через нашу тех. поддержку.')
    elif machine[await find(message.from_user.id)]['currentregister'] == 15:
        if message.text.isdigit():
            if int(message.text) >= 700 and int(message.text) <= 25000:
                machine[await find(message.from_user.id)]['userset'] = int(message.text)
                machine[await find(message.from_user.id)]['pay'] = await message.answer(f'Сумма пополнения:\n'
                                                                                        f'{message.text}р.\n'
                                                                                        f'Вы согласны?', reply_markup=ikmda)
            else:
                await message.answer("Сумма должна превышать 700р.")
        else:
            await message.answer("Напишите число без пробелов и букв")
    elif machine[await find(message.from_user.id)]['currentregister'] == 2:
        if message.text == 'BTC':
            machine[await find(message.from_user.id)]['currentregister'] = 3
            cur.execute(f"""UPDATE userinfo SET crypt = '{abtc}' WHERE userid = {message.from_user.id}""")
            await message.answer(f"Текущий курс BTC: <b>${crypto[abtc]}</b>\n\nКурс BTC 1 сек. назад: <b>${cryptoold[abtcold]}</b>\n\nСкажите, куда по вашему мнению пойдет курс через минуту?", reply_markup=keyboardupdown)
            cur.execute(f"""UPDATE userinfo SET currentregister = '3' WHERE userid = {message.from_user.id}""")
            machine[await find(message.from_user.id)]['crypt'] = 'btc'
        elif message.text == 'SOL':
            machine[await find(message.from_user.id)]['currentregister'] = 3
            cur.execute(f"""UPDATE userinfo SET crypt = '{asol}' WHERE userid = {message.from_user.id}""")
            await message.answer(f"Текущий курс SOL: <b>${crypto[asol]}</b>\n\nКурс SOL 1 сек. назад: <b>${cryptoold[asolold]}</b>\n\nСкажите, куда по вашему мнению пойдет курс через минуту?", reply_markup=keyboardupdown)
            cur.execute(f"""UPDATE userinfo SET currentregister = '3' WHERE userid = {message.from_user.id}""")
            machine[await find(message.from_user.id)]['crypt'] = 'sol'
        elif message.text == 'ETH':
            machine[await find(message.from_user.id)]['currentregister'] = 3
            cur.execute(f"""UPDATE userinfo SET crypt = '{aeth}' WHERE userid = {message.from_user.id}""")
            await message.answer(f"Текущий курс ETH: <b>${crypto[aeth]}</b>\n\nКурс ETH 1 сек. назад: <b>${cryptoold[aethold]}</b>\n\nСкажите, куда по вашему мнению пойдет курс через минуту?", reply_markup=keyboardupdown)
            cur.execute(f"""UPDATE userinfo SET currentregister = '3' WHERE userid = {message.from_user.id}""")
            machine[await find(message.from_user.id)]['crypt'] = 'eth'
        else:
            await message.answer(f"Выберите монету из списка")

    elif machine[await find(message.from_user.id)]['currentregister'] == 3:
        if message.text == "Вверх":
            machine[await find(message.from_user.id)]['currentregister'] = 4
            cur.execute(f"""UPDATE userinfo SET currentregister = '4' WHERE userid = {message.from_user.id}""")
            cur.execute(f"""UPDATE userinfo SET updown = "up" WHERE userid = {message.from_user.id}""")
            machine[await find(message.from_user.id)]['updown'] = 'up'
            await message.answer(f"Выберите плечо сделки. От него будет зависеть ваша прибыль!", reply_markup=keyboardx)
        elif message.text == "Вниз":
            machine[await find(message.from_user.id)]['currentregister'] = 4
            cur.execute(f"""UPDATE userinfo SET currentregister = '4' WHERE userid = {message.from_user.id}""")
            cur.execute(f"""UPDATE userinfo SET updown = "down" WHERE userid = {message.from_user.id}""")
            await message.answer(f"Выберите плечо сделки. От него будет зависеть ваша прибыль!", reply_markup=keyboardx)
            machine[await find(message.from_user.id)]['updown'] = 'down'
        else:
            await message.answer("Вы ввели неправильное направление!")
    elif machine[await find(message.from_user.id)]['currentregister'] == 4:
        if message.text == "1X":
            machine[await find(message.from_user.id)]['currentregister'] = 5
            cur.execute(f"""UPDATE userinfo SET xxx = '1' WHERE userid = {message.from_user.id}""")
            cur.execute(f"""UPDATE userinfo SET currentregister = '5' WHERE userid = {message.from_user.id}""")
            machine[await find(message.from_user.id)]['xxx'] = 1
            sumsd = f"Теперь определимся с суммой сделки.\nСумма должна начинаться от 100\nВаш текущий баланс: {machine[await find(message.from_user.id)]['balance']}"
            await message.answer(sumsd, reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "10X":
            machine[await find(message.from_user.id)]['currentregister'] = 5
            cur.execute(f"""UPDATE userinfo SET xxx = '10' WHERE userid = {message.from_user.id}""")
            cur.execute(f"""UPDATE userinfo SET currentregister = '5' WHERE userid = {message.from_user.id}""")
            machine[await find(message.from_user.id)]['xxx'] = 10
            sumsd = f"Теперь определимся с суммой сделки.\nСумма должна начинаться от 100\nВаш текущий баланс: {machine[await find(message.from_user.id)]['balance']}"
            await message.answer(sumsd, reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "20X":
            machine[await find(message.from_user.id)]['currentregister'] = 5
            cur.execute(f"""UPDATE userinfo SET xxx = '20' WHERE userid = {message.from_user.id}""")
            cur.execute(f"""UPDATE userinfo SET currentregister = '5' WHERE userid = {message.from_user.id}""")
            machine[await find(message.from_user.id)]['xxx'] = 20
            sumsd = f"Теперь определимся с суммой сделки.\nСумма должна начинаться от 100\nВаш текущий баланс: {machine[await find(message.from_user.id)]['balance']}"
            await message.answer(sumsd, reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "50X":
            machine[await find(message.from_user.id)]['currentregister'] = 5
            cur.execute(f"""UPDATE userinfo SET xxx = '50' WHERE userid = {message.from_user.id}""")
            cur.execute(f"""UPDATE userinfo SET currentregister = '5' WHERE userid = {message.from_user.id}""")
            machine[await find(message.from_user.id)]['xxx'] = 50
            sumsd = f"Теперь определимся с суммой сделки.\nСумма должна начинаться от 100\nВаш текущий баланс: {machine[await find(message.from_user.id)]['balance']}"
            await message.answer(sumsd, reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer("Вы ввели неправильное значение!")
    elif machine[await find(message.from_user.id)]['currentregister'] == 5:
        if int(message.text) > machine[await find(message.from_user.id)]['balance'] or int(message.text) < 100:
            await message.answer("Вы ввели сумму меньше 100р., либо же Вам не хватает средств!")
        else:
            machine[await find(message.from_user.id)]['currentregister'] = 6
            cur.execute(f"""UPDATE userinfo SET currentregister = '6' WHERE userid = {message.from_user.id}""")
            cur.execute(f"""UPDATE userinfo SET userset = {int(message.text)} WHERE userid = {message.from_user.id}""")
            machine[await find(message.from_user.id)]['userset'] = int(message.text)
            await message.answer(f"<b>Сделка: {machine[await find(message.from_user.id)]['crypt'].upper()} {int(message.text)}р. {machine[await find(message.from_user.id)]['updown'].upper()}</b>\nПлечо сделки: <b>{machine[await find(message.from_user.id)]['xxx']}X</b>\n\nТекущий курс <b>{crypto[machine[await find(message.from_user.id)]['crypt']]}</b>\n\nПодтвердите сделку.", reply_markup=keyboardyes)
    elif machine[await find(message.from_user.id)]['currentregister'] == 6:
        if message.text == "✅":
            await getalll()
            cur.execute(f"""UPDATE userinfo SET userbuy = {(crypto[machine[await find(message.from_user.id)]['crypt']])} WHERE userid = {message.from_user.id}""")
            machine[await find(message.from_user.id)]['userbuy'] = crypto[machine[await find(message.from_user.id)]['crypt']]
            cur.execute(f"""UPDATE userinfo SET sec = '600' WHERE userid={message.from_user.id}""")
            machine[await find(message.from_user.id)]['sec'] = 600
            cur.execute(f"""UPDATE userinfo SET close = '0' WHERE userid={message.from_user.id}""")
            machine[await find(message.from_user.id)]['mymessage'] = await bot.send_message(message.from_user.id, "Сделка.")
            await message.answer("<b>Желаем удачи!</b>", reply_markup=types.ReplyKeyboardRemove())
            await game(machine[await find(message.from_user.id)], machine[await find(message.from_user.id)]['mymessage'])
        else:
            machine[await find(message.from_user.id)]['currentregister'] = 0
            cur.execute(f"""UPDATE userinfo SET currentregister = '0' WHERE userid = {message.from_user.id}""")
            cur.execute(f"""UPDATE userinfo SET userset = 0 WHERE userid = {message.from_user.id}""")
            cur.execute(f"""UPDATE userinfo SET updown = '0' WHERE userid = {message.from_user.id}""")
            await message.answer("Вы отказались от сделки!", reply_markup=keyboardhelp1)
    else:
        await message.answer("Вы ввели неправильную команду")
    await message.delete()
    con.commit()


if __name__ == '__main__':
    dp.loop.create_task(getall())
    executor.start_polling(dp, skip_updates=True)
