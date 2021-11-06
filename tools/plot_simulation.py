import socket

import matplotlib.pyplot as plt
import numpy as np

from tools import config

# Bind the TCP connection with only on device
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((config.HOST, config.PORT))
s.listen(1)

# Connect with client
conn, addr = s.accept()
print("Connected by ", addr)

# Saved temperature
temp = []

while True:
    # Receive data from client
    data = conn.recv(1024)

    # Check whether the clock can be used or not
    if "end" in data.decode():
        break
    else:
        print(data.decode())
        temp.append(float(data.decode()))

print("The clock is over")
conn.close()

plt.scatter(np.arange(len(temp)), temp)
plt.show()
