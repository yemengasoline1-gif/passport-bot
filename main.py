import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context):
    await update.message.reply_text("✅ البوت يعمل!")

async def photo(update: Update, context):
    result = """
✅ *تم استلام صورتك!*

📧 *بريد Gmail:* test123@gmail.com
🔑 *كلمة المرور:* Pass123!

🔗 *لإنشاء الحساب:*
https://accounts.google.com/signup
"""
    await update.message.reply_text(result, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo))
    app.run_polling()

if name == "main":
    main()
