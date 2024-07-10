import socket

# Configurar el cliente
HOST = '78f5f28d-5168-4c5e-b796-ce64ef2dd8f0-00-3w4d6lfb3rjai.riker.replit.dev'
PORT = 8080

# Crear un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Conectar al servidor
    client_socket.connect((HOST, PORT))

    # Enviar datos al servidor
    message = "Hola, servidor!"
    client_socket.sendall(message.encode())
    print(f'Mensaje enviado al servidor: {message}')
