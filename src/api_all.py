# for future reference to pull all pages available - significantly slowed at 3k pages
import os, math, time, threading
import pandas as pd
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

API_KEY = os.getenv("API_KEY")
LIMIT = 250
WORKERS = 5
BATCH_SIZE = 100
OUTFILE = "data/raw/anna_data_filtered.parquet"
VIEW = "cats"

thread_local = threading.local()

FIELDS = [
    "sex","sizeCurrent","sizeGroup","sizeUOM","ageGroup","ageString",
    "breedString","colorDetails","vocalLevel","sheddingLevel","energyLevel",
    "exerciseNeeds","isSpecialNeeds","isCurrentVaccinations","isDeclawed",
    "isHousetrained","isKidsOk","adultSexesOk","obedienceTraining",
    "ownerExperience","newPeopleReaction","pictureCount","videoCount",
    "adoptedDate","availableDate"
]

def session():
    if not hasattr(thread_local, "session"):
        s = requests.Session()
        s.headers.update({
            "Authorization": API_KEY,
            "Content-Type": "application/vnd.api+json"
        })
        thread_local.session = s
    return thread_local.session

def fetch(page):
    url = (
        f"https://api.rescuegroups.org/v5/public/animals/search/{VIEW}"
        f"?limit={LIMIT}&page={page}"
        f"&fields[animals]={','.join(FIELDS)}"
    )
    for retry in range(5):
        try:
            r = session().get(url, timeout=30)
            r.raise_for_status()
            return r.json()["data"]
        except Exception:
            time.sleep(2 ** retry)
    return []

def process(records):
    rows = [{"id": r["id"], **r["attributes"]} for r in records]
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    if "adoptedDate" in df.columns:
        df["adoptedDate"] = pd.to_datetime(df["adoptedDate"], errors="coerce")
    if "availableDate" in df.columns:
        df["availableDate"] = pd.to_datetime(df["availableDate"], errors="coerce")
    if "adoptedDate" in df.columns and "availableDate" in df.columns:
        df["length_of_stay"] = (df["adoptedDate"] - df["availableDate"]).dt.days
    return df

# get total pages
s = requests.Session()
s.headers["Authorization"] = API_KEY
meta = s.get(f"https://api.rescuegroups.org/v5/public/animals/search/{VIEW}?limit=1").json()
pages = math.ceil(meta["meta"]["count"] / LIMIT)
print(f"{pages:,} pages to fetch")

all_dfs = []

for start in range(1, pages + 1, BATCH_SIZE):
    end = min(start + BATCH_SIZE, pages + 1)

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        dfs = list(ex.map(lambda p: process(fetch(p)), range(start, end)))

    batch = pd.concat([df for df in dfs if not df.empty], ignore_index=True)
    all_dfs.append(batch)

    print(f"Pages {start}-{end-1} complete, batch fetched")

pd.concat(all_dfs).to_parquet(OUTFILE, engine="pyarrow", compression="snappy", index=False)
print("All data saved to Parquet")