from aiogram import Bot, Dispatcher, executor, types
from time import strftime
import requests
import json
import logging
import asyncio
import Buttons as Bt
from config import TOKEN
from userdata import Database

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
data = Database()

url = 'https://api.coingecko.com/api/v3/simple/price?ids=&vs_currencies=usd'
big_dict = {
    'ukr': {'start': 'Привіт, я JoiCryptoBot\nЩоб дізнатись мої команди та почати користуватись, напишіть /help',
            'help': 'Налаштуй мову за допомогою /language\nВведи /list щоб обрати потрібні криптовалюти\n'
                    '1 клік - Обрати\n2 клік - Видалити\nALL➕ - Обрати все\n'
                    'ALL➖ - Очистити список\n📈 - Вивести курс\n⬅️ - Вийти з меню\n'
                    'Якщо ви хочете отримати курс лише одної криптовалюти - /one\n\n'
                    '<b>Як регулярно отримувати курс обраних криптовалют?</b>\n'
                    'Введіть /edit, потім змініть список і частоту відправки та увімкніть надсилання\n'
                    '📂 - Змінити список криптовалют\n'
                    '🕑 - Змінити частоту\n'
                    '✅ - Увімкнути\n'
                    '🚫 - Вимкнути\n'
                    '⬅️ - Вийти з меню\n'
                    'Курс оновлюється кожну хвилину\n'
                    '/commands - Усі команди\n',
            'commands': '<b>Команди</b>\n/help - Як використовувати бота\n/language - Обрати мову\n'
                        '/list - Cписок криптовалют\n/one - Обрати одну криптовалюту\n'
                        '/edit - Змінити швидкий список криптовалют',
            'list': 'Оберіть криптовалюти',
            'one': 'Оберіть 1 криптовалюту',
            'edit': ['Cписок криптовалют:', 'Частота відправки:', 'Cтатус:'],
            'status': ['Вимкнуто🚫', 'Увімкнуто✅'],
            'setlist': 'Оберіть криптовалюти',
            'settime': 'Оберіть частоту',
            'wait': 'Почекайте 5 сек...',
            'quick': 'Увімкніть надсилання /edit',
            'language': 'Оберіть мову',
            'choice': 'Мова обрана🇺🇦',
            'times': [['хв', 'хв', 'хв'], ['хв', 'год', 'год'], ['год', 'год', 'год']],
            'lang_time': {'10': ' хв', '15': ' хв', '20': ' хв', '30': ' хв',
                          '1 ': 'год', '3 ': 'год', '6 ': 'год', '12': ' год', '24': ' год'}
            },
    'rus': {'start': 'Привет, я JoiCryptoBot\nЧтобы узнать мои команды и начать пользоваться, напишите /help',
            'help': 'Настройте язык с помощью /language\nВведите /list чтобы выбрать нужные криптовалюты\n'
                    '1 клик – Выбрать\n2 клик - Удалить\nALL➕ - Выбрать все\n'
                    'ALL➖ - Очистить список\n📈 - Вывести курс\n⬅️ - Выйти из меню\n'
                    'Если вы хотите получить курс только одной криптовалюты - /one\n\n'
                    '<b>Как регулярно получать курс выбраных криптовалют?</b>\n'
                    'Введите /edit потом выберите криптовалюты и частоту, затем включите отправку\n'
                    '📂 - Изменить список криптовалют\n'
                    '🕑 - Изменить частоту\n'
                    '✅ - Включить\n'
                    '🚫 - Выключить\n'
                    '⬅️ - Выйти из меню\n'
                    'Курс обновляется каждую минуту\n'
                    '/commands - Все команды\n',
            'commands': '<b>Команды</b>\n/help - Как использовать бота\n/language - Выбрать язык\n'
                        '/list - Cписок криптовалют\n/one - Выбрать одну криптовалюту\n'
                        '/edit - Изменить быстрый список криптовалют\n',
            'list': 'Выберите криптовалютии',
            'one': 'Выберите 1 криптовалюту',
            'edit': ['Список криптовалют:', 'Частота отправки:', 'Cтатус:'],
            'status': ['Выключен🚫', 'Включен✅'],
            'setlist': 'Выберите криптовалюти',
            'settime': 'Выберите частоту',
            'wait': 'Подождите 5 сек...',
            'quick': 'Пожалуйста включите отправку /edit',
            'language': 'Выберите язык',
            'choice': 'Язык выбран🇷🇺',
            'times': [['м', 'м', 'м'], ['м', 'ч', 'ч'], ['ч', 'ч', 'ч']],
            'lang_time': {'10': ' м', '15': ' м', '20': ' м', '30': ' м',
                          '1 ': 'ч', '3 ': 'ч', '6 ': 'ч', '12': ' ч', '24': ' ч'}
            },
    'eng': {'start': 'Hi, I am JoiCryptoBot\nTo know my commands and start using me, tap /help',
            'help': 'Set the language using /language\nEnter /list to select the desired cryptocurrencies\n'
                    '1 click - Select\n2 click - Delete\nALL➕ - Select all\n'
                    'ALL➖ - Clear the list\n📈 - Display exchange rate\n⬅️ - Quit menu\n'
                    'If you want to choice only one cryptocurrency - /one\n\n'
                    '<b>How to get the cryptocurrencies exchange rate constantly?</b>\n'
                    'Enter /edit then set list and frequency, turn status on\n'
                    '📂 - To set list\n'
                    '🕑 - To set frequency\n'
                    '✅ - Turn on\n'
                    '🚫 - Turn off\n'
                    '⬅️ - Quit menu\n'
                    '/commands - All commands\n',
            'commands': '<b>Commands</b>\n/help - How to use bot\n/language - Select Language\n'
                        '/list - Cryptocurrency list\n/one - Choice one cryptocurrency\n/edit - Set quick list\n',
            'list': 'Choice cryptocurrency',
            'one': 'Choice 1 cryptocurrency',
            'edit': ['Cryptocurrency list:', 'Send frequency:', 'Status:'],
            'status': ['Turn off🚫', 'Turn on✅'],
            'setlist': 'Choice cryptocurrencies',
            'settime': 'Choice frequency',
            'wait': 'Wait 5 sec...',
            'quick': 'Turn on sending /edit',
            'language': 'Choice language',
            'choice': 'Language selected🇬🇧',
            'times': [['min', 'min', 'min'], ['min', 'hr', 'hr'], ['hr', 'hr', 'hr']],
            'lang_time': {'10': ' min', '15': ' min', '20': ' min', '30': ' min',
                          '1 ': 'hr', '3 ': 'hr', '6 ': 'hr', '12': ' hr', '24': ' hr'}
            }}
