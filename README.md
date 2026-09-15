# Inside the Funnel: Diagnosing Drop-off and Driving Conversion

### Product Analytics Case Study — Google Merchandise Store

## Overview

A product analytics case study analyzing user behavior across the Google Merchandise Store purchase funnel.

The project identifies major funnel drop-offs, evaluates conversion across acquisition sources and user segments, analyzes revenue concentration, prioritizes product opportunities, and proposes an A/B experiment to improve conversion.

**Analytical flow:**

> Funnel Diagnosis → User & Revenue Analysis → Opportunity Prioritization → Experiment Design

---

## Business Problem

The store attracts a large number of users, but only a small proportion ultimately purchase.

The analysis focuses on:

- Where users are dropping out of the funnel?
- Which funnel stage represents the largest opportunity?
- How conversion differs across acquisition sources, devices, countries, and engagement levels?
- Which user behaviors are associated with stronger conversion?
- Which product opportunity should be prioritized?
- How the highest-priority opportunity could be tested?

---

## Dataset

**Source:** Google Merchandise Store GA4 public e-commerce dataset

**Period:** November 2020 – January 2021

**Grain:** User-level aggregation

**Users analyzed:** 270,154

The working dataset contains user-level information on:

- Device category
- Country
- Traffic source
- Product views
- Add-to-cart activity
- Checkout activity
- Purchases
- Active days
- Session count
- Revenue

---

## Tools: 

SQL (BigQuery), Python (Pandas, NumPy, Matplotlib)

---

## Key Findings

- **Purchase conversion:** 1.64% across 270,154 users.
- **Largest funnel bottleneck:** View → Cart, with **20.47% progression** and **48,713 users** not reaching the cart stage.
- **Cart → Checkout:** 45.09% progression.
- **Checkout → Purchase:** 45.49% progression.
- **Device performance:** No statistically significant difference in purchase conversion across mobile, desktop, and tablet (p = 0.171).
- **Engagement:** High-engagement users show substantially higher conversion (**16.91%**) than low-engagement users (**0.55%**), although this represents an association rather than a causal effect.
- **Revenue concentration:** The top 20% of purchasers generate **54.28% of total revenue**.
- **Total revenue analyzed:** **$362,165**.

---

## Funnel Diagnosis

The primary product opportunity is the **View → Cart** stage.

```text
Product View
61,252 users
      ↓
20.47% progression
      ↓
Add to Cart
12,545 users
      ↓
45.09% progression
      ↓
Begin Checkout
9,715 users
      ↓
45.49% progression
      ↓
Purchase
4,419 users