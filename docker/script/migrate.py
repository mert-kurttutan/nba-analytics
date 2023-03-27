
import pandas as pd
from datetime import date
import pathlib

from nba_backend.db import (
    Base, engine
)

Base.metadata.create_all(bind=engine)





def write_teamstat(pd_table):
    pd_table = pd_table.sort_index(axis=1)
    pd_table["GAME_DATE"] = pd_table["GAME_DATE"].apply(date.fromisoformat)
    pd_table.to_sql(con=engine, index_label='id', name="teamstat_table", if_exists='replace')



# file_name = 'gamelog_2016_regular.csv'
# df = pd.read_csv(file_name)


def write_gamelog(pd_table):
    pd_table = pd_table.sort_index(axis=1)
    pd_table["GAME_DATE"] = pd_table["GAME_DATE"].apply(date.fromisoformat)
    pd_table["T1_IS_HOME"] = pd_table["T1_IS_HOME"].apply(int)
    pd_table["T2_IS_HOME"] = pd_table["T2_IS_HOME"].apply(int)
    pd_table.to_sql(con=engine, index_label='id', name="gamelog_table", if_exists='replace')



def migrate_teamstat_csv():
    teamstat_files = pathlib.Path("db-files/teamstat")

    for _file in teamstat_files.iterdir():
        df_teamstat = pd.read_csv(_file)
        write_teamstat(df_teamstat)

def migrate_gamelog_csv():
    gamelog_files = pathlib.Path("db-files/gamelog")

    for _file in gamelog_files.iterdir():
        df_gamelog = pd.read_csv(_file)
        write_gamelog(df_gamelog)