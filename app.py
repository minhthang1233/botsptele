from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Token bot Telegram lấy từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

# Route để Telegram gửi dữ liệu webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # Xử lý tin nhắn của người dùng
        response_message = f"Bạn đã gửi: {text}"

        # Gửi lại phản hồi cho người dùng thông qua Telegram API
        send_message(chat_id, response_message)

    return "ok", 200

# Hàm gửi tin nhắn thông qua Telegram API
def send_message(chat_id, text):
    url = TELEGRAM_API_URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
