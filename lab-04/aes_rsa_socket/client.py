from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import hashlib

# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Generate RSA key pair
client_key = RSA.generate(2048)

# 1) Receive server's public key
server_public_key = RSA.import_key(client_socket.recv(2048))

# 2) Send client's public key to server
client_socket.send(client_key.publickey().export_key(format='PEM'))

# 3) Receive encrypted AES key from server
encrypted_aes_key = client_socket.recv(2048)

# 4) Decrypt AES key with client's private RSA key
cipher_rsa = PKCS1_OAEP.new(client_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)

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

# Thread to receive messages from server
def receive_messages():
    while True:
        enc_msg = client_socket.recv(1024)
        msg = decrypt_message(aes_key, enc_msg)
        print("Received:", msg)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Main send loop
while True:
    message = input("Enter message ('exit' to quit): ")
    client_socket.send(encrypt_message(aes_key, message))
    if message == "exit":
        break

# Close when done
client_socket.close()