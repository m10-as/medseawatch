# Section 1 - CMEMS Dataset Discovery and Variable Selection

Date: 2026-07-05

## Objective

Confirm the Copernicus Marine products, dataset IDs, and variable names that
MedSeaWatch will use before any ingestion or modeling code is written.

## Tool Used

The live catalogue was queried with:

```powershell
python -m src.cmems_catalogue
```

This command uses `copernicusmarine.describe(...)` and does not download marine
data.

## Confirmed Products

| Component | Product ID | Product title |
|---|---|---|
| Waves | `MEDSEA_ANALYSISFORECAST_WAV_006_017` | Mediterranean Sea Waves Analysis and Forecast |
| Physics | `MEDSEA_ANALYSISFORECAST_PHY_006_013` | Mediterranean Sea Physics Analysis and Forecast |
| Biogeochemistry | `MEDSEA_ANALYSISFORECAST_BGC_006_014` | Mediterranean Sea Biogeochemistry Analysis and Forecast |

## Selected Version 1 Datasets

| Use | Dataset ID | Frequency/type | Selected variables |
|---|---|---|---|
| Wave forecasting and risk scoring | `cmems_mod_med_wav_anfc_4.2km_PT1H-i` | Hourly instantaneous, 2D | `VHM0`, `VTPK`, `VMDR` |
| SST anomaly detection | `cmems_mod_med_phy-tem_anfc_4.2km-2D_PT1H-m` | Hourly mean, 2D surface | `thetao` |
| Chlorophyll anomaly detection | `cmems_mod_med_bgc-pft_anfc_4.2km_P1D-m` | Daily mean, 3D | `chl` |
| Optional currents | `cmems_mod_med_phy-cur_anfc_4.2km-2D_PT1H-m` | Hourly mean, 2D surface | `uo`, `vo` |
| Optional salinity | `cmems_mod_med_phy-sal_anfc_4.2km-2D_PT1H-m` | Hourly mean, 2D surface | `so` |

## Variable Roles

| Variable | Role in project | Keep for V1? |
|---|---|---|
| `VHM0` | Main wave-height variable; target for forecasting and input to risk scoring | Yes |
| `VTPK` | Wave period feature; helps characterize sea state | Yes |
| `VMDR` | Wave direction feature; useful for maps and risk context | Yes |
| `thetao` | SST variable for anomaly detection | Yes |
| `chl` | Chlorophyll-a variable for anomaly detection | Yes |
| `uo`, `vo` | Surface current components; context and possible features | Optional |
| `so` | Surface salinity; possible ocean-state feature | Optional |

## Decision

For V1, MedSeaWatch will use a compact set of variables:

- Required wave variables: `VHM0`, `VTPK`, `VMDR`
- Required anomaly variables: `thetao`, `chl`
- Optional supporting variables: `uo`, `vo`, `so`

This keeps the scope focused enough for a laptop-friendly first build while
still supporting forecasting, risk scoring, anomaly detection, EDA, and an
interactive dashboard.

## Next Section

Section 2 will define the exact geographic region and select the initial buoy or
grid point for validation.
