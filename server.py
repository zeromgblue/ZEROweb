from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# 🔥 เปิด CORS ให้เว็บเรียกได้
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔑 ใส่ของคุณตรงนี้
LINE_TOKEN = "YRf7bE7TO57ZcNJsI62WzFy8LgRZLPG1RWOtC4LGutOZ5iyh8Ke8YI4cvPrCLqr9eQ9V49GhJ6jtcaLzhXEWQWF6aK80fxoaS9t1tGLT2HnGW0Vi9yFdD1qlDfmUb65CxTgMkQQTtBJvuKRtpylZtQdB04t89/1O/w1cDnyilFU="
USER_ID = "Ue07eb957873e60b329b23d12741b9e70"


@app.route("/send-line", methods=["POST"])
def send_line():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        message = data["message"]

        headers = {
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "to": USER_ID,
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }

        response = requests.post(
            "https://api.line.me/v2/bot/message/push",
            headers=headers,
            json=payload
        )

        print("LINE response:", response.status_code, response.text)

        return jsonify({
            "status": "sent",
            "line_status": response.status_code
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
