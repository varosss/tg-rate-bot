import requests
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from lxml import etree


TOKEN = "TOKEN"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def api_get_rate():
    rate = []

    xml = requests.get("http://www.cbr.ru/scripts/XML_daily.asp").content
    root = etree.fromstring(xml)

    for valute in root:
        id = valute.get("ID")

        # if id in required:
        rate.append(
            {
            "nominal": valute[2].text,
            "name": valute[3].text,
            "value": round(float(".".join(valute[4].text.split(","))), 2)
            })

    return rate


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = "Привет. Введите команду /rate, чтобы узнать сегодняшний курс валют."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)


async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = api_get_rate()
    text = "Курс валют на сегодня:\n"

    for elem in rate:
        text += f"  {elem['nominal']} {elem['name']} - {elem['value']} руб.\n"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, нет такой команды")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    rate_handler = CommandHandler('rate', rate)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    app.add_handler(start_handler)
    app.add_handler(rate_handler)
    app.add_handler(unknown_handler)

    app.run_polling()
