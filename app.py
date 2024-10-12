from flask import Flask, request, jsonify
import urllib.parse

app = Flask(__name__)

@app.route('/generate_links', methods=['POST'])
def generate_links():
    data = request.get_json()
    links = data.get('links', [])
    
    results = []
    for link in links:
        encoded_link = urllib.parse.quote(link)
        new_link = f"https://shope.ee/an_redir?origin_link={encoded_link}&affiliate_id=17385530062&sub_id=1review"
        results.append(new_link)
    
    return jsonify({"links": results})

@app.route('/webhook', methods=['POST'])
def webhook():
    # Xử lý dữ liệu webhook từ Telegram
    update = request.get_json()
    # (Thêm logic xử lý cập nhật tại đây)
    
    # Trả về một phản hồi OK
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
