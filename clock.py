import argparse
import datetime
import math
import socket
import tkinter as tk

import torch

from train import TempModel
from tools import Clock
from tools import config

# Bind the TCP connection with device
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((config.HOST, config.PORT))

# Saved temperature
temp = []
count_axis = []
count = 1

# Load model
model = TempModel().eval()


def model_prediction(in_temp):
    global HEATING

    k = model(torch.tensor([in_temp]).unsqueeze(0))
    return k.item() if HEATING else math.exp(k.item())


def temp_to_k(in_temp):
    return 0.0007 * in_temp - 0.0018


def temp_to_time(in_temp, mode):
    global HEATING

    if mode == "ori":
        k = config.K
    elif mode == "lin":
        k = -1 * temp_to_k(in_temp)
    else:
        k = -1 * model_prediction(in_temp)

    if HEATING:
        time = -k
    else:
        time = 60 * math.log((in_temp - config.T_s) / (config.T_initial - config.T_s)) / k
    return time


def get_time(mode):
    global count, HEATING

    # Receive data from server
    data = s.recv(1024)
    if "end" in data.decode("utf-8"):
        root.destroy()

    try:
        temperature = float(data.decode("utf-8"))
    except Exception as e:
        temperature = float(data.decode("utf-8").rsplit(".")[0])

    if HEATING and (temperature > 100.0):
        root.after(config.ELAPSE * 200, get_time, mode)
        return
    elif not HEATING and (temperature < 40.0):
        root.after(config.ELAPSE * 200, get_time, mode)
        return

    try:
        time = round(temp_to_time(temperature, mode), 0)
        conversion = datetime.timedelta(seconds=time)
        root.clk.config(text=str(conversion))
        root.temp.config(text=f"{temperature:.3f}˚C")
        temp.append(temperature)
        count_axis.append(count)
        root.axis.plot(count_axis, temp, color="blue")
        root.canvas.draw()
        count += 1
        root.after(config.ELAPSE * 200, get_time, mode)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Mode for computing the k value", type=str, default="ori")
    parser.add_argument("--heating", help="Whether is heating or not", action="store_true", default=False)
    parser.add_argument("--weight", help="Weight for the model", type=str, default="exp/cooling.pt")
    args = parser.parse_args()
    assert args.mode in ["ori", "lin", "model"], "The mode should be in [ori, log, model]."

    model.load_state_dict(torch.load(args.weight, map_location="cpu"))
    root = Clock()

    HEATING = args.heating

    # Set up the theme to prevent the bug on macOS
    style = tk.ttk.Style()
    style.theme_use('classic')

    get_time(args.mode)
    root.mainloop()

print("The clock is over")
s.close()
