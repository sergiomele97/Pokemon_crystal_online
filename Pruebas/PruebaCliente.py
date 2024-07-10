import requests

# Dirección y puerto del servidor
HOST = 'https://78f5f28d-5168-4c5e-b796-ce64ef2dd8f0-00-3w4d6lfb3rjai.riker.replit.dev/'  # Reemplaza con tu URL de Replit
PORT = 12345
URL = f"{HOST}/mensaje"

# Mensaje a enviar
message = "Hola, servidor"

# Enviar el mensaje al servidor
response = requests.post(URL, data=message)
print(f"Respuesta del servidor: {response.text}")
