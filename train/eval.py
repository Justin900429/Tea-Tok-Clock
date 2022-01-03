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
    parser.add_argument("--file_name", type=str, default="exp/record.csv")
    parser.add_argument("--weight", type=str, default="exp/model.pt")
    parser.add_argument("--plot", type=str, default="images/eval.svg")
    args = parser.parse_args()

    model = TempModel().eval()
    model.load_state_dict(torch.load(args.weight))
    data_loader = make_loader(
        file_name=args.file_name, batch_size=1,
        shuffle=False
    )

    prediction = []
    real = []
    with torch.no_grad():
        for temp, k in tqdm(data_loader):
            temp = temp.unsqueeze(-1).float()
            prediction.append(torch.exp(model(temp)).item())
            real.append(k.item())

    plt.scatter(np.arange(len(prediction)), real, c="blue", s=0.5, label="real")
    plt.scatter(np.arange(len(prediction)), prediction, c="red", s=0.5, label="prediction")
    plt.legend()
    plt.savefig(args.plot)
    plt.show()

