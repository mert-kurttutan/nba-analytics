"""
   CIFAR-10 data normalization reference:
   https://github.com/Armour/pytorch-nn-practice/blob/master/utils/meanstd.py
"""

import torch

from torch.utils.data import DataLoader

from torch.utils.data import Dataset
import os
import pandas as pd


def transform_table(
    pd_table: pd.DataFrame
) -> tuple[torch.Tensor, torch.Tensor]:
    COLS_TO_DROP = [
        "Unnamed: 0",
        "GAME_DATE",
        "GAME_ID",
        "T1_TEAM_NAME",
        "T2_TEAM_NAME",
        "T1_PTS",
        "T2_PTS",
        "T1_PLUS_MINUS",
        "T2_PLUS_MINUS",
        "T1_L",
        "T2_L",
        "T1_L_cum",
        "T2_L_cum",
        "T2_W",
        "T2_IS_HOME",
    ]

    LABEL_COL = "T1_W"
    team_id_offset = 1610612700

    pd_table.drop(columns=COLS_TO_DROP, inplace=True)
    pd_table.dropna(inplace=True)

    pd_table.loc[:, "T1_IS_HOME"] = pd_table.loc[:, "T1_IS_HOME"].astype(int)
    pd_table.loc[:, ["T1_TEAM_ID", "T2_TEAM_ID"]] = (
        pd_table.loc[:, ["T1_TEAM_ID", "T2_TEAM_ID"]] - team_id_offset
    )

    train_x = pd_table.drop(columns=LABEL_COL)
    train_y = pd_table.loc[:, LABEL_COL]
    return torch.Tensor(train_x.values), torch.tensor(train_y.values, dtype=torch.long)


# At the moment not optimized, since shuffle leads to redundant file I/O
# not a problem files and dataset is small
# TODO: think about this when this becomes a bottleneck (for whatever process)
class NBADataset(Dataset):
    def __init__(self, file_names, data_dir):
        self.file_names = file_names
        self.data_dir = data_dir
        self.transform = transform_table
        self.set_table_sizes()
        self.table_idx = None
        self.table = None
        self.set_table(0)

    def set_table_sizes(self):
        self.file_sizes = []
        for f_name in self.file_names:
            _table = pd.read_csv(os.path.join(self.data_dir, f_name))
            self.file_sizes.append(_table.shape[0])

    def get_row_table_idx(self, idx):
        for i, table_sz in enumerate(self.file_sizes):
            if idx >= i:
                return idx-table_sz, i

        return 0, 0

    def set_table(self, idx):

        _, table_idx = self.get_row_table_idx(idx)

        if self.table_idx != table_idx:
            self.table_idx = table_idx
            file_path = os.path.join(self.data_dir, self.file_names[table_idx])
            table = pd.read_csv(file_path)

            self.train_x, self.train_y = self.transform(table)

    def __len__(self):
        return sum(self.file_sizes)

    def __getitem__(self, idx):
        self.set_table(idx)
        row_idx, _ = self.get_row_table_idx(idx)
        return self.train_x[row_idx], self.train_y[row_idx]


def get_nba_dataloader(
    dataset_config,
    batch_size,
    shuffle,
    num_workers,
):

    file_names = ["training_2008_regular.csv"]#, "training_2008_playoff.csv"]

    nba_dataset = NBADataset(file_names, "nbadata")

    return DataLoader(
        dataset=nba_dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
    )