names_dict = {'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'BNB': 'Binance Coin', 'LTC': 'Litecoin', 'DOGE': 'Dogecoin',
              'XRP': 'Ripple', 'ADA': 'Cardano', 'SOL': 'Solana', 'DOT': 'Polkadot', 'TRX': 'Tron',
              'LINK': 'Chainlink', 'NEAR': 'Near Protocol', 'MATIC': 'Polygon', 'ATOM': 'Cosmos',
              'AVAX': 'Avalanche', 'UNI': 'Uniswap'}
cc_list = ['bitcoin', 'ethereum', 'binancecoin', 'litecoin', 'dogecoin', 'ripple', 'cardano',
           'solana', 'polkadot', 'tron', 'chainlink', 'near', 'matic-network',
           'cosmos', 'avalanche-2', 'uniswap']
cc_list_names = {'bitcoin': 'BTC', 'ethereum': 'ETH', 'binancecoin': 'BNB', 'litecoin': 'LTC',
                 'dogecoin': 'DOGE', 'ripple': 'XRP', 'cardano': 'ADA', 'solana': 'SOL',
                 'polkadot': 'DOT', 'tron': 'TRX', 'chainlink': 'LINK', 'near': 'NEAR',
                 'matic-network': 'MATIC', 'cosmos': 'ATOM', 'avalanche-2': 'AVAX', 'uniswap': 'UNI'}
