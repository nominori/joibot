from aiogram import Bot, Dispatcher, executor, types
from pycoingecko import CoinGeckoAPI
import logging
from time import sleep
import Buttons as Bt
from maintoken import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
cg = CoinGeckoAPI()

check_command, language = '', 'eng'
cc_name_list = []
names_dict = {'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'BNB': 'Binance Coin', 'LTC': 'Litecoin', 'DOGE': 'Dogecoin',
              'XRP': 'Ripple', 'ADA': 'Cardano', 'SOL': 'Solana', 'DOT': 'Polkadot', 'TRX': 'Tron',
              'LINK': 'Chainlink', 'NEAR': 'Near Protocol', 'MATIC': 'Polygon', 'ATOM': 'Cosmos',
              'AVAX': 'Avalanche', 'UNI': 'Uniswap'}
big_dict = {'ukr': {'about': 'Налаштуй мову за допомогою /language\nВведи /list щоб обрати потрібні криптовалюти\n'
                             '1 клік - Вибрати\n2 клік - Видалити\n⬅️ - Повернутись назад\nALL➕ - Обрати все\n'
                             'ALL➖ - Очистити список\n📈 - Вивести курс\n/commands - Усі команди\n',
                             'commands': '<b>Команди</b>\n/about - Як використовувати бота\n/language - Обрати мову\n'
                             '/list - Cписок криптовалют\n',
                    'list': 'Виберіть криптовалюту',
                    'wait': 'Почекайте 5 сек...',
                    'language': 'Оберіть мову',
                    'choice': 'Мова обрана🇺🇦'
                    },
            'rus': {'about': 'Настройте язык с помощью /language\nВведи /list чтобы выбрать нужные криптовалюты\n'
                             '1 клик – Выбрать\n2 клик - Удалить\n⬅️ - Вернуться назад\nALL➕ - Выбрать все\n'
                             'ALL➖ - Очистить список\n📈 - Вывести курс\n/commands - Все команды\n',
                             'commands': '<b>Команды</b>\n/about - Как использовать бота\n/language - Выбрать язык\n'
                             '/list - Cписок криптовалют\n',
                    'list': 'Выберите криптовалюту',
                    'wait': 'Подождите 5 сек...',
                    'language': 'Выберите язык',
                    'choice': 'Язык выбран🇷🇺'
                    },
            'eng': {'about': 'Set the language using /language\nEnter /list to select the desired cryptocurrencies\n'
                             '1 click - Select\n2 click - Delete\n⬅️ - Turn back\nALL➕ - Select all\n'
                             'ALL➖ - Clear the list\n📈 - Display exchange rate\n/commands - All commands\n',
                             'commands': '<b>Commands</b>\n/about - How to use bot\n/language - Select Language\n'
                             '/list - Cryptocurrency list\n',
                    'list': 'Choice cryptocurrency',
                    'wait': 'Wait 5 sec...',
                    'language': 'Choice language',
                    'choice': 'Language selested🇬🇧'
                    }}


@dp.message_handler(commands='start')
async def start(message: types.Message):
    global check_command
    if check_command != 'start':
        check_command = 'start'
        await message.answer('Hi, I am JoiCryptoBot\nTo know my commands and start using me, tap /about')
    else:
        await message.delete()


@dp.message_handler(commands=['about', 'commands', 'list', 'language'])
async def do(message: types.Message):
    global check_command
    commands = message.text[1:]
    await message.delete()
    if check_command != commands:
        check_command = commands
        if commands == 'list':
            await message.answer('✨')
            await message.answer(big_dict[language][check_command], reply_markup=Bt.ListMenu)
        elif commands == 'language':
            await message.answer('✨')
            await message.answer(big_dict[language][check_command], reply_markup=Bt.LanguageMenu)
        else:
            await message.answer(big_dict[language][check_command], parse_mode='HTML')


@dp.message_handler()
async def delete(message: types.Message):
    await message.delete()


@dp.callback_query_handler(text_contains="cc_")
async def callback_cc(call: types.CallbackQuery):
    global cc_name_list, check_command
    check_command = ''
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    for i in range(4):
        for j in range(4):
            name = Bt.ListMenu["inline_keyboard"][i][j]['text']
            if (call.data == 'cc_all' and name[len(name) - 1] != '✅') or \
               (call.data == Bt.ListMenu["inline_keyboard"][i][j]['callback_data'] and name[len(name)-1] != '✅'):
                cc_name_list.append(name)
                Bt.ListMenu["inline_keyboard"][i][j]['text'] = f"{name}✅"
            elif (call.data == 'cc_remove' and name[len(name) - 1] == '✅') or \
                 (call.data == Bt.ListMenu["inline_keyboard"][i][j]['callback_data'] and name[len(name)-1] == '✅'):
                cc_name_list.remove(name.replace('✅', ''))
                Bt.ListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
    await bot.send_message(call.from_user.id, '✨')
    await bot.send_message(call.from_user.id, big_dict[language]['list'], reply_markup=Bt.ListMenu)


@dp.callback_query_handler(text_contains="back")
async def callback_back(call: types.CallbackQuery):
    global cc_name_list, check_command
    check_command = ''
    if call.data == 'back':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
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
                if name[len(name)-1] == '✅':
                    currency = str(Bt.ListMenu["inline_keyboard"][i][j]['callback_data'][3:])
                    price = cg.get_price(ids=currency, vs_currencies='usd')[currency]['usd']
                    cc_price_list[name.replace('✅', '')] = price
                    Bt.ListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
        full_list = ''
        for i in range(len(cc_name_list)):
            full_list = full_list + f'{cc_name_list[i]} ({names_dict[cc_name_list[i]]}) - {cc_price_list[cc_name_list[i]]} USD\n'
        await bot.send_message(call.from_user.id, '✨')
        await bot.send_message(call.from_user.id, full_list)
        cc_name_list = []


@dp.callback_query_handler(text_contains="lang")
async def callback_back(call: types.CallbackQuery):
    global check_command, language
    check_command = ''
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    language = call.data[5:]
    await bot.send_message(call.from_user.id, big_dict[language]['choice'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
