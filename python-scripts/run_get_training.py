#!/usr/bin/env python3
'''Script for transforming gamelog info
'''

# Local modules
from nbaetl import transform, extract, utils
from nbaetl.enums import FileConfig



if __name__ == "__main__":

    data_config = extract.define_config_vars(FileConfig)

    cli_args = extract.cli()
    year_arr = [int(year) for year in cli_args.year_arr]

    transform.get_training_data(year_arr, data_config, FileConfig)
    utils.clear_dir(FileConfig.ROOT_RAW)
    utils.clear_dir(FileConfig.ROOT_TRANSFORMED)
    utils.clear_dir(FileConfig.ROOT_TRAINING)
