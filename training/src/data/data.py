import torch

from torch.utils.data import DataLoader

from torch.utils.data import Dataset
import os
import pandas as pd

import os
import urllib.request

from datasets import load_dataset


team_id_offset = 1610612700

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
    def __init__(self, data_dir = None, file_names = None):


        import os
        import tarfile
        import urllib.request

        if not os.path.exists("nbadata"):

            # URL of the tar file to download
            url = 'https://drive.google.com/uc?id=1ns-D2PzJ4vafvurnCNrrS1xg1M6YfmnM&export=download'

            # Create a directory to store the extracted files
            extracted_dir = './'

            # Download the tar file
            urllib.request.urlretrieve(url, 'nbadata.tar.gz')

            # Extract the tar file and save its contents into the directory
            with tarfile.open('nbadata.tar.gz', 'r:gz') as tar:
                tar.extractall(extracted_dir)

            # Remove the original tar file
            os.remove('nbadata.tar.gz')
            os.rename("nba-ml-training-data", "nbadata")

        self.data_dir = "./nbadata" if data_dir is None else data_dir
        self.file_names = os.listdir(self.data_dir) if file_names is None else file_names
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



def get_hg_nbadata():
    import os
    import tarfile
    import urllib.request

    if not os.path.exists("nbadata"):

        # URL of the tar file to download
        url = 'https://drive.google.com/uc?id=1ns-D2PzJ4vafvurnCNrrS1xg1M6YfmnM&export=download'

        # Create a directory to store the extracted files
        extracted_dir = './'

        # Download the tar file
        urllib.request.urlretrieve(url, 'nbadata.tar.gz')

        # Extract the tar file and save its contents into the directory
        with tarfile.open('nbadata.tar.gz', 'r:gz') as tar:
            tar.extractall(extracted_dir)

        # Remove the original tar file
        os.remove('nbadata.tar.gz')
        os.rename("nba-ml-training-data", "nbadata")

    # 2007 is the beginning year, includes nan data
    data_files = [os.path.join("nbadata", item) for item in os.listdir("nbadata") if "2007" not in item and "playoff" not in item]

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

    ds = load_dataset("csv", data_files=data_files).remove_columns(COLS_TO_DROP)
    ds.set_format("torch")
    ds = ds.map(create_label, batched=True).remove_columns(["T1_W"])
    ds = ds.map(process_cols, batched=True)
    ds = ds.map(merge_cols, batched=True)
    return ds["train"]

def process_cols(x):
    x["T1_IS_HOME"] = x["T1_IS_HOME"].type(torch.int)

    x["T1_TEAM_ID"] = x["T1_TEAM_ID"] - team_id_offset
    x["T2_TEAM_ID"] = x["T2_TEAM_ID"] - team_id_offset

    return x

def create_label(x):
    return  {"label": x["T1_W"]}

def merge_cols(x):
    return {"input": torch.stack([value for key, value in x.items() if key!="label"], dim=1)}


def get_nba_dataloader(
    batch_size,
    shuffle,
    num_workers,
):

    nba_dataset = get_hg_nbadata().train_test_split(0.1)

    return DataLoader(
        dataset=nba_dataset["train"],
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
    ), DataLoader(
        dataset=nba_dataset["test"],
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
    )
