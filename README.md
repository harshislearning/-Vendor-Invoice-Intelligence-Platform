# 📦 Vendor Invoice Intelligence Platform

AI-driven freight cost forecasting and invoice risk detection for procurement & finance operations, built on vendor purchase/invoice data with a Streamlit dashboard front end.

## Modules

- **Freight Cost Prediction** (`freight_cost_prediction/`) — regression model estimating freight cost from invoice dollar value.
- **Invoice Risk Flagging** (`invoice_flagging/`) — Random Forest classifier (GridSearchCV-tuned) that flags invoices likely to need manual approval, based on cost/quantity/delivery-timing anomalies.
- **Inference** (`inference/`) — thin prediction wrappers used by the app.
- **App** (`app.py`) — Streamlit dashboard for interactive predictions.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Data

The models are trained from `Data/inventory.db`, a SQLite database of vendor purchases and invoices. It's excluded from this repo (424MB, over GitHub's 100MB file limit) — place your own `inventory.db` at `Data/inventory.db` before retraining.

Pretrained models are included in `models/`, so the app runs out of the box without the raw database.

## Train

```bash
python freight_cost_prediction/train.py
python invoice_flagging/train.py
```

## Run the app

```bash
streamlit run app.py
```
