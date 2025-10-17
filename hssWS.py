import requests

# Configuración de la API de WhatsApp (Meta)
ACCESS_TOKEN = "EAAL2nVqI7XEBPiO9r5YvAdf5zeC1aw8HtCTxUpLGv56A7EObuaINQu78ZBuKBvTF6SZBApBoJCmZBcoZAHElzxRAajBtxLye2Kh8p1WElyydYhjaLOMxF7KlIwMwt7ZCA8ED5iaZBHD4DFEwx3UKZAzZCd6rqkKrWXrpvhDRPuXzZBmRl0T6PYvuSLxNn1baUW11RoLZBbyqauJqqNzKObx2tlrVaaf1GQ4G3yEwRFecXVSJf3eH0g50L9u4U2EDxtwHJWVnELATmDWPULQtf6Wl7g"  # Reemplazar con tu token real
PHONE_NUMBER_ID = "812406141963723"  # Reemplazar con tu ID de número
RECIPIENT_PHONE = "826666166538472"  # Número del cliente en formato internacional

# Endpoint de la API
url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

# Encabezados HTTP
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Personalización del mensaje
mensaje = "¡Gracias por contactarnos! ¿En qué podemos ayudarte hoy?"

# Cuerpo del mensaje
data = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE,
    "type": "text",
    "text": {
        "body": mensaje
    }
}

# Envío del mensaje y manejo de errores
try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print("✅ Mensaje enviado correctamente.")
    print("📨 Respuesta del servidor:", response.json())
except requests.exceptions.HTTPError as errh:
    print("❌ Error HTTP:", errh)
except requests.exceptions.ConnectionError as errc:
    print("❌ Error de conexión:", errc)
except requests.exceptions.Timeout as errt:
    print("❌ Error de tiempo de espera:", errt)
except requests.exceptions.RequestException as err:
    print("❌ Error inesperado:", err)