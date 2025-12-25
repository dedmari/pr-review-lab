import pandas as pd
import pytest
from data_pipeline.etl import transform


def test_transform_dedup_keeps_latest():
    df = pd.DataFrame(
        [
            {"event_id": "e1", "event_ts": "2025-01-01T00:00:00Z", "amount": 10},
            {"event_id": "e1", "event_ts": "2025-01-01T00:02:00Z", "amount": 12},
        ]
    )
    out = transform(df)
    assert len(out) == 1
    assert float(out.iloc[0]["amount"]) == 12.0


def test_negative_amount_rejected():
    df = pd.DataFrame(
        [{"event_id": "e9", "event_ts": "2025-01-01T00:00:00Z", "amount": -1}]
    )
    with pytest.raises(ValueError):
        transform(df)


def test_missing_columns():
    df = pd.DataFrame([{"event_id": "e1", "event_ts": "2025-01-01T00:00:00Z"}])
    with pytest.raises(ValueError):
        transform(df)