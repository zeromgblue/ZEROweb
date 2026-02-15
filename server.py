from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

LINE_TOKEN = os.environ.get("ToYMn1TZZR/o+0mdelmW6fJl9GRW6w55BdSJ4xTp8lh/1slo6Fy7qGBkthZYm7YNeQ9V49GhJ6jtcaLzhXEWQWF6aK80fxoaS9t1tGLT2HkMYSquQtFihXTGAQktcTF8Glxyvxd/RrXhZkCb5JfDIQdB04t89/1O/w1cDnyilFU=")
USER_ID = os.environ.get("Ue07eb957873e60b329b23d12741b9e70")

# 🔥 เก็บข้อมูลกิจกรรมล่าสุด
LATEST_ACTIVITY = {
    "name": "ยังไม่มีกิจกรรม",
    "time": "-",
    "created_at": "-"
}


@app.route("/")
def home():
    return "Bot is running 🚀"


# =========================================
# 🔵 1) เว็บเรียกเมื่อเพิ่มกิจกรรม
# =========================================
@app.route("/send-line", methods=["POST"])
def send_line():
    global LATEST_ACTIVITY

    data = request.get_json()

    activity_name = data.get("activity", "ไม่ระบุชื่อกิจกรรม")
    activity_time = data.get("time", "ไม่ระบุเวลา")

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # 🔥 อัปเดตข้อมูลล่าสุด
    LATEST_ACTIVITY = {
        "name": activity_name,
        "time": activity_time,
        "created_at": now
    }

    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    message_text = (
        f"📢 มีกิจกรรมใหม่!\n\n"
        f"📌 กิจกรรม: {activity_name}\n"
        f"⏰ เวลา: {activity_time}\n"
        f"🕒 บันทึกเมื่อ: {now}"
    )

    payload = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message_text
            }
        ]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=payload
    )

    return jsonify({"status": "sent"})


# =========================================
# 🟢 2) LINE พิมพ์มาถามสถานะระบบ
# =========================================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    events = data.get("events", [])

    for event in events:
        if event["type"] == "message" and event["message"]["type"] == "text":

            user_text = event["message"]["text"]
            reply_token = event["replyToken"]

            if "เช็คสถานะระบบตอนนี้" in user_text:

                reply_text = (
                    f"📊 สถานะระบบตอนนี้\n\n"
                    f"📌 กิจกรรมล่าสุด: {LATEST_ACTIVITY['name']}\n"
                    f"⏰ เวลา: {LATEST_ACTIVITY['time']}\n"
                    f"🕒 บันทึกเมื่อ: {LATEST_ACTIVITY['created_at']}"
                )

            else:
                reply_text = "พิมพ์ว่า 'เช็คสถานะระบบตอนนี้' เพื่อดูสถานะล่าสุด"

            headers = {
                "Authorization": f"Bearer {LINE_TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "replyToken": reply_token,
                "messages": [
                    {
                        "type": "text",
                        "text": reply_text
                    }
                ]
            }

            requests.post(
                "https://api.line.me/v2/bot/message/reply",
                headers=headers,
                json=payload
            )

    return "OK", 200


if __name__ == "__main__":
    app.run()
