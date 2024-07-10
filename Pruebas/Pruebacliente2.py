import requests

# Dirección y puerto del servidor
HOST = 'https://confident-gratia-pokemon-crystal-online-d49b6bc2.koyeb.app/pks'  # Reemplaza con tu URL de Replit
PORT = 8000
URL = f"{HOST}/mensaje"

# Mensaje a enviar
message = "Hola, servidor"

# Enviar el mensaje al servidor
response = requests.post(URL, data=message)
print(f"Respuesta del servidor: {response.text}")
