# MedSeaWatch

Coastal Marine Risk Intelligence Platform for forecasting dangerous sea
conditions and detecting ocean anomalies along the Barcelona-Tarragona /
Catalan Coast.

## Project Scope

Version 1 focuses on two components:

- Wave and marine-risk forecasting.
- Sea surface temperature and chlorophyll anomaly detection.

The project will use Copernicus Marine Service data, Spanish buoy/weather data
where available, DuckDB for analytical storage, and Streamlit for the dashboard.

## Current Status

Section 0 is in progress:

- Local project skeleton created.
- Python environment: `medseawatch` with Python 3.11.
- Core packages installed by the user.
- Copernicus Marine access smoke test pending/started.

## Planned Architecture

Data sources -> raw storage -> cleaned Parquet -> DuckDB analytical layer ->
feature engineering -> modeling -> evaluation -> Streamlit dashboard ->
GitHub documentation.

## Main Folders

- `app/`: Streamlit application.
- `data/`: raw, interim, and processed datasets.
- `notebooks/`: exploratory analysis and modeling notebooks.
- `src/`: reusable pipeline code.
- `models/`: saved model artifacts.
- `reports/`: figures and technical report.
- `config/`: project configuration.
- `docs/`: project documentation.

