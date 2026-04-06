import pandas as pd
import numpy as np

def compute_broker_profiles(df):

    broker = df.groupby("broker_clean").agg({
        "rating_score": ["count", "mean", "std"],
        "stance_change": "mean"
    })

    broker.columns = [
        "total_reports",
        "bias_index",
        "rating_volatility",
        "avg_stance_changes"
    ]

    broker = broker.reset_index()

    broker["reliability_score"] = (
        (1 / broker["rating_volatility"].replace(0, 0.0001)) *
        (1 / broker["avg_stance_changes"].replace(0, 0.0001))
    )

    return broker