import socket, hashlib, time
from config import *

sock = socket.socket()
sock.connect(SERVER_ADDR)

user_id = {"user_id":hashlib.md5(input('Enter user name -> ').encode("utf-8")).hexdigest()}

sock.send(bytes(str(user_id).encode('utf-8')))
while True:
	data = sock.recv(1024).decode('utf-8')
	if data:
		print(data)
	time.sleep(1)


sock.shutdown(socket.SHUT_RDWR)
time.sleep(0.1)
sock.close()