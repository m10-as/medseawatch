"""Data ingestion utilities for MedSeaWatch."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import copernicusmarine
import yaml


CONFIG_PATH = Path("config/config.yaml")


def load_config(path: str | Path = CONFIG_PATH) -> dict[str, Any]:
    """Load the project configuration file."""
    with Path(path).open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def get_region_bounds(config: dict[str, Any]) -> dict[str, float]:
    """Return the configured geographic bounds for CMEMS subsetting."""
    region = config["region"]
    return {
        "minimum_longitude": float(region["longitude_min"]),
        "maximum_longitude": float(region["longitude_max"]),
        "minimum_latitude": float(region["latitude_min"]),
        "maximum_latitude": float(region["latitude_max"]),
    }


def subset_cmems(
    dataset_id: str,
    variables: list[str],
    start_datetime: str,
    end_datetime: str,
    output_directory: str | Path,
    output_filename: str,
    *,
    dry_run: bool = False,
    file_format: str = "netcdf",
    overwrite: bool = True,
) -> copernicusmarine.ResponseSubset:
    """Download or dry-run a CMEMS subset using the configured region."""
    config = load_config()
    bounds = get_region_bounds(config)
    return copernicusmarine.subset(
        dataset_id=dataset_id,
        variables=variables,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        output_directory=Path(output_directory),
        output_filename=output_filename,
        file_format=file_format,
        coordinates_selection_method="inside",
        overwrite=overwrite,
        dry_run=dry_run,
        disable_progress_bar=True,
        **bounds,
    )


def smoke_test_wave_subset(dry_run: bool = True) -> copernicusmarine.ResponseSubset:
    """Run the Section 3 one-hour wave subset smoke test."""
    config = load_config()
    cmems = config["data_sources"]["copernicus_marine"]
    return subset_cmems(
        dataset_id=cmems["wave_dataset_hourly"],
        variables=["VHM0"],
        start_datetime="2026-07-01 00:00:00",
        end_datetime="2026-07-01 01:00:00",
        output_directory="data/raw/cmems_smoke",
        output_filename="wave_vhm0_smoke_20260701.nc",
        dry_run=dry_run,
    )
