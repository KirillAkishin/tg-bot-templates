commands = [
    '/start',
    '/help',
    '/settings',
    '/rules',
    '/users',
    '/user',
    '/roles',
    '/role',
    '/groups',
    '/group',
    '/id',
    '/test',
    '/demoted2user',
    '/demoted2moder',
    '/promote2vip',
    '/promote2moder',
    '/promote2admin',
    '/ban',
    '/admin'
]

blanks = {
    'help': (
        'Демонстрационный мок-бот.\n\n' + 
        f"Команды:\n  {',\n  '.join(commands)}.\n\n" +
        'Вы также можете отправлять:\n  текст,\n  gif-файлы,\n  стикеры,\n  видео,\n  картинки.\n\n' +
        'Обрабатываемые ошибки:\n  невалидные команды,\n  некоторые форматы сообщений.' ),
    'rules': '\n    '.join(['[RULES]',
                            '1. The Admin is always right.',
                            '2. If Admin is wrong, see rule №1.' ]),
    'start': 'Do you accept the /rules?\n[enter "yes" to continue]',
    'repeated_start': 'Вам не надо проходить повторную регистрацию.',
    'settings': 'Выберите желаемые настройки.',
    'cmd_unknown': 'Такой команды нет.\n/help',
    'msg_unknown': 'Формат сообщения не поддерживается.\n/help',
    'error_nouser': 'Ошибка. Пользователь {user} не найден.',
    'error_request': 'Ошибка. Некорректный формат запроса.',
    'processing': 'Обработка запроса.',
}
blanks['start'] = blanks['start'].format(rules=blanks['rules']) 

gif_ids = {
    'common': {
        'wow': 'CgACAgQAAxkBAAIHVWYISGgK7W9ZVcbm-Ls3oY-kraMRAAJ0BAACcIAsUGjd0cICyOuqNAQ',
        'wow_malfoy': 'CgACAgIAAxkBAAIHcWYIUBAGI_6cqj_via1ZOHXlTISeAAK0NAACFDjYSR7PkZtaJ0TtNAQ',
        'wow_malfoy_2': 'CgACAgIAAxkBAAIHdWYIUHMTWzudtzX8kbCHmnQXciCgAALMBAACGuSpS2T07NrRBirrNAQ',
        'amaze': 'CgACAgIAAxkBAAIHd2YIUKAhdo6NOeUC0ZtYiCSstmAQAAK0FAACL13wSllm6pDq8OH8NAQ',
        'dog': 'CgACAgIAAxkBAAIHZ2YITmaZb_7CNOVHKeFkEK5f3nTlAAJ9EQACM_hBS5gwuzk6uoQfNAQ',
        'fucku': 'CgACAgIAAxkBAAIHa2YITwt9Wk7eflAuRYfdJd3gJmobAALWMQACop_ASl6EgaNziH1LNAQ',
        'cat_no': 'CgACAgQAAxkBAAIHc2YIUE0hFSTIcGmqr3CH2pVjrVPNAAJXAwACILF9U41-kC9qvY08NAQ',
        'cat_reply': 'CgACAgQAAxkBAAIHeWYIUOVdtRTQWoP4Qqwumzx9FuwMAAIiAwACHRMMU4vLGaV3dSz0NAQ',
        'cat_hello': 'CgACAgIAAxkBAAIHY2YIS49Y8lJ4aJtw7u4LU6M32HiHAAIPEgACONoRS42LgQX-Ai6PNAQ',
        'cat_asleep': 'CgACAgQAAxkBAAIHbWYIT1pssThmAeBzjc5VfvsaNBzTAAKQFgACJh5kBy3lsIngPajsNAQ',
        'cat_shutdown': 'CgACAgIAAxkBAAIHb2YIT4ByqDDiY2ZOWG6oNP2hZVq_AALkDgAC9RbpSFyNG5tSsiJyNAQ',
        'taking_notes': 'CgACAgQAAxkBAAIHg2YIU0jsL-YdJFF-D4DcQoTbm5SBAAIwAwACrA8NU8Uh0JBGwj5dNAQ',
    },
    'reply': {
        'nuthouse': 'CgACAgIAAxkBAAIHhWYIU04Pdq5H-eaZ1Wt21mTyJb_yAAK4AgACUT_xSZftvYVWrys8NAQ',
        'ape_nods': 'CgACAgIAAxkBAAIHgWYIUzO_iFdWJ9G142TdCXC57lvMAAIjJwAC6CI5SpO583nsRHHUNAQ',
        'bale_nods_1': 'CgACAgIAAxkBAAIHiWYIVWj3D6swsP1uGTMtFGjakwu7AAJJFQACZHXhSvucoeFK_XQ9NAQ',
        'bale_nods_2': 'CgACAgIAAxkBAAIHi2YIVXjyDv09DPl1PDwZmU6il2D5AAIuGQACw3NhSkG59ebuCbq-NAQ',
        'bale_smile': 'CgACAgQAAxkBAAIHf2YIUl-yHZ_GTjzeI1zeBPh7Qul1AAKZAQACGN4MUDrIVTTKEp9vNAQ',
    },
}

