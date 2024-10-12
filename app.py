from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests
import os
import re
import urllib.parse

app = Flask(__name__)

# Đăng ký token bot Telegram
TELEGRAM_TOKEN = os.getenv("7725120534:AAF_NpkDpwYx0b3ritpvvjM3LbaUPayvlCA")  # Đặt token bot từ biến môi trường

# Khởi tạo bot
async def start(update: Update, context):
    await update.message.reply_text("Chào! Gửi văn bản chứa các liên kết Shopee để tôi tạo link cho bạn.")

async def handle_message(update: Update, context):
    text = update.message.text
    if not text:
        await update.message.reply_text("Vui lòng gửi văn bản chứa các liên kết!")
        return

    links = re.findall(r'(https?://(?:vn\.shp\.ee|s\.shopee\.vn)/[^\s]+)', text)
    results = text

    if not links:
        await update.message.reply_text("Không tìm thấy liên kết hợp lệ.")
        return

    for link in links:
        full_link = resolve_short_link(link)
        if not full_link:
            continue
        encoded_link = encode_link(full_link)
        new_link = f"https://shope.ee/an_redir?origin_link={encoded_link}&affiliate_id=17305270177&sub_id=huong"
        results = results.replace(link, new_link)

    await update.message.reply_text(results)

# Hàm để mã hóa URL
def encode_link(link):
    base_url = link.split('?')[0]  
    return urllib.parse.quote(base_url, safe='')

# Hàm để giải mã liên kết rút gọn thành liên kết đầy đủ
def resolve_short_link(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        return response.url
    except requests.RequestException:
        return None

# Khởi tạo bot Telegram
def init_bot():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application

@app.route('/')
def index():
    return "Bot Telegram đang hoạt động!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    bot.process_new_updates([update])
    return "OK"

if __name__ == '__main__':
    bot = init_bot()  # Khởi tạo bot Telegram
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
