import pandas as pd
from pathlib import Path

def remove_price_outliers(df):
    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    df = df[
        (df["price"] >= lower_bound)
        & (df["price"] <= upper_bound)
    ]

    return df


def main():
    print("Loading dataset...")

    df = pd.read_csv("data/raw/flights.csv")
    print("Dataset loaded.")

    df = df.sample(
        n=50000,
        random_state=42
    )
    print("Dataset sampled.")

    print("Initial shape:", df.shape)

    # Remove identifier column
    df = df.drop(columns=["flight"])

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Handle missing values
    df = df.dropna()

    # Remove price outliers
    df = remove_price_outliers(df)

    print("Shape after cleaning:", df.shape)

    # Shuffle data
    df = df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    # 80% train, 20% test
    split_index = int(len(df) * 0.8)

    train = df.iloc[:split_index]
    test = df.iloc[split_index:]

    Path("data/processed").mkdir(parents=True, exist_ok=True)

    train.to_csv("data/processed/train.csv", index=False)
    test.to_csv("data/processed/test.csv", index=False)

    print("Train shape:", train.shape)
    print("Test shape:", test.shape)

    print("Processed data saved successfully.")


if __name__ == "__main__":
    main()
