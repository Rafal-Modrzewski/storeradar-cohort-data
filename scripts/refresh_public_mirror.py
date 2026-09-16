#!/usr/bin/env python3
"""Refresh the public StoreRadar evidence mirror from canonical .co pages.

This intentionally uses only public HTTP responses and the Python standard
library. It mirrors crawlable URLs and aggregate table facts; it never fetches
store-level rows, contacts, credentials, or application data.
"""

from __future__ import annotations

import csv
import datetime as dt
import html as html_lib
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen


BASE_URL = "https://storeradar.co"
SITEMAP_URL = f"{BASE_URL}/apps-sitemap.xml"
ROOT = Path(__file__).resolve().parents[1]
PAGES_PATH = ROOT / "data" / "canonical-pages.csv"
CURRENT_SNAPSHOT_PATH = ROOT / "data" / "current-cohort-snapshot.csv"

COHORT_BY_DATASET = {
    "shopify-customer-support-stack": "customer_support",
    "shopify-retention-crm-stack": "retention_crm",
    "shopify-review-social-proof-stack": "reviews_social_proof",
    "shopify-storefront-optimization-stack": "storefront_optimization",
    "shopify-visual-merchandising-stack": "visual_merchandising",
}


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "StoreRadarPublicMirror/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


def sitemap_urls(document: str) -> list[str]:
    return re.findall(r"<loc>([^<]+)</loc>", document)


def page_type(url: str) -> str:
    path = url.removeprefix(BASE_URL)
    if path == "/apps":
        return "app_directory"
    if path.startswith("/apps/insights/"):
        return "insight"
    if path.startswith("/apps/"):
        return "app_cohort"
    if path == "/datasets/catalog":
        return "dataset_catalog"
    if path.startswith("/datasets/"):
        return "dataset"
    if path == "/research":
        return "research_hub"
    return "research"


def text_without_markup(value: str) -> str:
    return re.sub(r"\s+", " ", html_lib.unescape(re.sub(r"<[^>]+>", "", value))).strip()


def dataset_metadata(document: str) -> dict[str, object]:
    match = re.search(
        r'<script type="application/ld\+json">(.*?)</script>', document, re.S
    )
    if match is None:
        raise RuntimeError("dataset_jsonld_missing")
    payload = json.loads(html_lib.unescape(match.group(1)))
    graph = payload.get("@graph", []) if isinstance(payload, dict) else []
    dataset = next(
        (
            item
            for item in graph
            if isinstance(item, dict)
            and (
                item.get("@type") == "Dataset"
                or "Dataset" in (item.get("@type") or [])
            )
        ),
        None,
    )
    if not isinstance(dataset, dict):
        raise RuntimeError("dataset_jsonld_item_missing")
    return dataset


def dataset_rows(document: str, dataset_slug: str, observation_date: str) -> list[dict[str, object]]:
    cohort = COHORT_BY_DATASET[dataset_slug]
    rows = []
    for app_name, raw_count in re.findall(
        r'<tr><th scope="row">(.*?)</th><td>([0-9,]+)</td><td>',
        document,
        re.S,
    ):
        rows.append(
            {
                "cohort": cohort,
                "technology": text_without_markup(app_name),
                "observed_storefronts": int(raw_count.replace(",", "")),
                "observation_date": observation_date,
                "canonical_source": f"{BASE_URL}/datasets/{dataset_slug}",
            }
        )
    if not rows:
        raise RuntimeError(f"dataset_table_missing:{dataset_slug}")
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    urls = sitemap_urls(fetch(SITEMAP_URL))
    if len(urls) < 20 or any(not url.startswith(f"{BASE_URL}/") for url in urls):
        raise RuntimeError("unexpected_sitemap_surface")
    if any(re.search(r"storeradar\.(?:io|com)", url) for url in urls):
        raise RuntimeError("non_canonical_domain_in_sitemap")

    observed_in_sitemap = dt.datetime.now(dt.timezone.utc).date().isoformat()
    page_rows = [
        {
            "page_type": page_type(url),
            "canonical_url": url,
            "observed_in_sitemap": "true",
            "source_sitemap": SITEMAP_URL,
            "observed_date": observed_in_sitemap,
        }
        for url in urls
    ]
    write_csv(
        PAGES_PATH,
        ["page_type", "canonical_url", "observed_in_sitemap", "source_sitemap", "observed_date"],
        page_rows,
    )

    all_rows: list[dict[str, object]] = []
    dataset_urls = [url for url in urls if "/datasets/" in url and not url.endswith("/catalog")]
    if set(dataset_urls) != {f"{BASE_URL}/datasets/{slug}" for slug in COHORT_BY_DATASET}:
        raise RuntimeError("dataset_sitemap_coverage_changed")
    for url in dataset_urls:
        slug = url.rsplit("/", 1)[-1]
        document = fetch(url)
        metadata = dataset_metadata(document)
        observation_date = str(metadata.get("temporalCoverage", ""))[:10]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", observation_date):
            raise RuntimeError(f"dataset_observation_date_missing:{slug}")
        all_rows.extend(dataset_rows(document, slug, observation_date))

    all_rows.sort(key=lambda row: (str(row["cohort"]), -int(row["observed_storefronts"]), str(row["technology"])))
    write_csv(
        CURRENT_SNAPSHOT_PATH,
        ["cohort", "technology", "observed_storefronts", "observation_date", "canonical_source"],
        all_rows,
    )
    print(f"refreshed_pages={len(page_rows)} refreshed_dataset_rows={len(all_rows)}")


if __name__ == "__main__":
    main()
