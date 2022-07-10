from aiogram import Bot, Dispatcher, executor, types
from pycoingecko import CoinGeckoAPI
import datetime
from time import sleep
import Buttons as Bt
from maintoken import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
cg = CoinGeckoAPI()
check, check2, lang, k = '', '', '', 0
cc_list, cc_list1 = [], []


@dp.message_handler(commands='start')
async def start(message: types.Message):
    global check, check2
    check, check2 = '', ''
    await bot.send_message(message.chat.id, 'Hi, I am JoiCryptoBot\n'
                                            'To know my commands and start using me, tap /about',
                                            reply_markup=Bt.ReplyKeyboardRemove())


@dp.message_handler(commands='about')
async def about(message: types.Message):
    global check, check2
    check, check2 = '', ''
    if lang == 'ukr':
        await bot.send_message(message.chat.id, 'Налаштуй мову за допомогою /language\n'
                                                'Введи /list щоб обрати потрібні криптовалюти\n'
                                                '1 клік - Вибрати\n'
                                                '2 клік - Видалити\n'
                                                '⬅️ - Повернутись назад\n'
                                                'ALL➕ - Обрати все\n'
                                                'ALL➖ - Очистити список\n'
                                                '📈 - Вивести курс\n'
                                                '/commands - Усі команди\n',
                                                reply_markup=Bt.ReplyKeyboardRemove())
    elif lang == 'ru':
        await bot.send_message(message.chat.id, 'Настройте язык с помощью /language\n'
                                                'Введи /list чтобы выбрать нужные криптовалюты\n'
                                                '1 клик – Выбрать\n'
                                                '2 клик - Удалить\n'
                                                '⬅️ - Вернуться назад\n'
                                                'ALL➕ - Выбрать все\n'
                                                'ALL➖ - Очистить список\n'
                                                '📈 - Вывести курс\n'
                                                '/commands - Все команды\n',
                                                reply_markup=Bt.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Set the language using /language\n'
                                                'Enter /list to select the desired cryptocurrencies\n'
                                                '1 click - Select\n'
                                                '2 click - Delete\n'
                                                '⬅️ - turn back\n'
                                                'ALL➕ - select all\n'
                                                'ALL➖ - clear the list\n'
                                                '📈 - display exchange rate\n'
                                                '/commands - All commands\n',
                                                reply_markup=Bt.ReplyKeyboardRemove())


@dp.message_handler(commands=['commands'])
async def commands(message: types.Message):
    global check, check2
    check, check2 = '', ''
    if lang == 'ukr':
        await bot.send_message(message.chat.id, '<b>Команди</b>\n/about - Як використовувати бота\n'
                                                '/language - Обрати мову\n'
                                                '/time - Обрати час\n'
                                                '/list - Cписок криптовалют\n', parse_mode='HTML',
                                                reply_markup=Bt.ReplyKeyboardRemove())
    elif lang == 'ru':
        await bot.send_message(message.chat.id, '<b>Команды</b>\n/about - Как использовать бота\n'
                                                '/language - Выбрать язык\n'
                                                '/time - Выбрать время\n'
                                                '/list -Cписок криптовалют\n', parse_mode='HTML',
                                                reply_markup=Bt.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, '<b>Commands</b>\n/about - How to use bot\n'
                                                '/language - Select Language\n'
                                                '/time - Choose a time\n'
                                                '/list - Cryptocurrency list\n', parse_mode='HTML',
                                                reply_markup=Bt.ReplyKeyboardRemove())


@dp.message_handler(commands='language')
async def language(message: types.Message):
    global check, check2
    await bot.delete_message(message.from_user.id, message.message_id)
    if check2 == '':
        if lang == 'ukr':
            await bot.send_message(message.chat.id, 'Оберіть мову', reply_markup=Bt.LanguageMenu)
        elif lang == 'ru':
            await bot.send_message(message.chat.id, 'Выберите язык', reply_markup=Bt.LanguageMenu)
        else:
            await bot.send_message(message.chat.id, 'Choice language', reply_markup=Bt.LanguageMenu)
        check = 'language'
        check2 = 'language'
    else:
        pass


@dp.message_handler(commands='list')
async def setlist(message: types.Message):
    global check, check2
    check, check2 = '', ''
    await bot.send_message(message.chat.id, '✨', reply_markup=Bt.ReplyKeyboardRemove())
    if lang == 'ukr':
        await bot.send_message(message.chat.id, 'Виберіть криптовалюту', reply_markup=Bt.ListMenu)
    elif lang == 'ru':
        await bot.send_message(message.chat.id, 'Выберите криптовалюту', reply_markup=Bt.ListMenu)
    else:
        await bot.send_message(message.chat.id, 'Choice cryptocurrency', reply_markup=Bt.ListMenu)


