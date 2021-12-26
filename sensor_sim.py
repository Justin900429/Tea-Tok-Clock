import math
import socket
import time

from tools import config


if __name__ == "__main__":
    # Set up the TCP connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", config.PORT))
    s.listen(1)

    # Connect with server
    conn, addr = s.accept()
    print("Connected by ", addr)

    # Information to be recorded
    T_next = config.T_initial
    count_time = 0

    # Send data stream and compute the temperature
    while True:
        T_next = config.T_s + (config.T_initial - config.T_s) * math.exp(config.K * count_time)
        count_time += 1 / 60
        conn.send(str(T_next).encode("utf-8"))

        # Reach the final result
        if T_next < 25.001:
            conn.send("end".encode("utf-8"))
            time.sleep(1)
            break

        time.sleep(config.ELAPSE)

    s.close()
