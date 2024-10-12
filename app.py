from flask import Flask, request, jsonify
import requests
import urllib.parse
import os
import re

app = Flask(__name__)

# Hàm xử lý webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    # Kiểm tra xem có tin nhắn mới không
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        message_text = update['message'].get('text', '')

        # Kiểm tra và xử lý liên kết
        response_text = process_message(message_text)

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

# Hàm xử lý tin nhắn
def process_message(message):
    # Tìm kiếm liên kết trong tin nhắn
    link = extract_link(message)

    if link:
        # Kiểm tra tên miền của liên kết
        if "s.shopee.vn" in link:
            final_url = get_final_link(link)
            # Tạo liên kết mới
            new_link = create_redirect_link(final_url)
            # Kết hợp văn bản gốc với liên kết mới
            return message.replace(link, new_link)
        else:
            return "Vui lòng nhập đúng link là link sản phẩm."
    else:
        return message  # Nếu không có link, trả lại tin nhắn gốc

# Hàm tạo liên kết mới
def create_redirect_link(final_url):
    # Phân tích URL và loại bỏ các tham số không cần thiết
    parsed_url = urllib.parse.urlparse(final_url)
    # Giữ lại tên miền và đường dẫn
    origin_link = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    # Tạo liên kết cuối
    result_link = f"https://shope.ee/an_redir?origin_link={urllib.parse.quote(origin_link)}&affiliate_id=17385530062&sub_id=1review"
    return result_link

# Hàm trích xuất liên kết từ tin nhắn
def extract_link(message):
    # Sử dụng regex để tìm link trong tin nhắn
    urls = re.findall(r'(https?://[^\s]+)', message)
    return urls[0] if urls else None  # Trả về liên kết đầu tiên hoặc None nếu không tìm thấy

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
