#! /usr/bin/env python3

import sqlite3
import pandas
from os import listdir
from os.path import join
from tqdm import tqdm

def csv_to_table(csvfile, tablename):
    df = pandas.read_csv(csvfile, chunksize=20000)
    for chunk in tqdm(df):
        chunk.to_sql(tablename, con, if_exists='append', index=False)

CSV_FOLDER = "./"
DB_NAME = "database.db"

csv_files = list(filter(lambda i: i.endswith(".csv"), listdir(CSV_FOLDER)))

db_path = join(CSV_FOLDER, DB_NAME)

con = sqlite3.connect(db_path)
print(f"[*] Connected to database at {db_path}")

for i, csv in enumerate(csv_files, start=1):
    print(f"[{i}/{len(csv_files)}] Converting {csv} to SQL as table '{csv[:-4]}'")
    csv_to_table(join(CSV_FOLDER, csv), f"{csv[:-4]}")

print(f"[*] Closing connection to database at {db_path}")
con.close()

