from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)

# 🔥 เปิด CORS ให้เว็บเรียกได้
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔑 ใส่ Discord Webhook ของบลูตรงนี้
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1472595217872850945/stkj1W_jvWywvo4R_fbhK0k6fPy8JgQ-WuuTZjwAGZz6Ia7MjD6MMdrS43oUfB5kWpdJ"


@app.route("/add-task", methods=["POST"])
def add_task():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        title = data.get("title", "ไม่มีชื่อ")
        time = data.get("time", "ไม่ระบุเวลา")
        priority = data.get("priority", "ปกติ")

        embed = {
            "title": "📌 มีกิจกรรมใหม่ใน Zeroweb",
            "color": 5814783,
            "fields": [
                {
                    "name": "📝 งาน",
                    "value": title,
                    "inline": False
                },
                {
                    "name": "⏰ เวลา",
                    "value": time,
                    "inline": True
                },
                {
                    "name": "🔥 ความสำคัญ",
                    "value": priority,
                    "inline": True
                }
            ],
            "footer": {
                "text": "Zeroweb Notification System"
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"embeds": [embed]}
        )

        print("Discord response:", response.status_code, response.text)

        return jsonify({
            "status": "sent",
            "discord_status": response.status_code
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
@app.route("/notify-time", methods=["POST"])
def notify_time():
    data = request.get_json()

    title = data.get("title")
    time = data.get("time")

    embed = {
        "title": "⏰ ถึงเวลาแล้ว!",
        "color": 16711680,
        "description": f"{title}\nเวลา {time}",
        "timestamp": datetime.utcnow().isoformat()
    }

    requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]})

    return jsonify({"status": "sent"})
