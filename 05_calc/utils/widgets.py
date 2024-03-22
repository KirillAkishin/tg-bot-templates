import telebot


calculater = telebot.types.InlineKeyboardMarkup()
calculater.row(     telebot.types.InlineKeyboardButton(" ", callback_data="no"),
                    telebot.types.InlineKeyboardButton("C", callback_data="C"),
                    telebot.types.InlineKeyboardButton("<=", callback_data="<="),
                    telebot.types.InlineKeyboardButton("/", callback_data="/") )

calculater.row(     telebot.types.InlineKeyboardButton("7", callback_data="7"),
                    telebot.types.InlineKeyboardButton("8", callback_data="8"),
                    telebot.types.InlineKeyboardButton("9", callback_data="9"),
                    telebot.types.InlineKeyboardButton("*", callback_data="*") )

calculater.row(     telebot.types.InlineKeyboardButton("4", callback_data="4"),
                    telebot.types.InlineKeyboardButton("5", callback_data="5"),
                    telebot.types.InlineKeyboardButton("6", callback_data="6"),
                    telebot.types.InlineKeyboardButton("-", callback_data="-") )

calculater.row(     telebot.types.InlineKeyboardButton("1", callback_data="1"),
                    telebot.types.InlineKeyboardButton("2", callback_data="2"),
                    telebot.types.InlineKeyboardButton("3", callback_data="3"),
                    telebot.types.InlineKeyboardButton("+", callback_data="+") )

calculater.row(     telebot.types.InlineKeyboardButton(" ", callback_data="no"),
                    telebot.types.InlineKeyboardButton("0", callback_data="0"),
                    telebot.types.InlineKeyboardButton(",", callback_data="."),
                    telebot.types.InlineKeyboardButton("=", callback_data="=") )