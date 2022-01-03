import torch.nn as nn


class TempModel(nn.Module):
    def __init__(self, hidden_dim=16):
        super(TempModel, self).__init__()

        self.layers = nn.Sequential(
            nn.Linear(1, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, x):
        return self.layers(x)