pic_ids = {
    'common': {
        'nietzsche': 'AgACAgIAAxkBAAIJSWYKPWKi1ho7Rt2VL6UWGstxaCpeAAKe2DEbZslYSL0avUCVcVOOAQADAgADeQADNAQ',
        'psa_popierdolilo': 'AgACAgIAAxkBAAIJaWYKQ4j83LNcRTHy37Bo38Hq-P3-AAKx2DEbZslYSKpup4Nbtzx1AQADAgADeAADNAQ',
        'kota_tez_pojebalo': 'AgACAgIAAxkBAAIJa2YKQ5eOqgUGuJwkxO0xKsdyiIdhAAKy2DEbZslYSEH3HXR96qlJAQADAgADeQADNAQ',
        'cat_smalltalk': 'AgACAgIAAxkBAAIJVmYKQeuXbRRtpRuRhgjp-5w65ayOAAKq2DEbZslYSOB52uwT2OBJAQADAgADeQADNAQ',
        'lonely_faggot': 'AgACAgIAAxkBAAIJZ2YKQuMT_ogHiCyR57fHZ3H9L8MFAAKu2DEbZslYSBJm1g1gARDAAQADAgADeAADNAQ',
    },
    'reply': {
        'robocop': 'AgACAgIAAxkBAAIJUmYKQIY5FjTraIPUSE8up_vIN8tHAAKm2DEbZslYSKNxgAbSWN5RAQADAgADeAADNAQ',
        'angry_dog': 'AgACAgIAAxkBAAIJVGYKQdLNqiAGg0T9SQ1BgiHCITXDAAKp2DEbZslYSI0-4-CpAbopAQADAgADeAADNAQ',
    },
}


video_ids = {
    'common': {
        'bukin_dance': 'BAACAgIAAxkBAAIJmmYKRv-D_UgXXZRX9hRXr6lSyz8NAAKgQgACZslYSBMOLGnc6l5LNAQ',
    },
    'reply': {
        'dog_moo': 'BAACAgIAAxkBAAIJomYKSB2fyH1vPOglyZniS46N9S6eAAKpQgACZslYSMHILl60aFkwNAQ',
        'fox': 'BAACAgIAAxkBAAIJpGYKSFtl9yeO2kZkETIrc2iVx7gLAAKtQgACZslYSGOmNG5BwCYwNAQ',
        'roar': 'BAACAgIAAxkBAAIJpmYKSHd_4O82b7e4q6Bt-AyWK5GqAAKvQgACZslYSLiuEM2dAaWDNAQ',
        'parrot_instagram': 'BAACAgIAAxkBAAIJqGYKSJpYnnOrcf6B2Q_RRaWM6LbBAAKxQgACZslYSPMfYTOscKsYNAQ',
        'rabbit_lotr': 'BAACAgIAAxkBAAIJqmYKSPCc33yZY3fw2-MfSR8YzS1CAAK0QgACZslYSPqlxlN5s0TVNAQ',
        'squirrel': 'BAACAgIAAxkBAAIJrGYKSSMF0Nf3TgIYZpWTNPos8F1VAAK2QgACZslYSEL-poGr_hF-NAQ',
        'deer_screamer': 'BAACAgIAAxkBAAIJrmYKSWIyIMfkm6zfScZDdg6hyNwZAAK9QgACZslYSKCc1E_WyLEzNAQ',
        'cat_dogs_tv': 'BAACAgIAAxkBAAIJsGYKSaeKwi0OKrDLrwgpbXZNCnugAAK-QgACZslYSPo5gJXFbxnINAQ',
        'cat_dog_wtf': 'BAACAgIAAxkBAAIJsmYKSddJTp1SMilK5XmncOMmjakkAALAQgACZslYSBogvdndLkVoNAQ',
    },
}

sticker_ids = {
    'common': {},
    'reply': {
        'joker_monkey': 'CAACAgIAAxkBAAIJw2YKS8WJ3VrWMSCLJ0OUiKX3f5iSAALNJwACg_i5S4AzvwZ8JVk7NAQ',
    },
}