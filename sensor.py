import math
import socket
import time

from tools import config

# Set up the TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((config.HOST, config.PORT))

# Information to be recorded
T_next = config.T_initial
count_time = 0

# Send data stream and compute the temperature
while True:
    T_next = config.T_s + (config.T_initial - config.T_s) * math.exp(config.K * count_time)
    count_time += 1 / 60
    s.send(str(T_next).encode("utf-8"))

    # Reach the final result
    if T_next < 25.001:
        s.send("end".encode("utf-8"))
        time.sleep(1)
        break

    time.sleep(config.ELAPSE)

s.close()
