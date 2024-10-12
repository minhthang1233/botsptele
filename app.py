from flask import Flask, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

# Hàm xử lý webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    # Kiểm tra xem có tin nhắn mới không
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        message_text = update['message'].get('text', '')

        # Gọi hàm để xử lý liên kết
        response_text = process_link(message_text)

        # Gửi phản hồi về Telegram
        send_message(chat_id, response_text)

    return jsonify({"status": "ok"})

# Hàm gửi tin nhắn đến bot Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot7725120534:AAF_NpkDpwYx0b3ritpvvjM3LbaUPayvlCA/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

# Hàm xử lý liên kết
def process_link(link):
    # Mã hóa liên kết
    encoded_link = urllib.parse.quote(link)
    
    # Tạo liên kết cuối
    final_link = f"https://shope.ee/an_redir?origin_link={encoded_link}&affiliate_id=17385530062&sub_id=1review"
    
    return final_link

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
