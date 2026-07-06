# Data Dictionary

Last updated: 2026-07-06

This file records the confirmed Copernicus Marine and Portus/Puertos del Estado
variables selected during Sections 1-3.

## Region

Project region: Barcelona-Tarragona / Catalan Coast.

Version 1 bounding box from `config/config.yaml`:

| Field | Value |
|---|---:|
| Minimum longitude | 0.75 |
| Maximum longitude | 3.10 |
| Minimum latitude | 40.45 |
| Maximum latitude | 41.95 |

CRS: `EPSG:4326`.

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

## Portus / Puertos del Estado Buoy Variables

These fields were verified from the public Portus API in Section 3. Portus
returns raw values plus a `factor`; numeric values must be divided by `factor`
before analysis.

Primary station for V1 validation:

```text
1731 - Boya de Barcelona II
```

Backup stations:

```text
1712 - Boya de Tarragona
2720 - Boya de Tarragona offshore
```

| Field | Portus `paramEseoo` | Meaning | Units | Role |
|---|---|---|---:|---|
| `hm0` | `Hm0` | Significant wave height | m | Ground-truth wave-height target |
| `hmax` | `Hmax` | Maximum wave height | m | Extreme-wave context |
| `tp` | `Tp` | Peak period | s | Ground-truth wave-period feature |
| `tm02` | `Tm02` | Mean period Tm02 | s | Secondary wave-period feature |
| `dmd` | `MeanDir` | Mean wave direction of provenance | degree | Ground-truth wave-direction feature |
| `lat` | `Latitude` | Station latitude | degree | Station metadata/check |
| `lon` | `Longitude` | Station longitude | degree | Station metadata/check |

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

## Section 3 Decisions

- Use CMEMS programmatic subsetting for gridded wave, physics, and
  biogeochemistry data.
- Use Portus public endpoints for station metadata, wave parameter metadata, and
  latest observations.
- Use `1731 - Boya de Barcelona II` as the primary V1 validation station.
- Treat long historical buoy-observation export as a follow-up ingestion
  verification task; the Portus app exposes a request/cart flow rather than a
  confirmed direct historical download endpoint.

## Still To Verify

- Direct or documented export path for long historical buoy observations.
- Whether V1 training should use a multi-year/reanalysis product in addition to
  analysis-forecast products for longer historical coverage.
