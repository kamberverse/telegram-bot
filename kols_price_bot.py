import os
import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔑 Get Bot Token from Railway Environment Variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🧠 Logging setup (for debugging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 💰 KOLS Price Function
def get_kols_price():
    try:
        url = "https://api.dexscreener.com/latest/dex/pairs/base/0xb6cffcb74c0867e126cc3d2c1e3bf290aff705d5"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        pair = data.get("pairs", [])[0]
        price_usd = float(pair["priceUsd"])

        result = (
            "💰 *KOLscan by Virtuals Live Price*\n\n"
            f"💵 USD: ${price_usd:,.7f}\n\n"
            "_Data from DexScreener_"
        )
        return result

    except Exception as e:
        logging.error(f"Error fetching price: {e}")
        return "❌ Unable to fetch KOLS price right now."

# 💬 Reusable button layout
def get_price_button():
    keyboard = [[InlineKeyboardButton("💰 Get Price", callback_data="get_price")]]
    return InlineKeyboardMarkup(keyboard)

# 🚀 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_kols_price()
    await update.message.reply_text(
        text=message,
        parse_mode="Markdown",
        reply_markup=get_price_button()
    )

# 🪄 Button click handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Stop loading animation

    if query.data == "get_price":
        message = get_kols_price()
        await query.message.reply_text(
            text=message,
            parse_mode="Markdown",
            reply_markup=get_price_button()
        )

# 🧩 Run bot
def main():
    if not BOT_TOKEN:
        print("❌ Error: BOT_TOKEN environment variable not set!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("✅ Bot is running on Railway...")
    app.run_polling()

if __name__ == "__main__":
    main()
