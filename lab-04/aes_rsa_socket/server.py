from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import hashlib

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# Generate RSA key pair
server_key = RSA.generate(2048)

# List of connected clients
clients = []

# Function to encrypt message
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

# Function to decrypt message
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Function to handle a single client connection
def handle_client(client_socket, client_address):
    print(f"Connected with {client_address}")

    # 1) Send server's public key to client
    client_socket.send(server_key.publickey().export_key(format='PEM'))

    # 2) Receive client's public key
    client_received_key = RSA.import_key(client_socket.recv(2048))

    # 3) Generate AES key for this session
    aes_key = get_random_bytes(16)

    # 4) Encrypt the AES key with the client's public RSA key
    cipher_rsa = PKCS1_OAEP.new(client_received_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    client_socket.send(encrypted_aes_key)

    # 5) Add to clients list
    clients.append((client_socket, aes_key))

    # 6) Receive/encrypt/decrypt loop
    while True:
        encrypted_message = client_socket.recv(1024)
        decrypted_message = decrypt_message(aes_key, encrypted_message)
        print(f"Received from {client_address}: {decrypted_message}")

        if decrypted_message == "exit":
            break

        # Broadcast to other clients
        for (sock, key) in clients:
            if sock != client_socket:
                sock.send(encrypt_message(key, decrypted_message))

    # Cleanup
    clients.remove((client_socket, aes_key))
    client_socket.close()
    print(f"Connection with {client_address} closed")

# Main accept loop
while True:
    client_sock, client_addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
    thread.start()