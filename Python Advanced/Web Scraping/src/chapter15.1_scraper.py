import _thread
import time


def print_time(threadName, delay, iterations):
    start = int(time.time())
    for i in range(0, iterations):
        time.sleep(delay)
        seconds_elapsed = str(int(time.time()) - start)
        print("{} {}".format(seconds_elapsed, threadName))


try:
    _thread.start_new_thread(print_time, ("Bella", 3, 33))
    _thread.start_new_thread(print_time, ("Echo", 5, 20))
    _thread.start_new_thread(print_time, ("VL", 1, 100))
except:
    print("Error: unable to start thread")

while True:
    pass
