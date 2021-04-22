# Server.py
import time, socket, sys
from random import randint
import hashlib
from Crypto.Cipher import AES

P = 13
G = 6
PrKB = randint(1,1000)
PuKB = (G**PrKB) % P

print("\nWelcome to End-to-end Encrypted Chat\n")
print("Initialising....\n")

s = socket.socket()
port = 8080
s.bind(("127.0.0.1", port))
name = "Bob"

shareParams = name+","+str(PuKB)
           
s.listen(1)
print("Waiting for incoming connections...\n")
conn, addr = s.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")

s_name = conn.recv(2048)
s_name = s_name.decode()

recParams = s_name.split(",")

print(recParams[0], "has joined the chat.\n")
conn.send(shareParams.encode())

sharedSecret = (int(recParams[1])**PrKB) % P
sharedSecretKey = hashlib.sha1(str(sharedSecret).encode()).hexdigest()[:32]
aesEncrypt = AES.new(sharedSecretKey.encode('utf-8'),AES.MODE_EAX, str(sharedSecret).encode())
aesDecrypt = AES.new(sharedSecretKey.encode('utf-8'),AES.MODE_EAX, str(sharedSecret).encode())
print("The shared secret is: ",sharedSecretKey)

while True:
    message = input(str("Me : "))
    message = aesEncrypt.encrypt(message.encode('utf-8'))
    conn.send(message)
    # conn.send(message.encode())
    message = conn.recv(2048)
    message = aesDecrypt.decrypt(message)
    print(recParams[0], ":", message.decode('utf-8'))