@dp.callback_query_handler(text_contains="cc_")
async def crypt(call: types.CallbackQuery):
    global k, cc_list, cc_list1
    if call.data != 'cc_all' and call.data != 'cc_remove':
        currency = str(call.data[3:])
        price = cg.get_price(ids=currency, vs_currencies='usd')[currency]['usd']
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id-1)
        for i in range(3):
            for j in range(5):
                name = Bt.ListMenu["inline_keyboard"][i][j]['text']
                if call.data == Bt.ListMenu["inline_keyboard"][i][j]['callback_data']:
                    if name[len(name)-1] == '✅':
                        k = k - 1
                        cc_list.remove(name.replace('✅', ''))
                        cc_list1.remove(price)
                        Bt.ListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
                    else:
                        k = k + 1
                        cc_list.append(name)
                        cc_list1.append(price)
                        Bt.ListMenu["inline_keyboard"][i][j]['text'] = f"{name}✅"
                    await bot.send_message(call.from_user.id, '✨', reply_markup=Bt.ReplyKeyboardRemove())
                    if lang == 'ukr':
                        await bot.send_message(call.from_user.id, 'Виберіть криптовалюту', reply_markup=Bt.ListMenu)
                    elif lang == 'ru':
                        await bot.send_message(call.from_user.id, 'Выберите криптовалюту', reply_markup=Bt.ListMenu)
                    else:
                        await bot.send_message(call.from_user.id, 'Choice cryptocurrency', reply_markup=Bt.ListMenu)
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        await bot.send_message(call.from_user.id, 'wait...')
        for i in range(3):
            for j in range(5):
                sleep(0.5)
                currency = str(Bt.ListMenu["inline_keyboard"][i][j]['callback_data'][3:])
                price = cg.get_price(ids=currency, vs_currencies='usd')[currency]['usd']
                name = Bt.ListMenu["inline_keyboard"][i][j]['text']
                if call.data == 'cc_all' and name[len(name) - 1] != '✅':
                    k = k + 1
                    cc_list.append(name)
                    cc_list1.append(price)
                    Bt.ListMenu["inline_keyboard"][i][j]['text'] = f"{name}✅"
                elif call.data == 'cc_remove' and name[len(name) - 1] == '✅':
                    k = k - 1
                    name = name.replace('✅', '')
                    cc_list.remove(name)
                    cc_list1.remove(price)
                    Bt.ListMenu["inline_keyboard"][i][j]['text'] = name
        await bot.delete_message(call.from_user.id, call.message.message_id + 1)
        await bot.send_message(call.from_user.id, '✨', reply_markup=Bt.ReplyKeyboardRemove())
        if lang == 'ukr':
            await bot.send_message(call.from_user.id, 'Виберіть криптовалюту', reply_markup=Bt.ListMenu)
        elif lang == 'ru':
            await bot.send_message(call.from_user.id, 'Выберите криптовалюту', reply_markup=Bt.ListMenu)
        else:
            await bot.send_message(call.from_user.id, 'Choice cryptocurrency', reply_markup=Bt.ListMenu)


@dp.callback_query_handler(text_contains="back")
async def crypt(call: types.CallbackQuery):
    global k, cc_list, cc_list1
    if call.data == 'back':
        for i in range(2):
            await bot.delete_message(call.from_user.id, call.message.message_id-i)
    elif call.data == 'back_send' and cc_list != []:
        for i in range(2):
            await bot.delete_message(call.from_user.id, call.message.message_id-i)
        short = ''
        for o in range(k):
            short = short + f'{cc_list[o]} - {cc_list1[o]} USD\n'
        await bot.send_message(call.from_user.id, short)
        for i in range(3):
            for j in range(5):
                name = Bt.ListMenu["inline_keyboard"][i][j]['text']
                if name[len(name) - 1] == '✅':
                    Bt.ListMenu["inline_keyboard"][i][j]['text'] = name.replace('✅', '')
        k = 0
        cc_list, cc_list1 = [], []



@dp.message_handler()
async def answer(message: types.Message):
    global check, lang, check2
    if check == 'language':
        if message.text == 'Українська🇺🇦':
            await bot.send_message(message.chat.id, 'Мова обрана🇺🇦', reply_markup=Bt.ReplyKeyboardRemove())
            lang, check, check2 = 'ukr', '', ''
        elif message.text == 'Русский🇷🇺':
            await bot.send_message(message.chat.id, 'Язык выбран🇷🇺', reply_markup=Bt.ReplyKeyboardRemove())
            lang, check, check2 = 'ru', '', ''
        elif message.text == 'English🇬🇧':
            await bot.send_message(message.chat.id, 'Language selected🇬🇧', reply_markup=Bt.ReplyKeyboardRemove())
            lang, check, check2 = 'eng', '', ''
        elif message.text == '⬅️':
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id-1)
            check, check2 = '', ''
            return
        else:
            await language(message)
        await bot.delete_message(message.from_user.id, message.message_id)
        await bot.delete_message(message.from_user.id, message.message_id-1)
        check = ''
    elif check == '':
        await commands(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
