import socket
import time
import sys

# global constants
f = open(r'C:\Games\client_history.txt', 'a')
host = ''


# Functions
def write_history(s):
    f.write(time.asctime(time.localtime(time.time())) + '\t' + s + '\n')
    f.close()


def get_host():
    global host
    print('Input server ip adress: ')
    host = input()


# Main
if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    get_host()

sock = socket.socket()
sock.connect((host, 1035))

print('Input command: ')
inp = input()
sock.send(bytes(inp, encoding='utf-8'))
write_history('client_send:' + inp)

while True:

    data = sock.recv(1024)
    if not data:
        break
    ans = data.decode('utf-8')
    print(ans)

f.close()
sock.close()
