import math
import os
import glob
import socket
import time

from tools import config

# Set up w1-wire
os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")

base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")[0]
device_file = device_folder + "/w1_slave"


def read_temp_raw():
    f = open(device_file, "r")
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


if __name__ == "__main__":
    # Set up the TCP connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", config.PORT))
    s.listen(1)

    # Connect with server
    conn, addr = s.accept()
    print("Connected by ", addr)

    # Send data stream and compute the temperature
    while True:
        temperature = read_temp()
        if temperature is None:
            continue

        conn.send(str(temperature).encode("utf-8"))

        # Reach the final result
        if temperature < 25.001:
            conn.send("end".encode("utf-8"))
            time.sleep(1)
            break

        time.sleep(config.ELAPSE)

    s.close()
