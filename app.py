
import os
import logging
import requests
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")


@app.get("/")
def health():
    return jsonify({
        "status": "online",
        "service": "MACD Telegram Bot 11/9/3"
    })


@app.post("/webhook")
def webhook():

    if WEBHOOK_SECRET and request.args.get("secret") != WEBHOOK_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return jsonify({"error": "Telegram credentials missing"}), 500

    data = request.get_json(silent=True)

    if isinstance(data, dict):
        message = str(data.get("message", "Alerta MACD recebido"))
    else:
        message = request.get_data(as_text=True) or "Alerta MACD recebido"

    text = "📊 MACD FOREX 11/9/3\n" + message

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        },
        timeout=15
    )

    if not response.ok:
        logging.error("Telegram error: %s", response.text)
        return jsonify({"error": "Telegram send failed"}), 502

    return jsonify({"status": "sent"})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "10000"))
    )
