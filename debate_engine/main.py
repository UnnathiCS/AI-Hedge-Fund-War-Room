import pandas as pd
from engines.broker_engine import compute_broker_profiles
from engines.company_engine import compute_company_scores
from engines.weighting_engine import compute_weighted_ratings

df = pd.read_csv("debate_engine/dataset/final_dataset_cleaned.csv")

broker_profiles = compute_broker_profiles(df)
company_scores = compute_company_scores(df)
weighted_scores = compute_weighted_ratings(df, broker_profiles)

print(weighted_scores.sort_values("weighted_rating", ascending=False))