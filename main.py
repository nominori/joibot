from aiogram import Bot, Dispatcher, executor, types
from pycoingecko import CoinGeckoAPI
import logging
from time import sleep, strftime
import Buttons as Bt
from maintoken import TOKEN
import userdata as data

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
cg = CoinGeckoAPI()

names_dict = {'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'BNB': 'Binance Coin', 'LTC': 'Litecoin', 'DOGE': 'Dogecoin',
              'XRP': 'Ripple', 'ADA': 'Cardano', 'SOL': 'Solana', 'DOT': 'Polkadot', 'TRX': 'Tron',
              'LINK': 'Chainlink', 'NEAR': 'Near Protocol', 'MATIC': 'Polygon', 'ATOM': 'Cosmos',
              'AVAX': 'Avalanche', 'UNI': 'Uniswap'}
big_dict = {
    'ukr': {'start': 'Привіт, я JoiCryptoBot\nЩоб дізнатись мої команди та почати користуватись, напишіть /about',
            'about': 'Налаштуй мову за допомогою /language\nВведи /list щоб обрати потрібні криптовалюти\n'
                     '1 клік - Вибрати\n2 клік - Видалити\n⬅️ - Повернутись назад\nALL➕ - Обрати все\n'
                     'ALL➖ - Очистити список\n📈 - Вивести курс\n'
                     'Якщо ви хочете вибрати лише одну криптовалюту - /one\n\n'
                     '<b>Як отримувати курс выбраних криптовалют постійно?</b>\n'
                     'Введіть /edit щоб змінити список криптовалют та частоту відправки курсу, а потім написніть:\n'
                     '📂 - Змінити список криптовалют\n'
                     '🕑 - Змінити частоту\n'
                     '/commands - Усі команди\n',
            'commands': '<b>Команди</b>\n/about - Як використовувати бота\n/language - Обрати мову\n'
                        '/list - Cписок криптовалют\n/one - Обрати одну криптовалюту\n'
                        '/edit - Змінити список криптовалют/частоту відправки',
            'list': 'Оберіть криптовалюти',
            'one': 'Оберіть 1 криптовалюту',
            'edit': ['Змінити список криптовалют/частоту', 'Cписок криптовалют:', 'Частота відправки:'],
            'setlist': 'Оберіть криптовалюти',
            'settime': 'Оберіть частоту',
            'wait': 'Почекайте 5 сек...',
            'language': 'Оберіть мову',
            'choice': 'Мова обрана🇺🇦',
            'times': [['хв', 'хв', 'хв'], ['хв', 'год', 'год'], ['год', 'год', 'год']],
            'lang_time': {'10': ' хв', '20': ' хв', '30': ' хв', '45': ' хв',
                          '1 ': 'год', '3 ': 'год', '6 ': 'год', '12': ' год', '24': ' год'}
            },
    'rus': {'start': 'Привет, я JoiCryptoBot\nЧтобы узнать мои команды и начать пользоваться, напишите /about',
            'about': 'Настройте язык с помощью /language\nВведите /list чтобы выбрать нужные криптовалюты\n'
                     '1 клик – Выбрать\n2 клик - Удалить\n⬅️ - Вернуться назад\nALL➕ - Выбрать все\n'
                     'ALL➖ - Очистить список\n📈 - Вывести курс\n'
                     'Если вы хотите выбрать только одну криптовалюту - /one\n\n'
                     '<b>Как получать курс выбраных криптовалют постоянно?</b>\n'
                     'Введыть /edit чтобы изменить список криптовалют и частоту отправки курса, а потом нажмите:\n'
                     '📂 - Изменить список криптовалют\n'
                     '🕑 - Изменить частоту\n'
                     '/commands - Все команды\n',
            'commands': '<b>Команды</b>\n/about - Как использовать бота\n/language - Выбрать язык\n'
                        '/list - Cписок криптовалют\n/one - Выбрать одну криптовалюту\n'
                        '/edit - Изменить список криптовалют/частоту отправки',
            'list': 'Выберите криптовалютии',
            'one': 'Выберите 1 криптовалюту',
            'edit': ['Изменить частоту/список криптовалют', 'Список криптовалют:', 'Частота отправки:'],
            'setlist': 'Выберите криптовалюти',
            'settime': 'Выберите частоту',
            'wait': 'Подождите 5 сек...',
            'language': 'Выберите язык',
            'choice': 'Язык выбран🇷🇺',
            'times': [['м', 'м', 'м'], ['м', 'ч', 'ч'], ['ч', 'ч', 'ч']],
            'lang_time': {'10': ' м', '20': ' м', '30': ' м', '45': ' м',
                          '1 ': 'ч', '3 ': 'ч', '6 ': 'ч', '12': ' ч', '24': ' ч'}
            },
    'eng': {'start': 'Hi, I am JoiCryptoBot\nTo know my commands and start using me, tap /about',
            'about': 'Set the language using /language\nEnter /list to select the desired cryptocurrencies\n'
                     '1 click - Select\n2 click - Delete\n⬅️ - Turn back\nALL➕ - Select all\n'
                     'ALL➖ - Clear the list\n📈 - Display exchange rate\n'
                     'If you want to choice only one cryptocurrency - /one\n\n'
                     '<b>How to get the cryptocurrencies exchange rate constantly?</b>\n'
                     'Enter /edit to set list and frequency\n'
                     '📂 - To set list\n'
                     '🕑 - To set frequency\n'
                     '/commands - All commands\n',
            'commands': '<b>Commands</b>\n/about - How to use bot\n/language - Select Language\n'
                        '/list - Cryptocurrency list\n/one - Choice one cryptocurrency\n/edit - Set list/frequency',
            'list': 'Choice cryptocurrency',
            'one': 'Choice 1 cryptocurrency',
            'edit': ['Set list/frequency', 'Cryptocurrency list:', 'Send frequency:'],
            'setlist': 'Choice cryptocurrencies',
            'settime': 'Choice frequency',
            'wait': 'Wait 5 sec...',
            'language': 'Choice language',
            'choice': 'Language selected🇬🇧',
            'times': [['min', 'min', 'min'], ['min', 'hr', 'hr'], ['hr', 'hr', 'hr']],
            'lang_time': {'10': ' min', '20': ' min', '30': ' min', '45': ' min',
                          '1 ': 'hr', '3 ': 'hr', '6 ': 'hr', '12': ' hr', '24': ' hr'}
            }}
