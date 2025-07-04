from telegram import Bot


async def send_message(chat_id, message, TELEGRAM_TOKEN):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML", pool_timeout=2000, connect_timeout = 2000, read_timeout= 2000)
