from __future__ import annotations
import pandas as pd

REQUIRED_COLS = {"event_id", "event_ts", "amount"}


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")

    df["event_ts"] = pd.to_datetime(df["event_ts"], utc=True, errors="raise")
    df["amount"] = pd.to_numeric(df["amount"], errors="raise")

    df = df.sort_values("event_ts").drop_duplicates(subset=["event_id"], keep="last")

    if (df["amount"] < 0).any():
        raise ValueError("amount must be non-negative")

    return df[["event_id", "event_ts", "amount"]]


def run(input_csv: str, output_parquet: str) -> None:
    df = pd.read_csv(input_csv)
    out = transform(df)
    out.to_parquet(output_parquet, index=False)