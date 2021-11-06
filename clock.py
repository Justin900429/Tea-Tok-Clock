import datetime
import math
import socket
import tkinter as tk

from tools import Clock
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


def temp_to_time(in_temp):
    time = math.log((in_temp - config.T_s) / (config.T_initial - config.T_s)) / config.K
    return time * 60


def get_time():
    # Receive data from client
    data = conn.recv(1024)
    temperature = data.decode()

    if "end" in temperature:
        root.destroy()

    time = round(temp_to_time(float(temperature)), 0)
    conversion = datetime.timedelta(seconds=time)
    root.clk.config(text=str(conversion))
    root.temp.config(text=f"{float(temperature):.3f}˚C")
    root.after(config.ELAPSE * 1000, get_time)


if __name__ == "__main__":
    root = Clock()

    # Set up the theme to prevent the bug on MacOS
    style = tk.ttk.Style()
    style.theme_use('classic')

    get_time()
    root.mainloop()

print("The clock is over")
conn.close()