time_buttons = [['🔟', '2️⃣0️⃣', '3️⃣0️⃣'], ['4️⃣5️⃣', '1️⃣', '3️⃣'], ['6️⃣', '1️⃣2️⃣', '2️⃣4️⃣']]
time_buttons1 = [['10', '20', '30'], ['45', '1', '3'], ['6', '12', '24']]
minutes = {'10': '10', '20': '20', '30': '30', '45': '45',
           '1 ': '60', '3 ': '180', '6 ': '360', '12': '720', '24': '1440'}


@dp.message_handler(commands=['about', 'commands', 'list', 'edit', 'one', 'language', 'start'])
async def do(message: types.Message):
    data.add_user(user_id=message.from_user.id)
    """data.add_user_detail(user_id=message.from_user.id, user_username=("@" + str(message.from_user.username)),
                         command=message.text[1:], time_=strftime("%b/%d/%Y %H:%M:%S"))"""
    language = data.get_data(user_id=message.from_user.id, target='language')
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
        await message.answer('✨')
        full_list = data.get_data(user_id=message.from_user.id, target='full_list')
        time = data.get_data(user_id=message.from_user.id, target='time')
        if time != '':
            data.change_time(user_id=message.from_user.id, time=time[:2]+big_dict[language]['lang_time'][time[:2]])
            time = data.get_data(user_id=message.from_user.id, target='time')
        await bot.send_message(message.from_user.id, f"{big_dict[language]['edit'][0]}\n{big_dict[language]['edit'][1]} "
                                                     f"{full_list}\n{big_dict[language]['edit'][2]} {time}",
                               reply_markup=Bt.SetMenu)
    else:
        await message.answer(big_dict[language][message.text[1:]], parse_mode='HTML')


@dp.message_handler()
async def delete(message: types.Message):
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
        currency = call.data[5:]
        price = cg.get_price(ids=currency, vs_currencies='usd')[currency]['usd']
        for i in range(4):
            for j in range(4):
                name = Bt.OneListMenu["inline_keyboard"][i][j]['text']
                Bt.OneListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
                if call.data == Bt.OneListMenu["inline_keyboard"][i][j]['callback_data']:
                    await bot.send_message(call.from_user.id, '✨')
                    await bot.send_message(call.from_user.id, f'{name} ({names_dict[name]}) - {price} USD\n')


