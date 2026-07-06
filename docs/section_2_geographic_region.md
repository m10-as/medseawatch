# Section 2 - Geographic Region Definition and Data Boundaries

Date: 2026-07-06

## Objective

Lock a laptop-friendly geographic boundary for Version 1 and define the first
validation target area before data ingestion starts.

## Region Decision

MedSeaWatch V1 will focus on the Barcelona-Tarragona / Catalan Coast segment in
the northwestern Mediterranean.

The Version 1 CMEMS subset box is:

| Boundary | Value |
|---|---:|
| Minimum longitude | 0.75 |
| Maximum longitude | 3.10 |
| Minimum latitude | 40.45 |
| Maximum latitude | 41.95 |
| CRS | EPSG:4326 |

This box is intentionally larger than the coastline line itself because CMEMS is
gridded marine data. We need enough offshore area to capture wave fields,
surface temperature patterns, chlorophyll patterns, and nearby model grid cells
for the dashboard.

## Reference Points

These points are not confirmed buoys. They are initial CMEMS extraction
reference points for testing small subsets.

| Name | Longitude | Latitude | Role |
|---|---:|---:|---|
| Barcelona nearshore | 2.25 | 41.30 | First CMEMS reference point |
| Tarragona nearshore | 1.35 | 41.05 | Backup CMEMS reference point |

## Validation Target Decision

The preferred validation target is a Puertos del Estado / Portus buoy in the
Barcelona buoy area. The backup target is a buoy in the Tarragona buoy area.

The exact station ID, coordinates, variables, and access path are deliberately
not filled in yet. They must be verified from Portus/Puertos del Estado during
Section 3 before we build ingestion code around them.

## Why This Boundary Works

- It covers the Barcelona-Tarragona project region while leaving enough offshore
  space for wave fields and chlorophyll/SST maps.
- It is small enough to keep CMEMS subsets manageable on a laptop.
- It supports two practical target areas: Barcelona first, Tarragona backup.
- It keeps the project focused on the chosen Catalan coast, instead of drifting
  into a broad Mediterranean analysis.

## Files Updated

- `config/config.yaml`
- `config/region.geojson`

## Sources To Use In The Next Section

- Copernicus Marine catalogue for gridded wave, physics, and biogeochemistry
  products.
- Portus by Puertos del Estado for Spanish buoy observations and station
  metadata.

## Next Section

Section 3 will verify the actual data access path:

- CMEMS subset command for the selected box.
- Portus/Puertos del Estado buoy station metadata and data export.
- Decision on whether buoy retrieval is programmatic or documented manual
  export.
