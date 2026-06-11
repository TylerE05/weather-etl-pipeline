import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

DB_NAME = "weatherstack.db"
OUTPUT_DIR = "charts"


#HELPER  – load data from SQLite
#─────────────────────────────────────────────
def load_data() -> pd.DataFrame:
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM weather_data", conn)
    conn.close()
    df["pipeline_run"] = pd.to_datetime(df["pipeline_run"])
    return df


#Scatter: humidity vs temperature
#─────────────────────────────────────────────
def scatter_chart(df: pd.DataFrame) -> None:
    cities = df["city"].unique()
    palette = ["#4a9eff", "#f59e0b", "#22c55e", "#f43f5e",
               "#a855f7", "#06b6d4", "#fb923c"]

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    for i, city in enumerate(cities):
        city_df = df[df["city"] == city]
        color = palette[i % len(palette)]
        ax.scatter(city_df["temp_f"], city_df["humidity_pct"],
                   label=city, color=color, s=80, alpha=0.85, zorder=3)

    ax.set_title("Humidity vs Temperature", color="white",
                 fontsize=14, fontweight="bold", pad=16)
    ax.set_xlabel("Temperature (°F)", color="#94a3b8", fontsize=10)
    ax.set_ylabel("Humidity (%)", color="#94a3b8", fontsize=10)
    ax.tick_params(colors="white", labelsize=9)
    ax.grid(color="#1e293b", linewidth=0.8, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.legend(frameon=True, facecolor="#1e293b", edgecolor="#334155",
              labelcolor="white", fontsize=9)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "scatter_chart.png")
    plt.savefig(path, dpi=150, facecolor=fig.get_facecolor())
    plt.close()
    print(f"  ✓  Saved {path}")


#MAIN
#─────────────────────────────────────────────
if __name__ == "__main__":
    if not os.path.exists(DB_NAME):
        print(f"No database found. Run pipeline.py first.")
    else:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        df = load_data()
        print(f"\n▶  Generating charts from {len(df)} rows in {DB_NAME}\n")
        scatter_chart(df)
        print(f"\n  Charts saved to ./{OUTPUT_DIR}/\n")