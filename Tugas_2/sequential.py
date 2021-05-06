import sys

value = 0
for ii in sys.stdin:
    ii = ii.strip().split()
    if ii[0]=="ADD":
        value += int(ii[1])
    elif ii[0]=="DEC":
        value -= int(ii[1])
    else:
        print("unknown command...: ", ii)
        sys.exit(0)
print("value = ", value)

# import threading

# a = threading.Lock()
# a.acquire_lock()
# a.release_()