import os
import time
from datetime import datetime

import pandas as pd
import pytz
from apiclient.discovery import build

intz = pytz.timezone('Asia/Kolkata')
nowdt = datetime.now(intz).strftime("%d%m%Y%H%M")
save_filename = f"youtube_trends_{nowdt}.csv"

regionid_data = pd.read_csv("info/region_id.csv")


api_key = os.getenv("API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)


def collect_data(r):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics,localizations,topicDetails",
        chart="mostPopular",
        regionCode=r["country"],
        maxResults=5,
        hl="ta"

    )
    response = request.execute()

    df = pd.json_normalize(response["items"])

    return df.copy()


total_trends = pd.DataFrame()
for i, r in regionid_data.iterrows():
    try:

        country_trends_df = collect_data(r)
        total_trends = total_trends.append(
            country_trends_df, ignore_index=True)

    except:
        pass


if not os.path.exists("./data"):
    os.makedirs("./data")

total_trends.to_csv(f"./data/{save_filename}")
