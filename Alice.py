# Client.py
import time, socket, sys
from random import randint
import hashlib
from Crypto.Cipher import AES

P = 13
G = 6
PrKA = randint(1,1000)
PuKA = (G**PrKA) % P

print("\nWelcome to End-to-end Encrypted Chat\n")
print("Initialising....\n")

s = socket.socket()
host = "127.0.0.1"
port = 8080
name = "Alice"

shareParams = name+","+str(PuKA)

print("Trying to connect to ", host, "(", port, ")\n")
time.sleep(1)
s.connect((host, port))

s.send(shareParams.encode())
s_name = s.recv(2048)
s_name = s_name.decode()

recParams = s_name.split(",")
sharedSecret = (int(recParams[1])**PrKA) % P
sharedSecretKey = hashlib.sha1(str(sharedSecret).encode()).hexdigest()[:32]
aesEncrypt = AES.new(sharedSecretKey.encode('utf-8'),AES.MODE_EAX, str(sharedSecret).encode())
aesDecrypt = AES.new(sharedSecretKey.encode('utf-8'),AES.MODE_EAX, str(sharedSecret).encode())

print(recParams[0], "has joined the chat.\n")
print("The shared secret is: ",sharedSecretKey)

while True:
    message = s.recv(2048)
    message = aesDecrypt.decrypt(message)
    print(recParams[0], ":", message.decode('utf-8'))
    message = input(str("Me : "))
    message = aesEncrypt.encrypt(message.encode('utf-8'))
    s.send(message)
    # s.send(message.encode())