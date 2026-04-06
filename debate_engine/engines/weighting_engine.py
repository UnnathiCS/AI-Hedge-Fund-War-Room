def compute_weighted_ratings(df, broker_profiles):

    df = df.merge(
        broker_profiles[["broker_clean", "reliability_score"]],
        on="broker_clean",
        how="left"
    )

    weighted = df.groupby("company").apply(
        lambda x: (
            x["rating_score"] *
            x["reliability_score"]
        ).sum() / x["reliability_score"].sum()
    ).reset_index(name="weighted_rating")

    return weighted