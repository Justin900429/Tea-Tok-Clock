import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader


class TempDataset(Dataset):
    def __init__(self, file_name):
        self.file_name = pd.read_csv(file_name)

    def __getitem__(self, idx):
        return (
            self.file_name.loc[idx, "temperature"],
            self.file_name.loc[idx, "real_k"]
        )

    def __len__(self):
        return len(self.file_name)


def make_loader(file_name, batch_size, shuffle=True):
    dataset = TempDataset(file_name)
    dataloader = DataLoader(
        dataset=dataset, batch_size=batch_size,
        shuffle=shuffle, pin_memory=True
    )

    return dataloader
