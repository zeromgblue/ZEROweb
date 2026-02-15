from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 🔐 ดึง Webhook จาก Environment Variable
DISCORD_WEBHOOK_URL = os.environ.get("https://discordapp.com/api/webhooks/1472595217872850945/stkj1W_jvWywvo4R_fbhK0k6fPy8JgQ-WuuTZjwAGZz6Ia7MjD6MMdrS43oUfB5kWpdJ")


def send_embed(embed_data):
    if not DISCORD_WEBHOOK_URL:
        print("Webhook not set")
        return

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"embeds": [embed_data]}
        )
        print("Discord response:", response.status_code)
    except Exception as e:
        print("Discord Error:", e)


# ===============================
# เพิ่ม Task
# ===============================

@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    title = data.get("title", "ไม่มีชื่อ")
    time_value = data.get("time", "ไม่ระบุเวลา")
    priority = data.get("priority", "ปกติ")

    embed = {
        "title": "📌 มีกิจกรรมใหม่ใน Zeroweb",
        "color": 5814783,
        "fields": [
            {"name": "📝 งาน", "value": title, "inline": False},
            {"name": "⏰ เวลา", "value": time_value, "inline": True},
            {"name": "🔥 ความสำคัญ", "value": priority, "inline": True}
        ],
        "footer": {"text": "Zeroweb Notification System"},
        "timestamp": datetime.utcnow().isoformat()
    }

    send_embed(embed)

    return jsonify({"status": "sent"})


# ===============================
# แจ้งเตือนเมื่อถึงเวลา
# ===============================

@app.route("/notify-time", methods=["POST"])
def notify_time():
    data = request.get_json()

    title = data.get("title", "ไม่มีชื่อ")
    time_value = data.get("time", "ไม่ระบุเวลา")

    embed = {
        "title": "⏰ ถึงเวลาแล้ว!",
        "color": 16711680,
        "description": f"{title}\nเวลา {time_value}",
        "timestamp": datetime.utcnow().isoformat()
    }

    send_embed(embed)

    return jsonify({"status": "sent"})


# ===============================
# Health Check (ไว้เช็คระบบ)
# ===============================

@app.route("/")
def home():
    return jsonify({"status": "Zeroweb Backend Online"})


# ===============================
# Run (รองรับ Render)
# ===============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
import requests
import os

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route("/test-discord")
def test_discord():
    data = {
        "content": "🔥 TEST MESSAGE FROM RENDER"
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    return {
        "status_code": response.status_code,
        "response_text": response.text
    }

