from threading import Thread
import argparse, socket, time
import sys

value = 0

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received' '%d bytes before the socket closed' % (length, len(data)))   
        data += more
    return data

def my_handle_request(sock):
    print("0")
    global value
    print("1")
    len_msg = recvall(sock, 3)
    print("2")
    message = recvall(sock, int(len_msg))
    message = str(message, encoding="ascii")
    print("3")
    ii = message.split()
    if ii[0] =="ADD":
        value += int(ii[1])
    elif ii[0] == "DEC":
        value -= int(ii[1])
    else:
        print("unknown command...: ", ii)
        sys.exit(0)
    msg = "value = : " + str(value)
    len_msg = b"%03d" % (len(msg),)
    msg = len_msg + bytes(msg, encoding='ascii')
    sock.sendall(msg)


def my_threads(listener):
    while True: 
        sock, address, = listener.accept()
        print('Accepted connection from {}'.format(address))
        print("masok")
        my_handle_request(sock)
        try:
            print("masok")
            while True:
                #print("true")
                print("masok")
                my_handle_request(sock)
        except EOFError:
            print('Client socket to {} has closed'.format(address))
        except Exception as e:
            print('Client {} error: {}'.format(address, e))
        finally:
            print("anu")
            global value
            value = 0
            sock.close()

def start_threads(listener, workers=4):
    t = (listener,)
    print("masuk thread")
    for i in range(workers):
        Thread(target = my_threads, args=t).start()
        print("kelar")

def create_srv_socket(address):
    """Build and return a listening server socket."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('Listening at {}'.format(address))
    return listener

def parse_command_line(description):
    """Parse command line and return a socket address."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    return address

if __name__ == '__main__':
    address = parse_command_line('multi-threaded server')
    listener = create_srv_socket(address)
    start_threads(listener)