cc_price_list = {}
time_buttons = [['🔟', '1️⃣5️⃣', '2️⃣0️⃣'], ['3️⃣0️⃣', '1️⃣', '3️⃣'], ['6️⃣', '1️⃣2️⃣', '2️⃣4️⃣']]
time_buttons1 = [['10', '15', '20'], ['30', '1', '3'], ['6', '12', '24']]


@dp.message_handler(commands=['start', 'help', 'commands', 'language', 'one', 'list', 'edit'])
async def commands(message: types.Message):
    if message.chat.type == 'private':
        data.add_user(user_id=message.from_user.id)
        language = data.get_data(user_id=message.from_user.id, target='language')
        status = data.get_data(user_id=message.from_user.id, target='switch')
        await message.delete()
        if message.text[1:] == 'one':
            await message.answer('✨')
            await message.answer(big_dict[language][message.text[1:]], reply_markup=Bt.OneListMenu)
        elif message.text[1:] == 'language':
            await message.answer('✨')
            await message.answer(big_dict[language][message.text[1:]], reply_markup=Bt.LanguageMenu)
        elif message.text[1:] == 'list':
            cc_name_list = data.get_data(user_id=message.from_user.id, target='list_0')
            for i in range(4):
                for j in range(4):
                    name = Bt.ListMenu["inline_keyboard"][i][j]['text']
                    if name.replace('✅', '') in cc_name_list:
                        Bt.ListMenu["inline_keyboard"][i][j]['text'] = f"{name.replace('✅', '')}✅"
                    else:
                        Bt.ListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
            await message.answer('✨')
            await message.answer(big_dict[language][message.text[1:]], reply_markup=Bt.ListMenu)
        elif message.text[1:] == 'edit':
            full_list = data.get_data(user_id=message.from_user.id, target='full_list')
            time = data.get_data(user_id=message.from_user.id, target='time')
            if time != '':
                data.change_time(user_id=message.from_user.id, time=time[:2]+big_dict[language]['lang_time'][time[:2]])
                time = data.get_data(user_id=message.from_user.id, target='time')
            await message.answer('✨')
            if status == 0:
                await bot.send_message(message.from_user.id,
                                       f"{big_dict[language]['edit'][0]} {full_list}\n"
                                       f"{big_dict[language]['edit'][1]} {time}\n"
                                       f"{big_dict[language]['edit'][2]} {big_dict[language]['status'][status]}",
                                       reply_markup=Bt.SetMenu)
            else:
                await bot.send_message(message.from_user.id,
                                       f"{big_dict[language]['edit'][0]} {full_list}\n"
                                       f"{big_dict[language]['edit'][1]} {time}\n"
                                       f"{big_dict[language]['edit'][2]} {big_dict[language]['status'][status]}",
                                       reply_markup=Bt.StopMenu)
        else:
            await message.answer(big_dict[language][message.text[1:]], parse_mode='HTML')


@dp.message_handler()
async def delete(message: types.Message):
    if message.chat.type == 'private':
        await message.delete()


