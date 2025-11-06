# TODO


import telebot


calc_inline = telebot.types.InlineKeyboardMarkup()
calc_inline.row(    telebot.types.InlineKeyboardButton(" ", callback_data="no"),
                    telebot.types.InlineKeyboardButton("C", callback_data="C"),
                    telebot.types.InlineKeyboardButton("<=", callback_data="<="),
                    telebot.types.InlineKeyboardButton("/", callback_data="/") )
calc_inline.row(    telebot.types.InlineKeyboardButton("7", callback_data="7"),
                    telebot.types.InlineKeyboardButton("8", callback_data="8"),
                    telebot.types.InlineKeyboardButton("9", callback_data="9"),
                    telebot.types.InlineKeyboardButton("*", callback_data="*") )
calc_inline.row(    telebot.types.InlineKeyboardButton("4", callback_data="4"),
                    telebot.types.InlineKeyboardButton("5", callback_data="5"),
                    telebot.types.InlineKeyboardButton("6", callback_data="6"),
                    telebot.types.InlineKeyboardButton("-", callback_data="-") )
calc_inline.row(    telebot.types.InlineKeyboardButton("1", callback_data="1"),
                    telebot.types.InlineKeyboardButton("2", callback_data="2"),
                    telebot.types.InlineKeyboardButton("3", callback_data="3"),
                    telebot.types.InlineKeyboardButton("+", callback_data="+") )
calc_inline.row(    telebot.types.InlineKeyboardButton(" ", callback_data="no"),
                    telebot.types.InlineKeyboardButton("0", callback_data="0"),
                    telebot.types.InlineKeyboardButton(",", callback_data="."),
                    telebot.types.InlineKeyboardButton("=", callback_data="=") )

calc_reply = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
calc_reply.row(     telebot.types.KeyboardButton("7"),
                    telebot.types.KeyboardButton("8"),
                    telebot.types.KeyboardButton("9"),
                    telebot.types.KeyboardButton("*") )
calc_reply.row(     telebot.types.KeyboardButton(text="4"),
                    telebot.types.KeyboardButton(text="5"),
                    telebot.types.KeyboardButton(text="6"),
                    telebot.types.KeyboardButton(text="/") )
calc_reply.row(     telebot.types.KeyboardButton(text="4"),
                    telebot.types.KeyboardButton(text="5"),
                    telebot.types.KeyboardButton(text="6"),
                    telebot.types.KeyboardButton(text="-") )
calc_reply.row(     telebot.types.KeyboardButton(text="0"),
                    telebot.types.KeyboardButton(text="."),
                    telebot.types.KeyboardButton(text="="),
                    telebot.types.KeyboardButton(text="+") )

keyboard_rm = telebot.types.ReplyKeyboardRemove()
