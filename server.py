from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔐 ดึงค่าจาก Environment Variables
LINE_TOKEN = os.getenv("ToYMn1TZZR/o+0mdelmW6fJl9GRW6w55BdSJ4xTp8lh/1slo6Fy7qGBkthZYm7YNeQ9V49GhJ6jtcaLzhXEWQWF6aK80fxoaS9t1tGLT2HkMYSquQtFihXTGAQktcTF8Glxyvxd/RrXhZkCb5JfDIQdB04t89/1O/w1cDnyilFU=")
USER_ID = os.getenv("Ue07eb957873e60b329b23d12741b9e70")


@app.route("/", methods=["GET"])
def home():
    return "Server is running!"


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

        return jsonify({
            "status": "sent",
            "line_status": response.status_code,
            "line_response": response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
