import socket
import time

# global constants
history = r'C:\Games\server_history.txt'

l = [("Max", "student", 2), ("Danil", "student", 2)]


# Functions
def write_history(s):
    global history
    f = open(history, 'a')
    f.write(time.asctime(time.localtime(time.time())) + '\t' + s + '\n')
    f.close()


def who(conn):
    cmd = 'info '
    author = 'The author: Maksim Litvin'
    task = "The task: Контейнер іменованих об'єктів"
    commands = "Commands: show_all(), add({1},{2},{3}), delete({1})," \
               " show({1}), change({1},{2],{3},{4})"
    conn.send(bytes(cmd + '\n' + author + '\n' + task + '\n' + commands, encoding='utf-8'))
    write_history('server_send: ' + author)
    write_history('server_send: ' + task)
    write_history('server_send: ' + commands)


def add(name, a, b):
    cmd = 'add '
    l.append((name, a, b))
    write_history('server_send:' + cmd + name + ' ' + a + ' ' + b)
    conn.send(bytes(cmd + name + a + b, encoding='utf-8'))


def find(name):
    for i, item in enumerate(l):
        if item[0] == name:
            return i


def delete(name):
    cmd = 'delete '
    n = find(name)
    l.pop(n)
    write_history('server_send:' + cmd + name)
    conn.send(bytes(cmd + name, encoding='utf-8'))


def change(a, b, c, d):
    cmd = 'change '
    n = find(a)
    print(n)
    l.pop(n)
    l.insert(n, (b, c, int(d)))
    write_history('server_send:' + cmd + a)
    conn.send(bytes(cmd + a, encoding='utf-8'))


def show(name):
    cmd = 'show '
    n = find(name)
    write_history('server_send:' + cmd + name)
    conn.send(bytes(cmd + '\n' + str(l[n]), encoding='utf-8'))


def show_all():
    cmd = 'show_all'
    a = ''
    for i, item in enumerate(l):
        a += str(i + 1) + '. ' + str(item) + '\n'
    conn.send(bytes(cmd + '\n' + a, encoding='utf-8'))


# Main
sock = socket.socket()
sock.bind(('', 1035))

while True:
    sock.listen(1)
    conn, addr = sock.accept()
    print('connected:', addr)

    data = conn.recv(1024)
    if not data:
        break
    input_str = data.decode('utf-8')
    write_history('server_get:' + input_str)
    input_str = input_str.split(" ")
    if input_str[0] == 'who':
        who(conn)
    elif input_str[0] == 'show_all':
        show_all()
    elif input_str[0] == 'add':
        try:
            add(input_str[1], input_str[2], input_str[3])
        except:
            write_history('server_send:' + 'add ' + 'Need 3 arguments')
            conn.send(bytes('Need 3 arguments', encoding='utf-8'))
    elif input_str[0] == 'delete':
        try:
            delete(input_str[1])
        except:
            write_history('server_send:' + 'delete ' + 'Need 1 argument')
            conn.send(bytes('Need 1 argument', encoding='utf-8'))

    elif input_str[0] == 'change':
        try:
            change(input_str[1], input_str[2], input_str[3], input_str[4])
        except:
            write_history('server_send:' + 'change ' + 'Need 4 arguments')
            conn.send(bytes('Need 4 arguments: : str, str, str, int', encoding='utf-8'))

    elif input_str[0] == 'show':
        try:
            show(input_str[1])
        except:
            write_history('server_send:' + 'show ' + 'Need 1 argument')
            conn.send(bytes('Need 1 argument', encoding='utf-8'))
    else:
        cmd = 'error '
        write_history('server_send:' + cmd + 'Invalid command')
        conn.send(bytes('Invalid command', encoding='utf-8'))
    conn.close()

f.close()
