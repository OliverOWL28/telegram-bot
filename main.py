import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_ai_response(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hallo! Willkommen bei meinem Telegram-Bot. Besuchen Sie unsere Gruppe für mehr Informationen: https://t.me/+FRVZrWEQjkA1MDM6')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    keywords = ["Bielefeld", "OWL", "Ostwestfalen-Lippe", "Gütersloh", "Herford", "Höxter", "Lippe", "Minden-Lübbecke", "Paderborn", "Plag", "weed", "Grünes", "plug", "joint"]
    if any(keyword in message.text for keyword in keywords):
        response = await get_ai_response(message.text)
        await message.reply_text(response)
        await message.reply_text('Besuchen Sie unsere Gruppe für mehr Informationen: https://t.me/+FRVZrWEQjkA1MDM6')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Verfügbare Befehle:\n/start - Startet den Bot\n/help - Zeigt diese Hilfe an')

async def test_openai_api(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Test message",
            max_tokens=5
        )
        await update.message.reply_text(f"OpenAI API funktioniert! Antwort: {response.choices[0].text.strip()}")
    except Exception as e:
        await update.message.reply_text(f"Fehler bei der Nutzung der OpenAI API: {e}")

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    print(f"Verwendeter Token: {token}")  # Zeile zur Ausgabe des Tokens hinzufügen
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test_openai", test_openai_api))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
