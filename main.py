import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher, CallbackContext
import openai

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_ai_response(prompt: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hallo! Willkommen bei meinem Telegram-Bot.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    message = update.message.text.lower()
    keywords = [
        "bielefeld", "owl", "ostwestfalen-lippe", "gütersloh", "rheda-wiedenbrück", "harsewinkel", "halle (westf.)",
        "herford", "bünde", "enger", "loehne", "spenge", "höxter", "warburg", "brakel", "bad driburg", "beverungen",
        "lippe", "detmold", "lemgo", "bad salzuflen", "lage", "oerlinghausen", "minden-lübbecke", "minden",
        "bad oeynhausen", "porta westfalica", "lübbecke", "espelkamp", "paderborn", "delbrück", "büren", "bad lippspringe", "salzkotten", "plag",
        "weed", "grünes", "plug", "joint"
    ]
    
    if any(keyword in message for keyword in keywords):
        response = await get_ai_response(message)
        await update.message.reply_text(response)
        await update.message.reply_text('Besuchen Sie unsere Gruppe für mehr Informationen: https://t.me/+FRVZrWEQjkA1MDM6')

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Verfügbare Befehle:\n/start - Startet den Bot\n/help - Zeigt diese Hilfe an')

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run(port=8443)
