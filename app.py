from flask import Flask, request, jsonify
import requests
import urllib.parse
import os

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

# Hàm lấy link cuối cùng từ URL
def get_final_link(link):
    try:
        # Gửi yêu cầu để lấy link cuối
        response = requests.get(link, allow_redirects=True)
        return response.url  # Trả về link cuối cùng
    except requests.exceptions.RequestException as e:
        return str(e)  # Trả về lỗi nếu có

# Hàm xử lý liên kết
def process_link(link):
    # Lấy link cuối cùng
    final_url = get_final_link(link)

    # Phân tích URL và loại bỏ các tham số không cần thiết
    parsed_url = urllib.parse.urlparse(final_url)

    # Tạo lại link với tên miền
    origin_link = f"https://shopee.vn{parsed_url.path}"
    
    # Mã hóa lại link
    encoded_origin_link = urllib.parse.quote(origin_link)

    # Tạo liên kết cuối
    result_link = f"https://shope.ee/an_redir?origin_link={encoded_origin_link}&affiliate_id=17385530062&sub_id=1review"
    
    return result_link

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
