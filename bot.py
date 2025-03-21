import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования для отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Используем реальный токен, который вы предоставили
BOT_TOKEN = "7413880812:AAHIMLVG9rZetPK3MtYSwnGCxO9FQd-wM6w"

# Шаблон URL для Личного кабинета клиента
WEBAPP_URL_TEMPLATE = "https://telegram-fotograf.onrender.com/?tg_id={tg_id}&first_name={first_name}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start: получает данные пользователя и отправляет сообщение с кнопкой,
    которая открывает Личный кабинет клиента через Telegram Web App.
    """
    user = update.effective_user
    if not user:
        return
    
    # Формируем URL с параметрами
    web_app_url = WEBAPP_URL_TEMPLATE.format(tg_id=user.id, first_name=user.first_name)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Открыть Личный кабинет", web_app=WebAppInfo(url=web_app_url))]
    ])
    
    await update.message.reply_text(
        "Добро пожаловать! Нажмите кнопку ниже, чтобы открыть Личный кабинет.",
        reply_markup=keyboard
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))
    # Запускаем бота (polling)
    application.run_polling()

if __name__ == '__main__':
    main()
