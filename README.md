# StoreRadar Shopify cohort snapshots

This repository publishes small, reproducible, aggregate Shopify storefront-technology snapshots from [StoreRadar.co](https://storeradar.co/). It is intended for analysts, app teams, agencies, and ecommerce SaaS teams that need a dated comparison before prospecting or message testing.

## Current snapshot

The first snapshot was observed on **2026-09-14**. It contains 12 aggregate technology rows across three focused cohorts:

- storefront optimization
- reviews and social proof
- retention and CRM

The canonical StoreRadar pages remain the source of record. The public pages include the visible tables, observation dates, methodology limits, and machine-readable `Dataset`/`DataCatalog` metadata:

- [StoreRadar dataset catalog](https://storeradar.co/datasets/catalog)
- [Storefront optimization stack](https://storeradar.co/datasets/shopify-storefront-optimization-stack)
- [Reviews and social proof stack](https://storeradar.co/datasets/shopify-review-social-proof-stack)
- [Retention and CRM stack](https://storeradar.co/datasets/shopify-retention-crm-stack)

## Method and limits

Counts are observed public storefront technology signatures in a versioned StoreRadar snapshot. They are not vendor customer lists, verified subscriptions, buying intent, revenue, or proof of product quality. Store-level records, contact details, and decision-maker enrichment are not published here.

The snapshot CSV is a compact public mirror for reproducible analysis. If a value differs from a later StoreRadar page, use the page's observation date and canonical URL to identify the newer snapshot.

## Canonical page map

[`data/canonical-pages.csv`](data/canonical-pages.csv) mirrors the public `.co` URLs discoverable from StoreRadar's sitemap surfaces as observed on 2026-09-16. It includes the research, app-cohort, insight, and dataset routes without changing their canonical ownership.

## Citation

For a cohort row, cite the relevant canonical StoreRadar dataset page, its observation date, and this repository only as the open analysis mirror. Suggested format:

> StoreRadar, “Shopify storefront optimization technology stack,” aggregate snapshot observed 2026-09-14, https://storeradar.co/datasets/shopify-storefront-optimization-stack.

This repository is licensed under CC BY 4.0. See [LICENSE](LICENSE).
