from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "EAAL2nVqI7XEBPiO9r5YvAdf5zeC1aw8HtCTxUpLGv56A7EObuaINQu78ZBuKBvTF6SZBApBoJCmZBcoZAHElzxRAajBtxLye2Kh8p1WElyydYhjaLOMxF7KlIwMwt7ZCA8ED5iaZBHD4DFEwx3UKZAzZCd6rqkKrWXrpvhDRPuXzZBmRl0T6PYvuSLxNn1baUW11RoLZBbyqauJqqNzKObx2tlrVaaf1GQ4G3yEwRFecXVSJf3eH0g50L9u4U2EDxtwHJWVnELATmDWPULQtf6Wl7g"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificación del token
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Token inválido", 403
    elif request.method == "POST":
        data = request.json
        print("Mensaje recibido:", data)
        return "Evento recibido", 200

if __name__ == "__main__":
    app.run(port=5000)