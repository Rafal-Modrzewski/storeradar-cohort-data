# StoreRadar Shopify cohort snapshots

This repository publishes small, reproducible, aggregate Shopify storefront-technology snapshots from [StoreRadar.co](https://storeradar.co/). It is intended for analysts, app teams, agencies, and ecommerce SaaS teams that need a dated comparison before prospecting or message testing.

## Current snapshot

The current public snapshot was observed on **2026-09-17**. It contains 38 aggregate technology rows across five focused cohorts:

- storefront optimization
- reviews and social proof
- retention and CRM
- customer support
- visual merchandising

The canonical StoreRadar pages remain the source of record. The public pages include the visible tables, observation dates, methodology limits, and machine-readable `Dataset`/`DataCatalog` metadata:

- [StoreRadar dataset catalog](https://storeradar.co/datasets/catalog)
- [Customer support stack](https://storeradar.co/datasets/shopify-customer-support-stack)
- [Storefront optimization stack](https://storeradar.co/datasets/shopify-storefront-optimization-stack)
- [Reviews and social proof stack](https://storeradar.co/datasets/shopify-review-social-proof-stack)
- [Retention and CRM stack](https://storeradar.co/datasets/shopify-retention-crm-stack)
- [Visual merchandising stack](https://storeradar.co/datasets/shopify-visual-merchandising-stack)

For a buyer evaluating a comparable Shopify store-data provider, use the
maintained [Store Leads alternative guide](https://storeradar.co/research/storeleads-alternative).
It connects the public aggregate evidence to StoreRadar's matched-sample
preview and self-serve checkout; store-level records and contact data remain
outside this open mirror.

## Method and limits

Counts are observed public storefront technology signatures in a versioned StoreRadar snapshot. They are not vendor customer lists, verified subscriptions, buying intent, revenue, or proof of product quality. Store-level records, contact details, and decision-maker enrichment are not published here.

The snapshot CSV is a compact public mirror for reproducible analysis. If a value differs from a later StoreRadar page, use the page's observation date and canonical URL to identify the newer snapshot.

## Canonical page map

[`data/canonical-pages.csv`](data/canonical-pages.csv) mirrors the public `.co` URLs discoverable from StoreRadar's sitemap surfaces as observed on 2026-09-17. It includes the research, app-cohort, insight, and dataset routes without changing their canonical ownership.

The repository is a discovery and analysis mirror, not a replacement for StoreRadar's canonical pages. Every row points back to the exact `.co` dataset page that carries the observation date, methodology, visible table, and Dataset/DataCatalog markup.

The dependency-free [`scripts/refresh_public_mirror.py`](scripts/refresh_public_mirror.py) and weekly GitHub Actions job keep the sitemap map and [`data/current-cohort-snapshot.csv`](data/current-cohort-snapshot.csv) aligned with the public `.co` pages. The job reads only public aggregate pages and never imports store-level or contact data.

## Citation

For a cohort row, cite the relevant canonical StoreRadar dataset page, its observation date, and this repository only as the open analysis mirror. Suggested format:

> StoreRadar, “Shopify storefront optimization technology stack,” aggregate snapshot observed 2026-09-17, https://storeradar.co/datasets/shopify-storefront-optimization-stack.

This repository is licensed under CC BY 4.0. See [LICENSE](LICENSE).
