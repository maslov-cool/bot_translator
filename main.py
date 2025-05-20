# Импортируем необходимые классы.
# @translator_by_coding_lover_bot --> ник в тг
import logging
import aiohttp
from deep_translator import GoogleTranslator
from telegram.ext import Application, CommandHandler


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
BOT_TOKEN = '7929632855:AAEVmLnNRNRmiUEeQY3RhZqsrcnXZVgYXkY'

LANGUAGE_MAP = {
    'english': '🇬🇧 Английский',
    'russian': '🇷🇺 Русский',
    'german': '🇩🇪 Немецкий',
    'french': '🇫🇷 Французский',
    'spanish': '🇪🇸 Испанский',
    'italian': '🇮🇹 Итальянский',
    'portuguese': '🇵🇹 Португальский',
    'chinese': '🇨🇳 Китайский',
    'japanese': '🇯🇵 Японский',
    'korean': '🇰🇷 Корейский',
    'arabic': '🇸🇦 Арабский',
    'hindi': '🇮🇳 Хинди',
    'turkish': '🇹🇷 Турецкий',
    'ukrainian': '🇺🇦 Украинский',
    'polish': '🇵🇱 Польский',
    'romanian': '🇷🇴 Румынский',
    'dutch': '🇳🇱 Нидерландский',
    'greek': '🇬🇷 Греческий',
    'czech': '🇨🇿 Чешский',
    'swedish': '🇸🇪 Шведский',
    'finnish': '🇫🇮 Финский',
    'hungarian': '🇭🇺 Венгерский',
    'thai': '🇹🇭 Тайский'
}


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def start(update, context):
    await update.message.reply_text('''👋 Привет! Я бот-переводчик.
Помогаю переводить тексты с одного языка на другой.
    
/from_lang <язык> (по умолчанию 'russian') - это команда позволяет выбрать язык, с которого будет переводиться текст
/to_lang <язык> (по умолчанию 'english') - это команда позволяет выбрать язык, на которой будет переводиться текст
    
🌐 Поддерживаемые языки:
🇬🇧 Английский      — 'english'
🇷🇺 Русский         — 'russian'
🇩🇪 Немецкий        — 'german'
🇫🇷 Французский     — 'french'
🇪🇸 Испанский       — 'spanish'
🇮🇹 Итальянский     — 'italian'
🇵🇹 Португальский   — 'portuguese'
🇨🇳 Китайский       — 'chinese'
🇯🇵 Японский        — 'japanese'
🇰🇷 Корейский       — 'korean'
🇸🇦 Арабский        — 'arabic'
🇮🇳 Хинди           — 'hindi'
🇹🇷 Турецкий        — 'turkish'
🇺🇦 Украинский      — 'ukrainian'
🇵🇱 Польский        — 'polish'
🇷🇴 Румынский       — 'romanian'
🇳🇱 Нидерландский   — 'dutch'
🇬🇷 Греческий       — 'greek'
🇨🇿 Чешский         — 'czech'
🇸🇪 Шведский        — 'swedish'
🇫🇮 Финский         — 'finnish'
🇭🇺 Венгерский      — 'hungarian'
🇹🇭 Тайский         — 'thai'
''')


async def from_lang(update, context):
    if update.message.text.split()[1] in LANGUAGE_MAP.keys():
        context.user_data['from_lang'] = update.message.text.split()[1]
        await update.message.reply_text(f'Язык, с которого переводим успешно изменён '
                                        f'на {LANGUAGE_MAP[update.message.text.split()[1]]}')
    else:
        await update.message.reply_text(f'Некорректный формат ввода')


async def to_lang(update, context):
    if update.message.text.split()[1] in LANGUAGE_MAP.keys():
        context.user_data['to_lang'] = update.message.text.split()[1]
        await update.message.reply_text(f'Язык, на который переводим успешно изменён '
                                        f'на {LANGUAGE_MAP[update.message.text.split()[1]]}')
    else:
        await update.message.reply_text(f'Некорректный формат ввода')


async def translator(update, context):
    from_lang = context.user_data.get('from_lang', 'russian')
    to_lang = context.user_data.get('to_lang', 'english')
    text = ' '.join(update.message.text.split()[1:])

    try:
        translated = GoogleTranslator(source=from_lang, target=to_lang).translate(text)
        await update.message.reply_text(translated)
    except Exception as e:
        logger.error(f"Ошибка перевода: {e}")
        await update.message.reply_text("❌ Произошла ошибка при переводе текста.")


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчик в приложении.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("translator", translator))
    application.add_handler(CommandHandler("from_lang", from_lang))
    application.add_handler(CommandHandler("to_lang", to_lang))

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()


