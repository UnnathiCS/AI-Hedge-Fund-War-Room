def compute_company_scores(df):

    company = df.groupby("company").agg({
        "rating_score": ["mean", "std"],
        "broker_clean": "nunique"
    })

    company.columns = [
        "avg_company_rating",
        "disagreement_index",
        "broker_count"
    ]

    company = company.reset_index()

    company["normalized_disagreement"] = (
        company["disagreement_index"] /
        company["disagreement_index"].max()
    )

    company["consensus_strength"] = (
        company["avg_company_rating"] *
        (1 - company["normalized_disagreement"])
    )

    return company