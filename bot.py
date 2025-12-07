import os
import re
import tweepy
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Load environment variables from Railway
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")          # string for public group
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Twitter/X Credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Setup Twitter client
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Print chat ID to check
    print("Chat ID:", update.message.chat_id)

    # Only process messages from your target Telegram group
# if update.message.chat.username != TELEGRAM_GROUP_ID.replace("@", ""):
 # return

    text = update.message.text

    # Extract ONLY numbers
    numbers = re.findall(r"\d+", text)
    if not numbers:
        return

    numbers_joined = ", ".join(numbers)

    # Format message
    final_message = f"Alert: {numbers_joined}"

    # Send to Twitter
    try:
        twitter_api.update_status(final_message)
    except Exception as e:
        print("Twitter error:", e)

    # Send to Telegram channel
    try:
        await context.bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=final_message)
    except Exception as e:
        print("Telegram channel error:", e)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

