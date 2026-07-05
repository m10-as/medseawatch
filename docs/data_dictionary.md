# Data Dictionary

Last updated: 2026-07-05

This file records the confirmed Copernicus Marine variables selected during
Section 1. The source of truth is the live `copernicusmarine describe` catalogue
queried through `src/cmems_catalogue.py`.

## Region

Project region: Barcelona-Tarragona / Catalan Coast.

Initial bounding box from `config/config.yaml`:

| Field | Value |
|---|---:|
| Minimum longitude | 0.5 |
| Maximum longitude | 3.5 |
| Minimum latitude | 40.0 |
| Maximum latitude | 42.0 |

This box will be refined in Section 2.

## Version 1 Essential Variables

| Variable | Meaning | Units | Product ID | Dataset ID | Role |
|---|---|---:|---|---|---|
| `VHM0` | Sea surface wave significant height | m | `MEDSEA_ANALYSISFORECAST_WAV_006_017` | `cmems_mod_med_wav_anfc_4.2km_PT1H-i` | Main wave forecasting target and risk-score input |
| `VTPK` | Sea surface wave period at variance spectral density maximum | s | `MEDSEA_ANALYSISFORECAST_WAV_006_017` | `cmems_mod_med_wav_anfc_4.2km_PT1H-i` | Wave-state feature |
| `VMDR` | Sea surface wave from direction | degree | `MEDSEA_ANALYSISFORECAST_WAV_006_017` | `cmems_mod_med_wav_anfc_4.2km_PT1H-i` | Directional wave feature and map context |
| `thetao` | Sea water potential temperature, used here as SST from the 2D surface dataset | degrees_C | `MEDSEA_ANALYSISFORECAST_PHY_006_013` | `cmems_mod_med_phy-tem_anfc_4.2km-2D_PT1H-m` | SST anomaly detection |
| `chl` | Mass concentration of chlorophyll-a in sea water | mg m-3 | `MEDSEA_ANALYSISFORECAST_BGC_006_014` | `cmems_mod_med_bgc-pft_anfc_4.2km_P1D-m` | Chlorophyll anomaly detection |

## Version 1 Supporting Variables

| Variable | Meaning | Units | Product ID | Dataset ID | Role |
|---|---|---:|---|---|---|
| `uo` | Eastward sea water velocity | m s-1 | `MEDSEA_ANALYSISFORECAST_PHY_006_013` | `cmems_mod_med_phy-cur_anfc_4.2km-2D_PT1H-m` | Optional current feature/context |
| `vo` | Northward sea water velocity | m s-1 | `MEDSEA_ANALYSISFORECAST_PHY_006_013` | `cmems_mod_med_phy-cur_anfc_4.2km-2D_PT1H-m` | Optional current feature/context |
| `so` | Sea water salinity | 0.001 | `MEDSEA_ANALYSISFORECAST_PHY_006_013` | `cmems_mod_med_phy-sal_anfc_4.2km-2D_PT1H-m` | Optional ocean-state feature |

## Optional Later Variables

| Variable | Meaning | Units | Product ID | Dataset ID | Possible use |
|---|---|---:|---|---|---|
| `VCMX` | Sea surface wave maximum height | m | `MEDSEA_ANALYSISFORECAST_WAV_006_017` | `cmems_mod_med_wav_anfc_4.2km_PT1H-i` | Extreme wave context |
| `VHM0_WW` | Sea surface wind-wave significant height | m | `MEDSEA_ANALYSISFORECAST_WAV_006_017` | `cmems_mod_med_wav_anfc_4.2km_PT1H-i` | Separate wind-wave signal |
| `VHM0_SW1` | Primary swell significant height | m | `MEDSEA_ANALYSISFORECAST_WAV_006_017` | `cmems_mod_med_wav_anfc_4.2km_PT1H-i` | Swell decomposition |
| `VTM02` | Sea surface wave mean period from second frequency moment | s | `MEDSEA_ANALYSISFORECAST_WAV_006_017` | `cmems_mod_med_wav_anfc_4.2km_PT1H-i` | Alternative wave-period feature |
| `zos` | Sea surface height above geoid | m | `MEDSEA_ANALYSISFORECAST_PHY_006_013` | `cmems_mod_med_phy-ssh_anfc_4.2km-2D_PT1H-m` | Optional sea-level context |
| `mlotst` | Ocean mixed layer thickness | m | `MEDSEA_ANALYSISFORECAST_PHY_006_013` | `cmems_mod_med_phy-mld_anfc_4.2km-2D_PT1H-m` | Optional physical-ocean context |
| `no3` | Nitrate concentration | mmol m-3 | `MEDSEA_ANALYSISFORECAST_BGC_006_014` | `cmems_mod_med_bgc-nut_anfc_4.2km_P1D-m` | Later biogeochemical enrichment |
| `o2` | Dissolved molecular oxygen concentration | mmol m-3 | `MEDSEA_ANALYSISFORECAST_BGC_006_014` | `cmems_mod_med_bgc-bio_anfc_4.2km_P1D-m` | Later biogeochemical enrichment |
| `ph` | Sea water pH on total scale | 1 | `MEDSEA_ANALYSISFORECAST_BGC_006_014` | `cmems_mod_med_bgc-car_anfc_4.2km_P1D-m` | Later biogeochemical enrichment |

## Section 1 Decisions

- Use the Mediterranean analysis-forecast products for the first discovery pass.
- Use hourly wave fields for the wave-risk component.
- Use hourly 2D surface temperature for SST anomaly detection.
- Use daily PFT/chlorophyll data for chlorophyll anomaly detection.
- Keep salinity and currents as supporting features, not required V1 targets.
- Do not include nutrient, oxygen, carbonate, or pH variables in V1 unless they
  become necessary after EDA.

## Still To Verify

- Puertos del Estado buoy data access and exact buoy variable names.
- Whether V1 training should use a multi-year/reanalysis product in addition to
  analysis-forecast products for longer historical coverage.
