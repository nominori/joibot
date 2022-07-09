from aiogram import Bot, Dispatcher, executor, types
from pycoingecko import CoinGeckoAPI
import Buttons as Bt
import config as info

bot = Bot(token=info.TOKEN)
dp = Dispatcher(bot)
cg = CoinGeckoAPI()
check, lang, check2 = '', '', ''


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global check, check2
    check, check2 = '', ''
    await bot.send_message(message.chat.id, 'Hi, I am JoiCryptoBot, I can show cryptocurrency exchange rate\n'
                                            'To know my commands and start using me, tap /commands',
                                            reply_markup=Bt.ReplyKeyboardRemove())


@dp.message_handler(commands=['commands'])
async def start_command(message: types.Message):
    global check, check2
    check, check2 = '', ''
    if lang == 'ukr':
        await bot.send_message(message.chat.id, '<b>Команди</b>\n /commands - Усі команди\n '
                                                '/language - Обрати мову\n '
                                                '/list - Cписок криптовалют', parse_mode='HTML',
                                                reply_markup=Bt.ReplyKeyboardRemove())
    elif lang == 'ru':
        await bot.send_message(message.chat.id, '<b>Команды</b>\n /commands - Все команды\n '
                                                '/language - Выбрать язык\n '
                                                '/list -Cписок криптовалют', parse_mode='HTML',
                                                reply_markup=Bt.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, '<b>Commands</b>\n /commands - All commands\n '
                                                '/language - Select Language\n '
                                                '/list - Cryptocurrency list', parse_mode='HTML',
                                                reply_markup=Bt.ReplyKeyboardRemove())


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
    callback_data = call.data
    currency = str(callback_data[3:])
    price = cg.get_price(ids=currency, vs_currencies='usd')[currency]['usd']
    if call.data == 'cc_bitcoin':
        await bot.send_message(call.from_user.id, f'BTC - {price} USD')
    elif call.data == 'cc_ethereum':
        await bot.send_message(call.from_user.id, f'ETH - {price} USD')
    elif call.data == 'cc_binancecoin':
        await bot.send_message(call.from_user.id, f'BNB - {price} USD')
    elif call.data == 'cc_litecoin':
        await bot.send_message(call.from_user.id, f'LTC - {price} USD')
    elif call.data == 'cc_dogecoin':
        await bot.send_message(call.from_user.id, f'DOGE - {price} USD')
    elif call.data == 'cc_ripple':
        await bot.send_message(call.from_user.id, f'XRP - {price} USD')
    elif call.data == 'cc_cardano':
        await bot.send_message(call.from_user.id, f'ADA - {price} USD')
    elif call.data == 'cc_solana':
        await bot.send_message(call.from_user.id, f'SOL - {price} USD')
    elif call.data == 'cc_polkadot':
        await bot.send_message(call.from_user.id, f'DOT - {price} USD')
    elif call.data == 'cc_tron':
        await bot.send_message(call.from_user.id, f'TRX - {price} USD')
    elif call.data == 'cc_chainlink':
        await bot.send_message(call.from_user.id, f'LINK - {price} USD')
    elif call.data == 'cc_near':
        await bot.send_message(call.from_user.id, f'NEAR - {price} USD')


@dp.callback_query_handler(text="back")
async def back(call: types.CallbackQuery):
    for i in range(3):
        await bot.delete_message(call.from_user.id, call.message.message_id-i)


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
        await start_command(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