@dp.callback_query_handler(text_contains="cc_")
async def callback_cc(call: types.CallbackQuery):
    language = data.get_data(user_id=call.from_user.id, target='language')
    cc_name_list = data.get_data(user_id=call.from_user.id, target='list_0')
    cc_set_list = data.get_data(user_id=call.from_user.id, target='list')
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    if call.data[:4] == 'cc_1':
        for i in range(4):
            for j in range(4):
                name = Bt.ListMenu["inline_keyboard"][i][j]['text']
                if name.replace('✅', '') in cc_name_list:
                    Bt.ListMenu["inline_keyboard"][i][j]['text'] = f"{name.replace('✅', '')}✅"
                else:
                    Bt.ListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
        for i in range(4):
            for j in range(4):
                name = Bt.ListMenu["inline_keyboard"][i][j]['text']
                if (call.data == 'cc_1_all' and name[len(name) - 1] != '✅') or \
                   (call.data == Bt.ListMenu["inline_keyboard"][i][j]['callback_data'] and name[len(name) - 1] != '✅'):
                    data.change_list_0(user_id=call.from_user.id, list_0=name, target='+')
                    Bt.ListMenu["inline_keyboard"][i][j]['text'] = f"{name}✅"
                elif (call.data == 'cc_1_remove' and name[len(name) - 1] == '✅') or \
                     (call.data == Bt.ListMenu["inline_keyboard"][i][j]['callback_data'] and name[len(name) - 1] == '✅'):
                    data.change_list_0(user_id=call.from_user.id, list_0=name.replace('✅', ''), target='-')
                    Bt.ListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
        await bot.send_message(call.from_user.id, '✨')
        await bot.send_message(call.from_user.id, big_dict[language]['list'], reply_markup=Bt.ListMenu)
    elif call.data[:4] == 'cc_3':
        for i in range(4):
            for j in range(4):
                name = Bt.SetListMenu["inline_keyboard"][i][j]['text']
                if name.replace('✅', '') in cc_set_list:
                    Bt.SetListMenu["inline_keyboard"][i][j]['text'] = f"{name.replace('✅', '')}✅"
                else:
                    Bt.SetListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
        for i in range(4):
            for j in range(4):
                name = Bt.SetListMenu["inline_keyboard"][i][j]['text']
                if (call.data == 'cc_3_all' and name[len(name) - 1] != '✅') or \
                   (call.data == Bt.SetListMenu["inline_keyboard"][i][j]['callback_data'] and name[len(name) - 1] != '✅'):
                    data.change_list(user_id=call.from_user.id, new=name, target='+')
                    Bt.SetListMenu["inline_keyboard"][i][j]['text'] = f"{name}✅"
                elif (call.data == 'cc_3_remove' and name[len(name) - 1] == '✅') or \
                     (call.data == Bt.SetListMenu["inline_keyboard"][i][j]['callback_data'] and name[len(name) - 1] == '✅'):
                    data.change_list(user_id=call.from_user.id, new=name.replace('✅', ''), target='-')
                    Bt.SetListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
        await bot.send_message(call.from_user.id, '✨')
        await bot.send_message(call.from_user.id, big_dict[language]['list'], reply_markup=Bt.SetListMenu)
    elif call.data[:4] == 'cc_2':
        for i in range(4):
            for j in range(4):
                name = Bt.OneListMenu["inline_keyboard"][i][j]['text']
                if call.data == Bt.OneListMenu["inline_keyboard"][i][j]['callback_data']:
                    await bot.send_message(call.from_user.id, f'{name} ({names_dict[name]}) - <u>{cc_price_list[name]}</u> USD\n',
                                           parse_mode='HTML')
                    break