@dp.callback_query_handler(text_contains="back")
async def callback_back(call: types.CallbackQuery):
    cc_name_list = data.get_data(user_id=call.from_user.id, target='list_0')
    time = data.get_data(user_id=call.from_user.id, target='time')
    language = data.get_data(user_id=call.from_user.id, target='language')
    full_list = data.get_data(user_id=call.from_user.id, target='full_list')
    if call.data == 'back':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    elif call.data == 'back_2':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        await bot.send_message(call.from_user.id, '✨')
        await bot.send_message(call.from_user.id, f"{big_dict[language]['edit'][0]}\n{big_dict[language]['edit'][1]} "
                                                  f"{full_list}\n{big_dict[language]['edit'][2]} {time}",
                               reply_markup=Bt.SetMenu)
    elif call.data == 'back_set_list':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        await bot.send_message(call.from_user.id, '✨')
        await bot.send_message(call.from_user.id, f"{big_dict[language]['edit'][0]}\n{big_dict[language]['edit'][1]} "
                                                  f"{full_list}\n{big_dict[language]['edit'][2]} {time}",
                               reply_markup=Bt.SetMenu)
    elif call.data == 'back_set' and time != '' and full_list != '':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        cc_set_list = data.get_data(user_id=call.from_user.id, target='list')
        cc_price_list = {}
        for i in range(4):
            for j in range(4):
                name = Bt.SetListMenu["inline_keyboard"][i][j]['text']
                if name.replace('✅', '') in cc_set_list:
                    Bt.SetListMenu["inline_keyboard"][i][j]['text'] = f"{name.replace('✅', '')}✅"
                else:
                    Bt.SetListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
                name = Bt.SetListMenu["inline_keyboard"][i][j]['text']
                if name[len(name) - 1] == '✅':
                    currency = str(Bt.SetListMenu["inline_keyboard"][i][j]['callback_data'][5:])
                    price = cg.get_price(ids=currency, vs_currencies='usd')[currency]['usd']
                    cc_price_list[name.replace('✅', '')] = price
        full_list1 = ''
        for i in range(len(cc_set_list)):
            full_list1 = full_list1 + f'{cc_set_list[i]} ({names_dict[cc_set_list[i]]}) - {cc_price_list[cc_set_list[i]]} USD\n'
        await bot.send_message(call.from_user.id, full_list1)
    elif call.data == 'back_send' and cc_name_list != []:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        await bot.send_message(call.from_user.id, big_dict[language]['wait'])
        sleep(5)
        await bot.delete_message(call.from_user.id, call.message.message_id + 1)
        cc_price_list = {}
        for i in range(4):
            for j in range(4):
                name = Bt.ListMenu["inline_keyboard"][i][j]['text']
                if name[len(name) - 1] == '✅':
                    currency = str(Bt.ListMenu["inline_keyboard"][i][j]['callback_data'][5:])
                    price = cg.get_price(ids=currency, vs_currencies='usd')[currency]['usd']
                    cc_price_list[name.replace('✅', '')] = price
                    Bt.ListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
        full_list = ''
        for i in range(len(cc_name_list)):
            full_list = full_list + f'{cc_name_list[i]} ({names_dict[cc_name_list[i]]}) - {cc_price_list[cc_name_list[i]]} USD\n'
        await bot.send_message(call.from_user.id, '✨')
        await bot.send_message(call.from_user.id, full_list)
        data.clear_data(user_id=call.from_user.id, target='list_0')


@dp.callback_query_handler(text_contains="set_")
async def callback_back(call: types.CallbackQuery):
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
async def callback_back(call: types.CallbackQuery):
    language = data.get_data(user_id=call.from_user.id, target='language')
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    data.change_time(user_id=call.from_user.id, time=call.data[5:])
    full_list = data.get_data(user_id=call.from_user.id, target='full_list')
    time = data.get_data(user_id=call.from_user.id, target='time')
    await bot.send_message(call.from_user.id, '✨')
    await bot.send_message(call.from_user.id, f"{big_dict[language]['edit'][0]}\n{big_dict[language]['edit'][1]} "
                                              f"{full_list}\n{big_dict[language]['edit'][2]} {time}",
                           reply_markup=Bt.SetMenu)


@dp.callback_query_handler(text_contains="lang")
async def callback_back(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    data.change_language(user_id=call.from_user.id, language=call.data[5:])
    language = data.get_data(user_id=call.from_user.id, target='language')
    await bot.send_message(call.from_user.id, big_dict[language]['choice'])


if __name__ == '__main__':
    data.init_db()
    executor.start_polling(dp, skip_updates=True)
