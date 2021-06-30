#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter08/queuepi.py
# Small application that uses several different message queues

import random, threading, time, zmq, sqlite3, os, sys, hashlib

start = time.time()
end = time.time()
count_all = 0
total = 0

def sqlGenerator(zcontext, url, url2):
    """Produce random points in the unit square."""
    zsock = zcontext.socket(zmq.PUB)
    zsock.bind(url)

    zsock2 = zcontext.socket(zmq.PUB)
    zsock2.bind(url2)
    count = 0
    for i in range(10):
        # print("masuk for sql generator")
        n1 = random.randint(1, 99000)
        n2 = random.randint(1, 1000)
        sql = "select count(*) from MOCKDATA where ID>=%s AND ID<=%s;" % (n1, n1+n2)
        
        # print("sql : ", sql)
        
        h = hash(sql)
        
        # print("hashed: ", h)
        
        kirim = h%2
        # if (kirim) : 
        zsock2.send_string(sql)
        kirim = str(kirim)
        
        # print("yang dikirim di awal : ", kirim)
        # print()
        
        zsock.send_string(kirim)
        count += 1
        # print ("total awal: ", count)
        time.sleep(0.1)

def return_0(zcontext, in_url, in_url2, out_url):
    """Coordinates in the lower-left quadrant are inside the unit circle."""
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b'0')

    isock2 = zcontext.socket(zmq.SUB)
    isock2.connect(in_url2)
    isock2.setsockopt_string(zmq.SUBSCRIBE, "select")
    
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    # print("return 0 jalan")
    count = 0
    while True:
        # print("return 0 terima :" ,isock.recv_string())
        osock.send_string('0')
        count += 1
        # print ("return 0: ",count)
        print(isock2.recv_string(), " count() = ", isock.recv_string())

def req_service(zcontext, in_url, in_url2, pythagoras_url, out_url):
    """Determine whether each input coordinate is inside the unit circle."""
    
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b"1")
    
    isock2 = zcontext.socket(zmq.SUB)
    isock2.connect(in_url2)
    isock2.setsockopt_string(zmq.SUBSCRIBE, "select")

    psock = zcontext.socket(zmq.REQ)
    psock.connect(pythagoras_url)
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    
    count = 0
    while True:
        # print("\nreq service jalan while\n")
        yangDiterima = isock.recv_string()
        # print("\nyangDiterima :", yangDiterima)
        
        sqlDiterima = isock2.recv_string()
        # print("sqlDiterima :", sqlDiterima)

        
        psock.send_string(sqlDiterima)
        hasilQuery = psock.recv_string()
        # print ("hasilquery: ", hasilQuery)

        # print("hasilQuery :", hasilQuery)
        osock.send_string(str(hasilQuery))
        count += 1
        # print ("service: ",count)
        

def sqlite_executor(zcontext, url):
    """Return the sum-of-squares of number sequences."""
    zsock = zcontext.socket(zmq.REP)
    zsock.bind(url)

    # print("sqlite executor jalan")

    while True:
        db = sqlite3.connect("data.db")
        cur = db.cursor()
        query = zsock.recv_string()
        cur.execute(str(query))
        value = int(cur.fetchone()[0])
        # print("value: ", value)
        db.close()
        print(query, " count() = ", value)
        zsock.send_string(str(value))

def print_all(zcontext, url, url2):
    """Tally how many points fall within the unit circle, and print pi."""
    zsock = zcontext.socket(zmq.PULL)
    zsock.bind(url)

    # sqlsock = zcontext.socket(zmq.SUB)
    # sqlsock.connect(url2)

    # print("printall jalan")
    global count_all
    global total
    global end

    for i in range(10):
        # print("count : ", count_all)
        value = zsock.recv_string()
        # query = sqlsock.recv_string()
        # print ("last value: ", value)
        count_all += 1
        total += int(value)
        end = time.time()
        # print ("last: ",all)
        # print("num query = %d, total return value = %d" % (count_all, total))

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True  # so you can easily Ctrl-C the whole program
    thread.start()

def main(zcontext):
    global count_all
    global total

    pubsub = 'tcp://127.0.0.1:6700'
    pubsub2 = 'tcp://127.0.0.1:6703'
    
    reqrep = 'tcp://127.0.0.1:6701'
    pushpull = 'tcp://127.0.0.1:6702'
    
    start_thread(sqlGenerator, zcontext, pubsub, pubsub2)
    start_thread(return_0, zcontext, pubsub,pubsub2, pushpull)
    start_thread(req_service, zcontext, pubsub, pubsub2, reqrep, pushpull)
    start_thread(sqlite_executor, zcontext, reqrep)
    start_thread(print_all, zcontext, pushpull, pubsub2)
    time.sleep(5)
    print()
    print()
    print("num query = %d, total return value = %d" % (count_all, total))
    print("waktu: = ", end-start)

if __name__ == '__main__':
    main(zmq.Context())
    