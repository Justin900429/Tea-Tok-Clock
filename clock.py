import datetime
import math
import socket
import tkinter as tk

from tools import Clock
from tools import config

# Bind the TCP connection with device
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((config.HOST, config.PORT))

# Saved temperature
temp = []
count_axis = []
count = 1


def temp_to_time(in_temp):
    time = math.log((in_temp - config.T_s) / (config.T_initial - config.T_s)) / config.K
    return time * 60


def get_time():
    global count

    # Receive data from server
    data = s.recv(1024)
    temperature = data.decode("utf-8")

    if float(temperature) > 100.0:
        root.after(config.ELAPSE * 1000, get_time)
        return

    if "end" in temperature:
        root.destroy()
    try:
        time = round(temp_to_time(float(temperature)), 0)
        conversion = datetime.timedelta(seconds=time)
        root.clk.config(text=str(conversion))
        root.temp.config(text=f"{float(temperature):.3f}˚C")
        temp.append(float(temperature))
        count_axis.append(count)
        root.axis.plot(count_axis, temp, color="blue")
        root.canvas.draw()
        count += 1
        root.after(config.ELAPSE * 1000, get_time)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    root = Clock()

    # Set up the theme to prevent the bug on MacOS
    style = tk.ttk.Style()
    style.theme_use('classic')

    get_time()
    root.mainloop()

print("The clock is over")
s.close()
