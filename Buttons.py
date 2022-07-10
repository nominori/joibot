from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
                          KeyboardButton, ReplyKeyboardRemove
LanguageButton1 = KeyboardButton('Українська🇺🇦')
LanguageButton2 = KeyboardButton('Русский🇷🇺')
LanguageButton3 = KeyboardButton('English🇬🇧')
Main = KeyboardButton('⬅️')
LanguageMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(LanguageButton1, LanguageButton2, LanguageButton3, Main)

Button1 = InlineKeyboardButton(text="BTC", callback_data='cc_bitcoin')
Button2 = InlineKeyboardButton(text="ETH", callback_data='cc_ethereum')
Button3 = InlineKeyboardButton(text="BNB", callback_data='cc_binancecoin')
Button4 = InlineKeyboardButton(text="LTC", callback_data='cc_litecoin')
Button5 = InlineKeyboardButton(text="DOGE", callback_data='cc_dogecoin')
Button6 = InlineKeyboardButton(text="XRP", callback_data='cc_ripple')
Button7 = InlineKeyboardButton(text="ADA", callback_data='cc_cardano')
Button8 = InlineKeyboardButton(text="SOL", callback_data='cc_solana')
Button9 = InlineKeyboardButton(text="DOT", callback_data='cc_polkadot')
Button10 = InlineKeyboardButton(text="TRX", callback_data='cc_tron')
Button11 = InlineKeyboardButton(text="LINK", callback_data='cc_chainlink')
Button12 = InlineKeyboardButton(text="NEAR", callback_data='cc_near')
Button13 = InlineKeyboardButton(text="MATIC", callback_data='cc_matic-network')
Button14 = InlineKeyboardButton(text="AVAX", callback_data='cc_avalanche-2')
Button15 = InlineKeyboardButton(text="ATOM", callback_data='cc_cosmos')
ButtonBack = InlineKeyboardButton(text="⬅️", callback_data='back')
ButtonSend = InlineKeyboardButton(text="📈", callback_data='back_send')
ListMenu = InlineKeyboardMarkup(row_width=5).add(Button1, Button2, Button3, Button4, Button5,
                                                 Button6, Button7, Button8, Button9, Button10,
                                                 Button11, Button12, Button13, Button14, Button15,
                                                 ButtonBack, ButtonSend)
