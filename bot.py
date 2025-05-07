import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY   = os.environ["OPENAI_API_KEY"]
MODEL            = "gpt-4o-mini"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("🔥 Nova is online! How can I assist you today?")

def echo(update, context):
    prompt = update.message.text
    openai.api_key = OPENAI_API_KEY
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    reply = resp.choices[0].message.content.strip()
    update.message.reply_text(reply)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # ─── Webhook server ────────────────────────────────────
    updater.start_webhook(
        listen="0.0.0.0",      # bind on all interfaces
        port=10000,            # match the port we expose
        url_path=TELEGRAM_TOKEN
    )
    updater.bot.set_webhook(f"https://{RENDER_EXTERNAL_URL}/{TELEGRAM_TOKEN}")
    updater.idle()


if __name__ == "__main__":
    main()
