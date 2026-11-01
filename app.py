"""Flask dashboard for the ADRO GRU and historical-simulation VaR study."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from flask import Flask, render_template

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
if not OUTPUT_DIR.exists() and (BASE_DIR / "adro_gru_complete_outputs").exists():
    OUTPUT_DIR = BASE_DIR / "adro_gru_complete_outputs"
DATA_DIR = OUTPUT_DIR / "data"
PREDICTION_DIR = OUTPUT_DIR / "predictions"
VAR_DIR = OUTPUT_DIR / "var"
app = Flask(__name__)

FALLBACK = {
    "data_rows": 2541, "data_start": "2016-01-04", "data_end": "2026-04-30",
    "best_overall": "A_T5_U512_RMSPROP_B64", "forecast_price": 2517.709717,
    "var_percentage": 3.4776386404, "var_rupiah": 34776.386404,
}


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        header = pd.read_csv(path, nrows=0).columns
        return pd.read_csv(path, parse_dates=["Date"] if "Date" in header else None)
    except (OSError, ValueError, pd.errors.ParserError):
        return pd.DataFrame()


def load_state() -> dict:
    metadata = FALLBACK.copy()
    metadata_path = OUTPUT_DIR / "run_metadata.json"
    if metadata_path.exists():
        try:
            metadata.update(json.loads(metadata_path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError):
            pass
    data = read_csv(DATA_DIR / "adro_usdidr.csv")
    predictions = read_csv(PREDICTION_DIR / f"{metadata['best_overall']}_predictions.csv")
    if predictions.empty:
        predictions = read_csv(PREDICTION_DIR / "A_T5_U512_RMSPROP_B64_predictions.csv")
    var_summary = read_csv(VAR_DIR / "adro_var_summary.csv")
    forecast = {"date":"2026-05-01", "price":metadata["forecast_price"], "last_price":2520.0,
        "return_pct":-0.090884, "model":metadata["best_overall"], "features":"ADRO_Close",
        "rmse":84.667145, "mape":2.242001}
    forecast_file = read_csv(PREDICTION_DIR / "one_step_forecast_summary.csv")
    if not forecast_file.empty:
        row = forecast_file.iloc[-1].to_dict()
        forecast.update({"date":str(row.get("display_forecast_date", forecast["date"]))[:10],
            "price":row.get("predicted_next_ADRO_Close", forecast["price"]),
            "last_price":row.get("last_actual_ADRO_Close", forecast["last_price"]),
            "return_pct":float(row.get("predicted_simple_return", 0))*100,
            "model":row.get("experiment_id", forecast["model"]),
            "features":row.get("features", forecast["features"])})
    if not var_summary.empty:
        row = var_summary.iloc[-1]
        metadata["var_percentage"] = row.get("VaR_Percentage", metadata["var_percentage"])
        metadata["var_rupiah"] = row.get("VaR_Rupiah", metadata["var_rupiah"])
    return {"metadata":metadata, "history":data.tail(180).to_dict("records") if not data.empty else [],
        "predictions":predictions.tail(180).to_dict("records") if not predictions.empty else [],
        "latest":data.iloc[-1].to_dict() if not data.empty else {}, "forecast":forecast,
        "artifacts_ready":not data.empty}


@app.get("/")
def index():
    return render_template("index.html", **load_state())


if __name__ == "__main__":
    app.run(debug=True)
