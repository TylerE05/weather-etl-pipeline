import requests
import time
import pandas as pd
import sqlite3
import os
from datetime import datetime, timezone

#Configs
#─────────────────────────────────────────────
API_KEY = "674171991048121bd77d913b249054cb"
BASE_URL = "http://api.weatherstack.com/current"
CITIES = ["Orlando", "New York", "Los Angeles"]
DB_NAME = "weatherstack.db"


#Extract (Import data from Weatherstack API)
#─────────────────────────────────────────────
def extract(city: str) -> dict:
    parameters = {
        "access_key": API_KEY,
        "query": city,
    }
    response = requests.get(BASE_URL, params=parameters)
    response.raise_for_status() #raises error if request failed
    data = response.json()
    if "error" in data:
        raise ValueError(f"API error for '{city}': {data['error']['info']}")
    return data


#Transform (Clean and reshape)
#─────────────────────────────────────────────
def transform(raw: dict) -> pd.DataFrame:
    location = raw.get("location", {})
    current  = raw.get("current",  {})
    record = {
        "city":         location.get("name"),
        "country":      location.get("country"),
        "temp_c":       current.get("temperature"),
        "feels_like_c": current.get("feelslike"),
        "humidity_pct": current.get("humidity"),
        "wind_kph":     current.get("wind_speed"),
        "description":  current.get("weather_descriptions", [""])[0],
        "temp_f":       round(current.get("temperature", 0) * 9/5 + 32, 1),
        "feels_cold":   current.get("temperature", 0) < 10,
        "pipeline_run": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    }
    return pd.DataFrame([record])


#Load (write to SQLite)
#─────────────────────────────────────────────
def load(df, db_name=DB_NAME):      #Write Dataframe to SQLite database
    conn = sqlite3.connect(db_name)
    df.to_sql("weather_data", conn, if_exists="append", index=False)
    conn.close()
    print(f"Loaded {len(df)} rows into {db_name}")


#MAIN
#─────────────────────────────────────────────
if __name__ == "__main__":
    for city in CITIES:
        raw = extract(city)
        cleaned = transform(raw)
        load(cleaned)
        print(cleaned.head())
        time.sleep(2)
