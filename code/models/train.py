import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def main():
    # Load processed data
    train = pd.read_csv("data/processed/train.csv")
    test = pd.read_csv("data/processed/test.csv")

    print("Train loaded:", train.shape)
    print("Test loaded:", test.shape)

    # Separate features and target
    X_train = train.drop(columns=["price"])
    y_train = train["price"]

    X_test = test.drop(columns=["price"])
    y_test = test["price"]

    categorical_features = [
        "airline",
        "source_city",
        "departure_time",
        "stops",
        "arrival_time",
        "destination_city",
        "class",
    ]

    numerical_features = [
        "duration",
        "days_left",
    ]

    # Convert categorical values into numbers
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
            (
                "numerical",
                "passthrough",
                numerical_features,
            ),
        ]
    )

    # Simple regression model
    model = LinearRegression()

    # Preprocessing + model in one pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    print("Training model...")

    pipeline.fit(X_train, y_train)

    print("Model trained.")

    # Predict on test data
    predictions = pipeline.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print("\nMetrics:")
    print("MAE:", mae)
    print("RMSE:", rmse)
    print("R2:", r2)

    # Save trained pipeline
    os.makedirs("models", exist_ok=True)

    joblib.dump(
        pipeline,
        "models/flight_price_model.pkl",
    )

    print("\nModel saved to models/flight_price_model.pkl")


if __name__ == "__main__":
    main()