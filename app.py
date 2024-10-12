from flask import Flask, request, jsonify
import urllib.parse

app = Flask(__name__)

@app.route('/generate_links', methods=['POST'])
def generate_links():
    # Lấy dữ liệu từ yêu cầu POST
    data = request.get_json()
    links = data.get('links', [])
    
    # Xử lý và tạo link mới
    results = []
    for link in links:
        # Mã hóa link
        encoded_link = urllib.parse.quote(link)
        # Tạo link mới
        new_link = f"https://shope.ee/an_redir?origin_link={encoded_link}&affiliate_id=17385530062&sub_id=1review"
        results.append(new_link)
    
    return jsonify({"links": results})

if __name__ == '__main__':
    app.run(debug=True)
