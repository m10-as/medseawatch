"""Small Portus API client for station metadata and latest observations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


BASE_URL = "https://portus.puertos.es/portussvr/api"


@dataclass(frozen=True)
class StationCandidate:
    station_id: int
    name: str
    longitude: float
    latitude: float
    network_id: int
    sensor_type: str | None
    model: str | None
    depth_m: float | None
    first_record: str | None
    last_record: str | None
    cadence_minutes: int | None
    incident: str | None
    available: bool


def _get(path: str, **params: Any) -> Any:
    response = requests.get(f"{BASE_URL}/{path}", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def _post(path: str, payload: Any, **params: Any) -> Any:
    response = requests.post(f"{BASE_URL}/{path}", params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def list_wave_stations(kind: str = "hist", locale: str = "es") -> list[dict[str, Any]]:
    """Return Portus wave station metadata.

    Parameters
    ----------
    kind:
        Use ``hist`` for historical station metadata or ``rt`` for real-time
        stations.
    """
    if kind not in {"hist", "rt"}:
        raise ValueError("kind must be 'hist' or 'rt'")
    return _get(f"estaciones/{kind}/WAVE", locale=locale)


def station_variables(station_id: int, locale: str = "es") -> list[str]:
    """Return available variable families for a station."""
    return _get(f"estaciones/variables/{station_id}", locale=locale)


def wave_parameters(station_id: int, locale: str = "es") -> list[dict[str, Any]]:
    """Return wave parameter metadata for a station."""
    return _post(f"parametros/{station_id}", ["WAVE"], locale=locale)


def latest_wave_data(station_id: int, locale: str = "es") -> dict[str, Any]:
    """Return latest wave observation payload for a station."""
    return _post(f"lastData/station/{station_id}", ["WAVE"], locale=locale)


def filter_station_candidates(
    stations: list[dict[str, Any]],
    *,
    min_lon: float,
    max_lon: float,
    min_lat: float,
    max_lat: float,
) -> list[StationCandidate]:
    """Filter station metadata to a bounding box."""
    candidates: list[StationCandidate] = []
    for station in stations:
        longitude = float(station["longitud"])
        latitude = float(station["latitud"])
        if not (min_lon <= longitude <= max_lon and min_lat <= latitude <= max_lat):
            continue
        candidates.append(
            StationCandidate(
                station_id=int(station["id"]),
                name=station["nombre"],
                longitude=longitude,
                latitude=latitude,
                network_id=int(station["redId"]),
                sensor_type=station.get("tipoSensor"),
                model=station.get("modeloEstacion"),
                depth_m=station.get("altitudProfundidad"),
                first_record=station.get("fechaAlta"),
                last_record=station.get("fechaFin"),
                cadence_minutes=station.get("cadencia"),
                incident=station.get("incidencia"),
                available=bool(station.get("disponible")),
            )
        )
    return candidates


def latest_wave_values(station_id: int) -> dict[str, float | str | None]:
    """Return latest wave values scaled by their published factors."""
    payload = latest_wave_data(station_id)
    values: dict[str, float | str | None] = {"fecha": payload.get("fecha")}
    for item in payload.get("datos", []):
        column = item.get("nombreColumna")
        raw_value = item.get("valor")
        factor = item.get("factor") or 1
        if raw_value is None:
            values[column] = None
            continue
        try:
            values[column] = float(raw_value) / float(factor)
        except (TypeError, ValueError):
            values[column] = raw_value
    return values
