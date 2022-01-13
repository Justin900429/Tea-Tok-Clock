import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader


class TempDataset(Dataset):
    def __init__(self, file_name, heating):
        self.file = pd.read_csv(file_name)
        self.heating = heating

    def __getitem__(self, idx):
        return (
            self.file.loc[idx, "temperature"],
            self.file.loc[idx, "time"] if self.heating else self.file.loc[idx, "real_k"]
        )

    def __len__(self):
        return len(self.file)


def make_loader(file_name, batch_size, heating, shuffle=True):
    dataset = TempDataset(file_name, heating)
    dataloader = DataLoader(
        dataset=dataset, batch_size=batch_size,
        shuffle=shuffle, pin_memory=True
    )

    return dataloader
