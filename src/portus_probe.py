"""Probe the public Portus web app for station/API metadata hints.

This helper is for discovery only. It fetches public Portus HTML/JS assets and
prints snippets around likely API and station terms.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass

import requests


BASE_URL = "https://portus.puertos.es"
TERMS = (
    "api",
    "boya",
    "buoy",
    "estacion",
    "station",
    "latitud",
    "longitud",
    "observacion",
    "datos",
    "oleaje",
    "waves",
)


@dataclass(frozen=True)
class Snippet:
    source: str
    term: str
    index: int
    text: str


def _ascii(text: str) -> str:
    return text.encode("ascii", "backslashreplace").decode("ascii")


def fetch_text(path: str) -> str:
    response = requests.get(f"{BASE_URL}{path}", timeout=30)
    response.raise_for_status()
    return response.text


def extract_asset_paths(html: str) -> list[str]:
    paths = re.findall(r"(?:src|href)=([^\s>]+)", html)
    cleaned = []
    for path in paths:
        path = path.strip("\"'")
        if path.startswith("/js/") and path.endswith(".js"):
            cleaned.append(path)
    return sorted(set(cleaned))


def find_snippets(source: str, text: str) -> list[Snippet]:
    snippets: list[Snippet] = []
    lowered = text.lower()
    for term in TERMS:
        start = 0
        while True:
            index = lowered.find(term.lower(), start)
            if index == -1:
                break
            snippet = text[max(0, index - 180) : index + 300]
            snippets.append(Snippet(source, term, index, _ascii(snippet)))
            start = index + len(term)
            if len([item for item in snippets if item.term == term]) >= 5:
                break
    return snippets


def main() -> None:
    routes_only = "--routes-only" in sys.argv
    html = fetch_text("/")
    assets = extract_asset_paths(html)
    print("JS assets:")
    for asset in assets:
        print(f"- {asset}")

    route_candidates: set[str] = set()
    if not routes_only:
        print("\nSnippets:")
    for asset in assets:
        text = fetch_text(asset)
        for pattern in (
            r'resourceApi:"([^"]+)"',
            r'mapsResourceApi:"([^"]+)"',
            r'\.get\("([^"]+)"',
            r'\.post\("([^"]+)"',
        ):
            route_candidates.update(re.findall(pattern, text))
        if routes_only:
            continue
        snippets = find_snippets(asset, text)
        if not snippets:
            continue
        print(f"\n## {asset}")
        for snippet in snippets[:25]:
            print(f"[{snippet.term} @ {snippet.index}] {snippet.text}")

    print("\nRoute candidates:")
    for route in sorted(route_candidates):
        if any(term in route.lower() for term in ("estacion", "station", "data", "dato", "pred", "param", "last", "punto", "wave", "wana")):
            print(f"- {_ascii(route)}")


if __name__ == "__main__":
    main()
