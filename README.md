# Flight Price MLOps Pipeline

## Project Overview

This project implements a simple end-to-end MLOps pipeline for flight price prediction.

The pipeline includes three main stages:

1. Data Engineering
2. Model Engineering
3. Deployment

The model predicts flight ticket prices based on flight information such as airline, source city, destination city, departure time, number of stops, class, duration, and days left before departure.

The complete pipeline can be launched manually with one script and can also run automatically every 5 minutes.

---

## Pipeline Stages

### Stage 1: Data Engineering

The raw flight dataset is loaded from:

```text
data/raw/flights.csv
```

The preprocessing stage performs:

- sampling of the raw dataset
- removal of the flight identifier column
- removal of duplicate rows
- removal of missing values
- removal of price outliers using the IQR method
- train/test split

The processed datasets are saved to:

```text
data/processed/train.csv
data/processed/test.csv
```

The preprocessing code is located in:

```text
code/datasets/preprocess.py
```

### Stage 2: Model Engineering

The training stage loads the processed train and test datasets.

Categorical features are encoded using `OneHotEncoder`.

The model used in this project is:

```text
Linear Regression
```

The trained preprocessing pipeline and model are saved together in:

```text
models/flight_price_model.pkl
```

The model is evaluated using:

- MAE
- RMSE
- R²

Example metrics:

```text
MAE: 4512.77
RMSE: 6638.55
R²: 0.9143
```

The training code is located in:

```text
code/models/train.py
```

### Stage 3: Deployment

The trained model is deployed using:

- FastAPI for the prediction API
- Streamlit for the web application
- Docker for containerization
- Docker Compose for running the API and app together

The API and the web application run in separate Docker containers.

The Streamlit application sends user input to the FastAPI prediction endpoint and displays the predicted flight price.

---

## Project Structure

```text
flight-price-mlops/
├── code/
│   ├── datasets/
│   │   └── preprocess.py
│   ├── models/
│   │   └── train.py
│   └── deployment/
│       ├── api/
│       │   ├── main.py
│       │   └── Dockerfile
│       ├── app/
│       │   ├── app.py
│       │   └── Dockerfile
│       └── docker-compose.yml
├── data/
│   ├── raw/
│   │   └── flights.csv
│   └── processed/
├── models/
├── requirements.txt
├── run_pipeline.sh
├── setup_automation.sh
├── .gitignore
└── README.md
```

---

## Requirements

The project was developed using Python 3.11.

Required software:

- Python 3.11
- Docker
- Docker Compose

---

## Setup

Clone the repository:

```bash
git clone https://github.com/ariiagaf/flight-price-mlops.git
cd flight-price-mlops
```

Create a virtual environment:

```bash
python3.11 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Start Docker Services

Build and start the API and Streamlit containers:

```bash
docker compose -f code/deployment/docker-compose.yml up -d --build
```

Check running containers:

```bash
docker compose -f code/deployment/docker-compose.yml ps
```

---

## Run the Complete Pipeline

Run all three stages with:

```bash
./run_pipeline.sh
```

The script performs:

```text
Data Engineering
        ↓
Model Training and Evaluation
        ↓
Model Packaging
        ↓
API Restart
```

A successful run ends with:

```text
=== Pipeline completed successfully ===
```

---

## API

FastAPI documentation is available at:

```text
http://localhost:8000/docs
```

The prediction endpoint is:

```text
POST /predict
```

Example request:

```json
{
  "airline": "Vistara",
  "source_city": "Delhi",
  "departure_time": "Morning",
  "stops": "zero",
  "arrival_time": "Afternoon",
  "destination_city": "Mumbai",
  "flight_class": "Economy",
  "duration": 2.25,
  "days_left": 10
}
```

Example response:

```json
{
  "predicted_price": 2241.46
}
```

The exact prediction may vary depending on the trained model.

---

## Web Application

The Streamlit application is available at:

```text
http://localhost:8501
```

The user can select or enter flight information and click:

```text
Predict price
```

The application sends the data to the FastAPI service and displays the predicted flight price.

---

## Automation

The complete pipeline is configured to run automatically every 5 minutes.

To install the automation:

```bash
./setup_automation.sh
```

On macOS, the script uses `launchd`.

On Linux, the script uses `cron`.

The automation launches `run_pipeline.sh` every 300 seconds.

Pipeline output is written to:

```text
pipeline.log
```

Errors are written to:

```text
pipeline_error.log
```

---

## Verify Automation

On macOS, check the registered job with:

```bash
launchctl print gui/$(id -u)/com.flightprice.pipeline
```

To manually trigger the scheduled pipeline:

```bash
launchctl kickstart -k gui/$(id -u)/com.flightprice.pipeline
```

Then check the log:

```bash
tail -n 50 pipeline.log
```

A successful automated run should contain:

```text
=== Pipeline completed successfully ===
```

---

## Stop Docker Services

To stop the API and application:

```bash
docker compose -f code/deployment/docker-compose.yml down
```

---

## Technologies

- Python
- pandas
- scikit-learn
- FastAPI
- Streamlit
- Docker
- Docker Compose
- launchd / cron

---

## Model

The project uses Linear Regression because the main goal of the assignment is to demonstrate a complete automated MLOps workflow rather than complex model optimization.

The saved scikit-learn pipeline includes both feature preprocessing and the regression model, which allows the API to directly accept raw feature values and generate predictions.

---

## Result

The project implements a complete automated MLOps workflow:

```text
Raw flight data
      ↓
Data preprocessing
      ↓
Train / Test split
      ↓
Feature engineering
      ↓
Model training
      ↓
Model evaluation
      ↓
Saved model
      ↓
FastAPI
      ↓
Streamlit
      ↓
Flight price prediction
```
