import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Загружаем секретные ключи
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Проверяем ключи
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("❌ ОШИБКА: Проверьте файл .env")
    exit()

# Настраиваем Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Привет! Я бот с Gemini AI!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💡 Просто напиши мне сообщение!")

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        await update.message.chat.send_action(action="typing")
        print(f"👤 Запрос: {user_message}")
        
        response = model.generate_content(user_message)
        
        if response.text:
            await update.message.reply_text(f"🤖 {response.text}")
            print("✅ Ответ отправлен!")
        else:
            await update.message.reply_text("🤔 Не получилось сгенерировать ответ")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        await update.message.reply_text("😔 Ошибка. Попробуйте другой запрос.")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    print("🚀 Бот запущен на GitHub Codespaces!")
    print("📱 Напишите /start в Telegram")
    application.run_polling()

if __name__ == "__main__":
    main()
