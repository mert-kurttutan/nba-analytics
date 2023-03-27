'''transform teamstat'''

import os

from pathlib import Path
from datetime import date
import pandas as pd
import numpy as np

from ..enums import FileConfig

from ..utils import (
    add_prefix, sort_df_cols, gamelog_name, daystat_name_filled, training_name
)




def get_training_data(
    year_arr: list[int],
    config_dict,
    file_config: FileConfig,
    is_upload: bool = True,
    ):

    stat_type = 'teamstat'
    # Make sure gamerotation diretory exists
    Path(f'{file_config.ROOT_TRANSFORMED}/'
    ).mkdir(parents=True, exist_ok=True)


    # Make sure gamerotation diretory exists
    Path(f'{file_config.ROOT_TRAINING}/'
    ).mkdir(parents=True, exist_ok=True)
    print(file_config.ROOT_TRAINING)
    os.system(
        f"aws s3 cp s3://{file_config.ROOT_TRANSFORMED}/ "
        f"{file_config.ROOT_TRANSFORMED}/ --recursive "
        f"--exclude \"*\" --include \"*.csv\" " )

    for year in year_arr:

        for season_type in ["playoff", "regular"]:

            gamelog_file_nm = (
                f'{file_config.ROOT_TRANSFORMED}/gamelog_data/'
                f'{gamelog_name(year, season_type)}'
            )
            teamstat_file_nm = (
                f'{file_config.ROOT_TRANSFORMED}/teamstat_data/'
                f'{daystat_name_filled(stat_type, year, season_type)}'
            )

            training_file_nm = (
                f'{file_config.ROOT_TRAINING}/'
                f'{training_name(year, season_type)}'
            )

            df_gamelog = pd.read_csv(gamelog_file_nm)
            df_teamstat = pd.read_csv(teamstat_file_nm)

            merged_0 = merge_teamstat_gamelog(df_gamelog, df_teamstat, 1)
            merged_1 = merge_teamstat_gamelog(merged_0, df_teamstat, 2)

            merged_1 = sort_df_cols(merged_1)
            merged_1.to_csv(training_file_nm)

    if is_upload:
        os.system(
            f"aws s3 cp {file_config.ROOT_TRAINING}/ "
            f"s3://{file_config.ROOT_TRAINING}/ --recursive "
            f"--exclude \"*\" --include \"*.csv\" " )


def merge_teamstat_gamelog(
    gamelog_df: pd.DataFrame,
    teamstat_df: pd.DataFrame,
    team_idx: int,
) -> pd.DataFrame:

    cols = list(teamstat_df.columns)
    cols.remove("GAME_DATE")
    cols.remove("DAY_WITHIN_SEASON")

    # rename teamstat cols for merging
    col_map1 = add_prefix(col_arr=cols, prefix=f"T{team_idx}_")

    teamstat_df = teamstat_df.rename(columns=col_map1)

    # Add team_stat into gamelog data
    return pd.merge(
        gamelog_df, teamstat_df,
        on=["GAME_DATE", "DAY_WITHIN_SEASON", f"T{team_idx}_TEAM_ID"], how="left"
    )
