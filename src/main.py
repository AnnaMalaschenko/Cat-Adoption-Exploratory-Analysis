import os
from pathlib import Path
import pandas as pd
import api_v03 as api #  Get API data
import data_cleaner as cleaner


os.chdir(Path(__file__).parent.parent)

cleaner.cleaner('data/raw/data_filtered.parquet', 'data/clean/clean_cats_data.parquet')

df = pd.read_parquet('data/clean/clean_cats_data.parquet')
