from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ====== НАСТРОЙКИ ======
# Вставь сюда свой токен группы и confirmation code
TOKEN = "vk1.a.Mzth4c-0Az7WG2RmHJWl0-6P_Kl64t4FjkksO7O-p7Gf4ePHgdfB90chgpp2ZOfaqACSjMzbSMjsZ5uXvL9o2X6QPOUNcFjiILPR6FpfWriFgWSveJ2fLNuFr68xB3TloklAXgWuedsK7Nt_H8x_tk4iq5PVVnueYLyKhFu1iR_uEPOhHqb3nyUPjvAkQ1cvnl6zxIKQoxxP95ZCJKAW8A"
CONFIRMATION_CODE = "6046c9fa"

def send_message(user_id, text):
    """Отправляет сообщение через VK API"""
    url = "https://api.vk.com/method/messages.send"
    params = {
        "user_id": user_id,
        "message": text,
        "access_token": TOKEN,
        "v": "5.199",
        "random_id": 0
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return None

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print(f"📩 Получено событие: {data}")

    # 1. Подтверждение сервера
    if data.get("type") == "confirmation":
        return CONFIRMATION_CODE

    # 2. Обработка нового сообщения
    if data.get("type") == "message_new":
        msg = data["object"]["message"]
        user_id = msg["from_id"]
        text = msg.get("text", "").lower()

        if text == "/start":
            send_message(user_id, "👋 Привет! Я бот на Callback API. Напиши что-нибудь, и я отвечу.")
        else:
            send_message(user_id, f"📩 Ты написал: {text}")

    return jsonify({"response": "ok"})

if __name__ == "__main__":
    app.run()
