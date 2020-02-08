import sys
import time
import threading

val = 0


def inp():
    while True:
        sys.stdout.write(f"\r")
        sys.stdout.flush()
        input(":-->")


t = threading.Thread(target=inp).start()
while True:
    print(val)
    val += 1
    time.sleep(1)
