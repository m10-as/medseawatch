# Section 3 - Data Ingestion Plan

Date: 2026-07-06

## Objective

Verify the practical ingestion path for CMEMS data and Puertos del Estado /
Portus buoy data before building the full pipeline.

## CMEMS Ingestion

The CMEMS subset path is verified.

Smoke-test dataset:

| Field | Value |
|---|---|
| Dataset | `cmems_mod_med_wav_anfc_4.2km_PT1H-i` |
| Variable | `VHM0` |
| Time window | `2026-07-01 00:00:00` to `2026-07-01 01:00:00` |
| Longitude window requested | `0.75` to `3.10` |
| Latitude window requested | `40.45` to `41.95` |
| Output | `data/raw/cmems_smoke/wave_vhm0_smoke_20260701.nc` |

Dry-run result:

- CMEMS accepted the request.
- Estimated file size: about `0.02 MB`.
- Estimated transfer size: about `7.58 MB`.
- Actual selected grid extent:
  - Longitude: `0.750000536441803` to `3.083333969116211`
  - Latitude: `40.47916793823242` to `41.9375`
  - Time: `2026-07-01T00:00:00Z` to `2026-07-01T01:00:00Z`

Actual download result:

- Request status: successful.
- File size on disk: `31,150` bytes.
- Verified with `xarray` using `engine="h5netcdf"`.
- Dimensions:
  - `time`: `2`
  - `latitude`: `36`
  - `longitude`: `57`
- Variables: `VHM0`

Important Windows note:

The `netCDF4` engine failed to open the smoke-test file from this workspace path
because the project folder contains a special dash character. The `h5netcdf`
engine opened it correctly. For this project, use:

```python
xarray.open_dataset(path, engine="h5netcdf")
```

## Portus / Puertos del Estado Access

The public Portus app uses this API base:

```text
https://portus.puertos.es/portussvr/api
```

Verified public endpoints:

| Purpose | Method | Endpoint |
|---|---|---|
| Real-time wave station metadata | GET | `estaciones/rt/WAVE` |
| Historical wave station metadata | GET | `estaciones/hist/WAVE` |
| Station variable families | GET | `estaciones/variables/{station_id}` |
| Wave parameter metadata | POST | `parametros/{station_id}?locale=es` with body `["WAVE"]` |
| Latest wave observations | POST | `lastData/station/{station_id}?locale=es` with body `["WAVE"]` |

The app also exposes a historical data request route:

```text
solicitudDatos/registraSolicitud?locale={locale}
```

That route appears to register a data request/cart submission with user
information. It is not yet confirmed as a direct historical observation download
endpoint. For the first modeling dataset, we should plan either:

- a documented Portus/Banco de Datos export, or
- a later implementation of the request/cart flow if it returns files reliably.

## Candidate Buoys

The following stations are inside the Section 2 region box and expose wave
metadata through Portus.

| Station ID | Name | Lon | Lat | Network | Depth m | First record | Cadence min | Current status |
|---:|---|---:|---:|---:|---:|---|---:|---|
| `1731` | Boya de Barcelona II | `2.20` | `41.32` | `1` | `68.0` | `2004-03-08 00:00:00.000` | `60` | Latest wave data verified |
| `1712` | Boya de Tarragona | `1.19` | `41.07` | `1` | `15.0` | `1992-11-12 00:00:00.000` | `60` | Latest wave data verified |
| `2720` | Boya de Tarragona offshore | `1.47` | `40.69` | `2` | `688.0` | `2004-08-20 14:00:00.000` | `60` | Latest wave data verified |

Primary V1 validation station:

```text
1731 - Boya de Barcelona II
```

Backup stations:

```text
1712 - Boya de Tarragona
2720 - Boya de Tarragona offshore
```

## Latest Wave Data Verification

All three candidate stations returned a latest wave payload on 2026-07-06.

Example variables available from `lastData/station/{station_id}`:

| Portus field | Meaning | Unit handling |
|---|---|---|
| `hm0` | Significant wave height | divide raw value by `factor` |
| `hmax` | Maximum wave height | divide raw value by `factor` |
| `tp` | Peak period | divide raw value by `factor` |
| `tm02` | Mean period Tm02 | divide raw value by `factor` |
| `dmd` | Mean wave direction | factor usually `1` |
| `lat` | Station latitude | factor `1` |
| `lon` | Station longitude | factor `1` |

## Code Added

- `src/ingest.py`
  - loads config
  - builds CMEMS subset calls
  - includes a one-hour wave smoke-test helper
- `src/portus_api.py`
  - lists Portus wave stations
  - filters station candidates by bounding box
  - reads station variable/parameter metadata
  - reads latest wave observations
- `src/portus_probe.py`
  - probes the public Portus app bundles for route discovery

## Section 3 Decision

Use CMEMS programmatic subsetting for gridded data.

Use Portus public API endpoints for:

- wave station metadata,
- station variable metadata,
- latest wave observations.

For historical buoy observations, do not claim a direct download API yet.
Treat historical training data as a verified access task in the next ingestion
iteration: either documented Portus/Banco de Datos export or implementation of
the Portus request/cart flow after testing.

## Next Section

Section 4 will design raw storage and DuckDB tables around:

- CMEMS NetCDF files,
- Portus station metadata,
- Portus latest/historical wave observations,
- future processed Parquet tables.
