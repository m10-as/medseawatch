"""Summarize selected Copernicus Marine catalogue products.

This module only reads catalogue metadata. It does not download marine data.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

import copernicusmarine


PRODUCT_IDS = [
    "MEDSEA_ANALYSISFORECAST_WAV_006_017",
    "MEDSEA_ANALYSISFORECAST_PHY_006_013",
    "MEDSEA_ANALYSISFORECAST_BGC_006_014",
]


@dataclass(frozen=True)
class VariableSummary:
    short_name: str
    standard_name: str
    units: str


@dataclass(frozen=True)
class DatasetSummary:
    product_id: str
    product_title: str
    dataset_id: str
    dataset_name: str
    variables: tuple[VariableSummary, ...]


def _iter_services(dataset: dict) -> Iterable[dict]:
    for version in dataset.get("versions", []):
        for part in version.get("parts", []):
            yield from part.get("services", [])


def _summarize_dataset(product: dict, dataset: dict) -> DatasetSummary:
    variables: dict[str, VariableSummary] = {}

    for service in _iter_services(dataset):
        for variable in service.get("variables", []):
            short_name = variable.get("short_name", "")
            if not short_name or short_name in variables:
                continue
            variables[short_name] = VariableSummary(
                short_name=short_name,
                standard_name=variable.get("standard_name", ""),
                units=variable.get("units", ""),
            )

    return DatasetSummary(
        product_id=product["product_id"],
        product_title=product["title"],
        dataset_id=dataset["dataset_id"],
        dataset_name=dataset["dataset_name"],
        variables=tuple(sorted(variables.values(), key=lambda item: item.short_name)),
    )


def summarize_products(product_ids: Iterable[str] = PRODUCT_IDS) -> list[DatasetSummary]:
    summaries: list[DatasetSummary] = []

    for product_id in product_ids:
        catalogue = copernicusmarine.describe(
            product_id=product_id,
            disable_progress_bar=True,
            raise_on_error=True,
        )
        product = catalogue.products[0].model_dump()
        for dataset in product.get("datasets", []):
            summaries.append(_summarize_dataset(product, dataset))

    return summaries


def main() -> None:
    grouped: dict[str, list[DatasetSummary]] = defaultdict(list)
    for summary in summarize_products():
        grouped[summary.product_id].append(summary)

    for product_id, datasets in grouped.items():
        print(product_id)
        print(f"  title: {datasets[0].product_title}")
        for dataset in datasets:
            print(f"  dataset: {dataset.dataset_id}")
            print(f"    name: {dataset.dataset_name}")
            print("    variables:")
            for variable in dataset.variables:
                print(
                    "      "
                    f"{variable.short_name} | {variable.standard_name} | {variable.units}"
                )


if __name__ == "__main__":
    main()
