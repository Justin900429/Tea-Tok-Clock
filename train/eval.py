import argparse
import platform
import matplotlib.pyplot as plt
import numpy as np
import torch
from tqdm import tqdm

from model import TempModel
from dataset import make_loader

if __name__ == "__main__":
    # Fix some bugs on Mac
    if platform.system() == "Darwin":
        import os
        os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

    # Parse the input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", type=str, default="exp/cooling.csv")
    parser.add_argument("--weight", type=str, default="exp/cooling.pt")
    parser.add_argument("--plot", type=str, default="images/cooling_eval.png")
    parser.add_argument("--heating", action="store_true", default=False)
    args = parser.parse_args()

    model = TempModel(hidden_dim=32).eval()
    model.load_state_dict(torch.load(args.weight))
    data_loader = make_loader(
        file_name=args.file_name, batch_size=1,
        shuffle=False, heating=args.heating
    )

    all_temp = []
    prediction = []
    real = []
    with torch.no_grad():
        for temp, k in tqdm(data_loader):
            temp = temp.unsqueeze(-1).float()
            all_temp.append(temp.item())

            if args.heating:
                prediction.append(model(temp).item())
            else:
                prediction.append(torch.exp(model(temp)).item())

            real.append(k.item())

    plt.scatter(all_temp, real, c="blue", s=0.5, label="real")
    plt.scatter(all_temp, prediction, c="red", s=0.5, label="prediction")
    plt.legend()
    plt.savefig(args.plot, dpi=1200)
    plt.show()

