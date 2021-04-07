#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter03/tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets

import argparse, socket
import glob
import pickle
import sys
import time

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    print('Waiting to accept a new connection')
    sc, sockname = sock.accept()
    print('We have accepted a connection from', sockname)
    print('  Socket name:', sc.getsockname())
    print('  Socket peer:', sc.getpeername())
    while True:
    
        #klaim command dari client
        len_command = recvall (sc, 3) 
        message = recvall(sc, int(len_command))
        print('  Incoming message:', repr(message))

        #displit command sama argumen
        command = message.split()
        arg = []
        if (len(command)==2):
            arg.append(command[1])
        elif (len(command)==3):
            arg.append(command[1])
            arg.append(command[2])
        command_text = command[0]

        #Jika commandnya LS
        if((command_text == b'ls') and (len(command)==2)):
            ls = glob.glob(arg[0])
            msg = pickle.dumps(ls)
            sc.send(msg)
        
        #Jika commandnya cuma LS
        if((command_text == b'ls') and (len(command)==1)):
            ls = glob.glob(b'*')
            msg = pickle.dumps(ls)
            sc.send(msg)

        #Jika commandnya GET
        elif ((command_text == b'get') and (len(command)==3)):
        
            #buka file dan baca datanya
            path = arg[0].decode("utf-8")
            file = open (path,"rb")
            data = file.read()
            file.close

            #kirim data ke client
            len_data = b"%04d" % (len(data),)
            msg = len_data + data
            sc.sendall(msg)

        #Jika commandnya QUIT
        elif (command_text == b'quit'):
            message = b'server shutdown..'

            #kirim message ke client
            len_message = b"%03d" % (len(message),)
            message = len_message + message
            sc.sendall(message)

            #jeda 1 dtk
            time.sleep(1)

            #stop looping
            break
    #done
    sc.close()
    print('  Reply sent, server shutdown')

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    while True:
        command = input("> ").encode('utf_8')
        commands = command.split()

        #Jika commandnya LS
        if ((commands[0]==b'ls') and (len(commands)>=1)):

            #sending command ke server
            len_command = b"%03d" % (len(command),)
            msg = len_command + command
            sock.sendall(msg)

            #klaim output server
            messages = sock.recv(4096)
            message = pickle.loads(messages)

            #print vertikal
            for line in message:
                print(line.decode("utf-8"))

        #Jika commandnya GET
        elif ((commands[0]==b'get')  and (len(commands)==3)):

            #sending command ke server
            len_command = b"%03d" % (len(command),)
            msg = len_command + command
            sock.sendall(msg)

            #klaim ouput server
            len_message = recvall (sock, 4) 
            data = recvall(sock, int(len_message))
            size = sys.getsizeof(data)

            #buka file dan masukin data
            file = open(commands[2].decode("utf-8"),"wb")
            file.write(data)
            file.close
            print("fetch:"+ str(commands[1].decode("utf-8")) + " size:" + str(size) + " lokal:" + str(commands[2].decode("utf-8")))

        #Jika commandnya QUIT
        elif commands[0]==b'quit':

            #sending command ke server
            len_command = b"%03d" % (len(command),)
            msg = len_command + command
            sock.sendall(msg)

            #klaim message dari server
            len_message = recvall (sock, 3) 
            message = recvall(sock, int(len_message))
            print(message.decode("utf-8"))
            print('client shutdown..')

            #stop looping
            break   
        else:
            print("unknown...")

    #done
    sock.close()

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
