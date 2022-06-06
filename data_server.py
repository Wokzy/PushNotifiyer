import socket, hashlib, time
from config import *

sock = socket.socket()
sock.bind(DATA_SERVER_ADDR)
sock.connect(SERVER_ADDR)

while True:
	user = hashlib.md5(input('Enter user name (it wiil be converted to id) -> ').encode('utf-8')).hexdigest()
	data = input('Enter notification string -> ')
	output = {"user_id":user, "data":data}
	sock.send(bytes(str(output).encode('utf-8')))

	print('data has been sent')
	if input('Continue? [Enter/q]').lower() == 'q':
		break

sock.shutdown(socket.SHUT_RDWR)
time.sleep(0.1)
sock.close()