@dp.callback_query_handler(text_contains="back")
async def callback_back(call: types.CallbackQuery):
    cc_name_list = data.get_data(user_id=call.from_user.id, target='list_0')
    language = data.get_data(user_id=call.from_user.id, target='language')
    full_list = data.get_data(user_id=call.from_user.id, target='full_list')
    status = data.get_data(user_id=call.from_user.id, target='switch')
    time = data.get_data(user_id=call.from_user.id, target='time')
    if call.data == 'back':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    elif call.data == 'back_2':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        await bot.send_message(call.from_user.id, '✨')
        await bot.send_message(call.from_user.id, f"{big_dict[language]['edit'][0]} {full_list}\n"
                                                  f"{big_dict[language]['edit'][1]} {time}\n"
                                                  f"{big_dict[language]['edit'][2]} {big_dict[language]['status'][status]}",
                               reply_markup=Bt.SetMenu)
    elif call.data == 'back_set_list':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        await bot.send_message(call.from_user.id, '✨')
        await bot.send_message(call.from_user.id, f"{big_dict[language]['edit'][0]} {full_list}\n"
                                                  f"{big_dict[language]['edit'][1]} {time}\n"
                                                  f"{big_dict[language]['edit'][2]} {big_dict[language]['status'][status]}",
                               reply_markup=Bt.SetMenu)
    elif call.data == 'back_set' and full_list != '' and status == 0:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        data.change_switch(user_id=call.from_user.id, target=1)
        data.change_set_time(user_id=call.from_user.id, time=strftime("%H:%M"))
        status = data.get_data(user_id=call.from_user.id, target='switch')
        await bot.send_message(call.from_user.id, '✨')
        await bot.send_message(call.from_user.id, f"{big_dict[language]['edit'][0]} {full_list}\n"
                                                  f"{big_dict[language]['edit'][1]} {time}\n"
                                                  f"{big_dict[language]['edit'][2]} {big_dict[language]['status'][status]}",
                               reply_markup=Bt.StopMenu)
    elif call.data == 'back_stop' and status == 1:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        data.change_switch(user_id=call.from_user.id, target=0)
        data.change_set_time(user_id=call.from_user.id, time="")
        status = data.get_data(user_id=call.from_user.id, target='switch')
        await bot.send_message(call.from_user.id, '✨')
        await bot.send_message(call.from_user.id, f"{big_dict[language]['edit'][0]} {full_list}\n"
                                                  f"{big_dict[language]['edit'][1]} {time}\n"
                                                  f"{big_dict[language]['edit'][2]} {big_dict[language]['status'][status]}",
                               reply_markup=Bt.SetMenu)
    elif call.data == 'back_send' and cc_name_list != []:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        for i in range(4):
            for j in range(4):
                name = Bt.ListMenu["inline_keyboard"][i][j]['text']
                if name[len(name) - 1] == '✅':
                    Bt.ListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
        full_list = ''
        for i in range(len(cc_name_list)):
            full_list = full_list + f'{cc_name_list[i]} ({names_dict[cc_name_list[i]]}) - ' \
                                    f'<u>{cc_price_list[cc_name_list[i]]}</u> USD\n'
        await bot.send_message(call.from_user.id, full_list, parse_mode='HTML')
        data.clear_data(user_id=call.from_user.id, target='list_0')


@dp.callback_query_handler(text_contains="set_")
async def callback_set(call: types.CallbackQuery):
    language = data.get_data(user_id=call.from_user.id, target='language')
    cc_set_list = data.get_data(user_id=call.from_user.id, target='list')
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    await bot.send_message(call.from_user.id, '✨')
    if call.data == 'set_list':
        for i in range(4):
            for j in range(4):
                name = Bt.SetListMenu["inline_keyboard"][i][j]['text']
                if name.replace('✅', '') in cc_set_list:
                    Bt.SetListMenu["inline_keyboard"][i][j]['text'] = f"{name.replace('✅', '')}✅"
                else:
                    Bt.SetListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
        await bot.send_message(call.from_user.id, big_dict[language]['setlist'], reply_markup=Bt.SetListMenu)
    elif call.data == 'set_time':
        for i in range(3):
            for j in range(3):
                Bt.SetTimeMenu["inline_keyboard"][i][j]['text'] = time_buttons[i][j] + big_dict[language]['times'][i][j]
                Bt.SetTimeMenu["inline_keyboard"][i][j]['callback_data'] = f"time_{time_buttons1[i][j]} {big_dict[language]['times'][i][j]}"
        await bot.send_message(call.from_user.id, big_dict[language]['settime'], reply_markup=Bt.SetTimeMenu)


