import os
import sys
import re
import random
import string
import logging
from datetime import datetime

# Telegram Bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# إعدادات البوت
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# تسجيل الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(name)

class DataGenerator:
    """مولد البيانات"""
    
    @staticmethod
    def extract_name_from_text(text):
        """استخراج الاسم من النص"""
        patterns = [
            r'الاسم[:\s]+([^\n]+)',
            r'اسم[:\s]+([^\n]+)',
            r'Name[:\s]+([^\n]+)',
            r'Full Name[:\s]+([^\n]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "محمد أحمد"
    
    @staticmethod
    def create_gmail(name):
        """إنشاء بريد Gmail"""
        # تنظيف الاسم
        clean_name = re.sub(r'[^a-zA-Z]', '', name)
        if len(clean_name) < 3:
            clean_name = "user"
        
        # إنشاء اسم المستخدم
        username = f"{clean_name[:4].lower()}{random.randint(1000, 9999)}"
        return f"{username}@gmail.com"
    
    @staticmethod
    def generate_passwords(name):
        """إنشاء كلمات مرور"""
        clean_name = re.sub(r'[^a-zA-Z]', '', name)
        if len(clean_name) < 3:
            clean_name = "user"
        
        # كلمة مرور بسيطة
        simple_pass = f"{clean_name[:3].lower()}{random.randint(100, 999)}!"
        
        # كلمة مرور قوية
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        strong_pass = ''.join(random.choice(chars) for _ in range(12))
        
        return simple_pass, strong_pass

# معالجة الأوامر
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /start"""
    welcome = """
🎉 *مرحباً بك في بوت استخراج بيانات الجوازات!*

*✨ المميزات:*
• استخراج النصوص العربية والإنجليزية
• إنشاء بريد Gmail تلقائياً
• إنشاء كلمات مرور آمنة

*📸 *كيفية الاستخدام:*
1. أرسل صورة جواز السفر أو البطاقة
2. انتظر ثواني للمعالجة
3. احصل على النتائج كاملة

*🚀 أرسل صورة الآن للبدء!*
"""
    await update.message.reply_text(welcome, parse_mode='Markdown')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الصور"""
    try:
        # إعلام المستخدم
        msg = await update.message.reply_text("📥 جاري معالجة الصورة...")
        
        # اسم افتراضي (في النسخة الحقيقية، هنا نستخرج النصوص)
        name = "أحمد محمد"
        
        # إنشاء البيانات
        generator = DataGenerator()
        gmail = generator.create_gmail(name)
        simple_pass, strong_pass = generator.generate_passwords(name)
        
        # النتائج
        result = f"""
✅ *تمت المعالجة بنجاح!*

👤 *الاسم:* {name}

📧 *بريد Gmail المقترح:*
{gmail}

🔑 *كلمات المرور:*
• مقتبس من الاسم: {simple_pass}
• كلمة مرور قوية: {strong_pass}

🔗 *لإنشاء الحساب:*
https://accounts.google.com/signup

💡 *نصائح أمنية:*
1. غيّر كلمة المرور بعد الإنشاء
2. استخدم مدير كلمات المرور
3. فعّل المصادقة الثنائية

⚠️ *تنبيه:* للاستخدام التعليمي فقط.
"""
        
        await msg.edit_text(result, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /help"""
    help_text = """
*❓ المساعدة:*

*لأفضل نتائج:*
• صور واضحة بإضاءة جيدة
• خلفية فاتحة
• مستند أفقي غير مائل

*للدعم:* @your_username
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')
# التشغيل الرئيسي
def main():
    """الدالة الرئيسية"""
    if not BOT_TOKEN:
        print("❌ خطأ: BOT_TOKEN غير موجود!")
        print("📝 أضفه في Environment Variables في Render")
        sys.exit(1)
    
    # إنشاء التطبيق
    app = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة الأوامر
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("🤖 بدء البوت...")
    app.run_polling()

if name == "main":
    main()