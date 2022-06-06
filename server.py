import socket, select, json
from config import *

sock = socket.socket()
sock.bind(SERVER_ADDR)
sock.listen(5)
inputs = [sock]
outputs = []

users = {} # key - socket, value - user_id
notifications = {} #key - user_id, value - data string

def finish_connection(s):
	if s in outputs:
		outputs.remove(s)
	inputs.remove(s)
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	try:
		del users[s]
	except Exception as e:
		print(e)
		print(users)

print('binded')

while inputs:
	readable, writable, exceptional = select.select(inputs, outputs, inputs)

	for s in readable:
		if s == sock:
			conn, addr = s.accept()
			conn.setblocking(0)
			inputs.append(conn)
		else:
			data = s.recv(1024).decode('utf-8')

			if data:
				data = json.loads(data.replace('\'', '"'))
				print(s.getpeername())
				if s.getpeername() != DATA_SERVER_ADDR:
					users[s] = data['user_id']
					if s not in outputs:
						outputs.append(s)
				else:
					notifications[data['user_id']] = data['data']
			else:
				finish_connection(s)

	for s in writable:
		if s in users and users[s] in notifications:
			s.send(str(notifications[users[s]]).encode('utf-8'))
			del notifications[users[s]]

	for s in exceptional:
		finish_connection(s)
