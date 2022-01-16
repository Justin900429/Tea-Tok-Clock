import argparse
import platform

import torch
import torch.nn.functional as F

from tqdm import tqdm

from dataset import make_loader
from model import TempModel

if __name__ == "__main__":
    # Fix some bugs on Mac
    if platform.system() == "Darwin":
        import os
        os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

    # Parse the input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", type=str, default="exp/cooling_merge.csv")
    parser.add_argument("--weight", type=str, default="exp/cooling.pt")
    parser.add_argument("--epochs", type=int, default=150)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--hidden_dim", type=int, default=32)
    parser.add_argument("--heating", action="store_true", default=False)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--weight_decay", type=float, default=1e-3)
    args = parser.parse_args()

    # Make model, dataloader, and optimizer for training
    dataloader = make_loader(file_name=args.file_name, batch_size=args.batch_size, heating=args.heating)
    model = TempModel(hidden_dim=args.hidden_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    # Training part
    for epoch in range(args.epochs):
        pg_bar = tqdm(dataloader, desc=f"Epoch {epoch + 1}")
        avg_loss = 0
        for temp, data in pg_bar:
            temp = temp.unsqueeze(-1).float()
            data = data.unsqueeze(-1).float()

            if not args.heating:
                data = torch.log(data)

            predict = model(temp)
            loss = F.smooth_l1_loss(predict, data)
            avg_loss += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            pg_bar.set_postfix_str(f"Loss: {loss.item():.3f}")

    # Save the weight down
    torch.save(model.state_dict(), args.weight)
