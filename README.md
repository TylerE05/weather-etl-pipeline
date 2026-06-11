---

## 🧠 How It Works

The pipeline is split into 4 clean functions, each with one job:

**1. `extract(city)`**
Sends an HTTP request to the Weatherstack API with the city name as a parameter. Gets back a JSON response — a raw nested dictionary full of weather data.

**2. `transform(raw)`**
Takes that messy dictionary and flattens it into a clean pandas DataFrame. Also creates new columns that weren't in the original data — like converting Celsius to Fahrenheit, flagging cold temperatures, and recording exactly when the pipeline ran.

**3. `load(df)`**
Takes the clean DataFrame and writes it to a SQLite database file (`weatherstack.db`). Uses `append` mode so every run adds new rows — building a history of weather data over time.

**4. `report()`**
Reads the latest run back out of the database and prints a formatted summary to the terminal so you can see what was loaded.

The `run_pipeline()` function ties all four together, loops over every city, and handles errors so one failed city doesn't stop the rest.

---

## 📦 Sample Data

What a single row looks like after it's been loaded into the database:

| city | country | temp_c | temp_f | humidity_pct | wind_kph | description | feels_cold | pipeline_run |
|---|---|---|---|---|---|---|---|---|
| Orlando | United States | 31 | 87.8 | 65 | 14 | Sunny | False | 2026-05-29 22:24:33 |
| New York | United States | 18 | 64.4 | 55 | 20 | Partly cloudy | False | 2026-05-29 22:24:35 |
| Los Angeles | United States | 22 | 71.6 | 60 | 10 | Clear | False | 2026-05-29 22:24:37 |

Each pipeline run appends new rows — so the longer it runs, the more historical data you accumulate.

---

## 💡 What I Learned

- **ETL architecture** — how to separate extraction, transformation, and loading into distinct, reusable functions
- **REST APIs** — how to authenticate with an API key, pass query parameters, and parse JSON responses
- **pandas** — flattening nested JSON into DataFrames, creating derived columns, type conversions
- **SQLite** — connecting to a local database, writing DataFrames with `.to_sql()`, querying with `pd.read_sql()`
- **Error handling** — using `try/except` so individual failures don't crash the whole pipeline
- **API rate limiting** — why `time.sleep()` matters in production pipelines
- **Secure credential management** — storing API keys in `.env` files and never committing them to GitHub
- **Data modeling** — thinking ahead about append vs replace, and how schema design affects historical analysis

---

## 🚀 Future Improvements

- [ ] Schedule pipeline to run hourly automatically using the `schedule` library
- [ ] Add email or Slack alert when extreme weather is detected (`feels_cold` or `high_wind`)
- [ ] Export weekly summary report to CSV
- [ ] Migrate from SQLite to PostgreSQL for production-scale storage
- [ ] Add more cities and a config file to manage them
- [ ] Deploy to AWS Lambda to run in the cloud on a timer
- [ ] Build a simple dashboard with Streamlit to visualize live data
- [ ] Write unit tests for `transform()` using `pytest`

---

## 🛠️ How to Run

### Prerequisites
- Python 3.8+
- A free API key from [weatherstack.com](https://weatherstack.com)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/weather-etl-pipeline.git
cd weather-etl-pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your .env file
cp .env.example .env
# Open .env and replace your_api_key_here with your real Weatherstack key

# 4. Run the pipeline
python pipeline.py

# 5. Explore the database
python query.py

# 6. Generate charts (requires matplotlib)
python visualize.py
```

### Customizing cities
Open `pipeline.py` and edit the `CITIES` list at the top:
```python
CITIES = ["Orlando", "New York", "Los Angeles", "Miami", "Chicago"]
```
Any city name recognized by Weatherstack will work.