@dp.callback_query_handler(text_contains="time_")
async def callback_time(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    language = data.get_data(user_id=call.from_user.id, target='language')
    status = data.get_data(user_id=call.from_user.id, target='switch')
    full_list = data.get_data(user_id=call.from_user.id, target='full_list')
    data.change_time(user_id=call.from_user.id, time=call.data[5:])
    time = data.get_data(user_id=call.from_user.id, target='time')
    await bot.send_message(call.from_user.id, '✨')
    await bot.send_message(call.from_user.id, f"{big_dict[language]['edit'][0]} {full_list}\n"
                                              f"{big_dict[language]['edit'][1]} {time}\n"
                                              f"{big_dict[language]['edit'][2]} {big_dict[language]['status'][status]}",
                           reply_markup=Bt.SetMenu)


@dp.callback_query_handler(text_contains="lang")
async def callback_lang(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    data.change_language(user_id=call.from_user.id, language=call.data[5:])
    language = data.get_data(user_id=call.from_user.id, target='language')
    await bot.send_message(call.from_user.id, big_dict[language]['choice'])


def big_time_dict(time: str, set_time: str):
    a = []
    if time == "10":
        a = ["00:" + str(i) for i in [int(set_time[3:])] + [int(set_time[3:]) + (int(time[:2]) * i) for i in range(1, 6)]]
        for j in range(1, 24):
            a = a + [f"{j}:" + str(i) for i in [int(set_time[3:])] + [int(set_time[3:]) + (int(time[:2]) * i) for i in range(1, 6)]]
    elif time == "15":
        a = ["00:" + str(i) for i in [int(set_time[3:])] + [int(set_time[3:]) + (int(time[:2]) * i) for i in range(1, 4)]]
        for j in range(1, 24):
            a = a + [f"{j}:" + str(i) for i in [int(set_time[3:])] + [int(set_time[3:]) + (int(time[:2]) * i) for i in range(1, 4)]]
    elif time == "20":
        a = ["00:" + str(i) for i in [int(set_time[3:])] + [int(set_time[3:]) + (int(time[:2]) * i) for i in range(1, 3)]]
        for j in range(1, 24):
            a = a + [f"{j}:" + str(i) for i in [int(set_time[3:])] + [int(set_time[3:]) + (int(time[:2]) * i) for i in range(1, 3)]]
    elif time == "30":
        a = ["00:" + str(i) for i in [int(set_time[3:])] + [int(set_time[3:]) + (int(time[:2]) * i) for i in range(1, 2)]]
        for j in range(1, 24):
            a = a + [f"{j}:" + str(i) for i in [int(set_time[3:])] + [int(set_time[3:]) + (int(time[:2]) * i) for i in range(1, 2)]]
    elif time == "1 ":
        a = [f"{i}:" + set_time[3:] for i in range(24)]
    elif time == "3 ":
        a = [f"{int(set_time[:2]) + 3 * i}:" + set_time[3:] for i in range(8)]
    elif time == "6 ":
        a = [f"{int(set_time[:2]) + 6 * i}:" + set_time[3:] for i in range(4)]
    elif time == "12":
        a = [f"{int(set_time[:2]) + 12 * i}:" + set_time[3:] for i in range(2)]
    elif time == "24":
        a = [set_time]
    for i in range(len(a)):
        if a[i][2] != ':':
            a[i] = "0" + a[i]
        if int(a[i][:2]) > 23:
            a[i] = str(int(a[i][:2]) - 24) + a[i][2:]
            if a[i][2] != ':':
                a[i] = "0" + a[i]
        if int(a[i][3:]) > 59:
            a[i] = a[i][:3] + str(int(a[i][3:]) - 60)
        if len(a[i]) != 5:
            a[i] = a[i][:3] + "0" + a[i][3]
    return a


async def always():
    while True:
        global cc_price_list
        cc_price_list = {}
        for cc in cc_list:
            url1 = url[:50] + cc + url[50:]
            rq = requests.Session().get(url1, timeout=120)
            rq.raise_for_status()
            cc_price_list[cc_list_names[cc]] = json.loads(rq.content.decode('utf-8'))[cc]['usd']
        if data.get_data_all() != 0:
            for elements in data.get_data_all():
                time = data.get_data(user_id=elements, target='time')[:2]
                set_time = data.get_data(user_id=elements, target='set_time')
                if strftime("%H:%M") in big_time_dict(time, set_time):
                    cc_set_list = data.get_data(user_id=elements, target='list')
                    full_list1 = ''
                    for i in range(len(cc_set_list)):
                        full_list1 = full_list1 + f'{cc_set_list[i]} ({names_dict[cc_set_list[i]]}) - ' \
                                                  f'<u>{cc_price_list[cc_set_list[i]]}</u> USD\n'
                    await bot.send_message(elements, full_list1, parse_mode='HTML')
        await asyncio.sleep(60)

if __name__ == '__main__':
    data.init_db()
    asyncio.gather(always())
    executor.start_polling(dp, skip_updates=True)
