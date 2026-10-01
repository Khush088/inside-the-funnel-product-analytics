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

* Where are users dropping out of the funnel?
* Which funnel stage represents the largest opportunity?
* How does conversion differ across acquisition sources, devices, countries, and engagement levels?
* Which user behaviors are associated with stronger conversion?
* Which product opportunity should be prioritized?
* How can the highest-priority opportunity be tested?

---

## Dataset

**Source:** Google Merchandise Store GA4 public e-commerce dataset

**Period:** November 2020 – January 2021

**Grain:** User-level aggregation

**Users analyzed:** 270,154

The working dataset contains user-level information on:

* Device category
* Country
* Traffic source
* Product views
* Add-to-cart activity
* Checkout activity
* Purchases
* Active days
* Session count
* Revenue

### Funnel Analysis Scope

The overall dataset contains **270,154 users**.

For funnel progression analysis, the population is restricted to the **61,252 users who viewed a product**, allowing progression through:

> Product View → Add to Cart → Begin Checkout → Purchase

This distinction is important because the overall purchase conversion rate and the funnel-stage conversion rates use different populations.

---

## Tools

* SQL (BigQuery)
* Python
* Pandas
* NumPy
* Matplotlib

---

## Key Findings

* **Overall purchase conversion:** 1.64% across 270,154 users.
* **Largest funnel bottleneck:** View → Cart, with **20.47% progression** and **48,713 users** not reaching the cart stage.
* **Cart → Checkout:** 45.09% progression.
* **Checkout → Purchase:** 45.49% progression.
* **Device performance:** No statistically significant difference in purchase conversion across mobile, desktop, and tablet (**p = 0.171**).
* **Engagement:** High-engagement users show substantially higher conversion (**16.91%**) than low-engagement users (**0.55%**). This represents an association rather than a causal effect.
* **Revenue concentration:** The top 20% of purchasers generate **54.28% of total revenue**.
* **Total revenue analyzed:** **$362,165**.

---

## Funnel Diagnosis

The primary product opportunity identified in the analysis is the **View → Cart** stage.

```text
Product View
61,252 users
      ↓
20.47% progression | 79.53% drop-off
      ↓
Add to Cart
12,545 users
      ↓
45.09% progression | 54.91% drop-off
      ↓
Begin Checkout
9,715 users
      ↓
45.49% progression | 54.51% drop-off
      ↓
Purchase
4,419 users
```

The largest loss occurs between **product viewing and adding an item to the cart**, making this stage the primary area for further product investigation.

---

## Key Product Opportunities

### 1. Improve Product View → Add-to-Cart Conversion

The largest funnel drop occurs before users add products to their cart.

Potential areas for investigation include:

* Product-page value proposition
* Product information and imagery
* Pricing visibility
* Product availability
* Add-to-cart CTA visibility
* Mobile product-page experience
* Friction in the product-selection process

These are hypotheses to investigate rather than confirmed root causes from the aggregated dataset.

### 2. Understand High-Engagement User Behavior

High-engagement users show substantially higher purchase conversion than low-engagement users.

Further analysis can investigate whether behaviors such as:

* Higher session frequency
* More active days
* Repeated product exploration

are associated with stronger purchase intent.

Because the dataset is observational, these relationships should not be interpreted as causal.

### 3. Evaluate Acquisition Quality

Conversion varies across acquisition sources and user segments.

Rather than optimizing purely for traffic volume, acquisition channels can be evaluated using:

> Traffic → Product Engagement → Cart Addition → Checkout → Purchase → Revenue

This helps distinguish channels that generate users from channels that generate commercially valuable users.

---

## Recommended Experiment

### Experiment: Improve Product Page → Add-to-Cart Conversion

**Hypothesis**

> Improving the product-page experience and making the add-to-cart action clearer will increase the percentage of product viewers who add an item to their cart.

### A/B Test

**Control:** Existing product-page experience

**Treatment:** Improved product-page experience with clearer product information and a more prominent add-to-cart CTA.

### Primary Metric

**Product View → Add-to-Cart Conversion Rate**

$$
\text{ATC Conversion} =
\frac{\text{Users Adding to Cart}}
{\text{Users Viewing Product}}
$$

### Secondary Metrics

* Checkout initiation rate
* Purchase conversion rate
* Revenue per user
* Average order value

### Guardrails

* Overall purchase conversion
* Revenue per user
* Checkout abandonment
* Page performance

The experiment should be evaluated using a statistically appropriate test with sufficient sample size before drawing conclusions.

---

## Limitations

* The analysis uses an **aggregated user-level GA4 dataset** rather than raw event-level clickstream data.
* Sequential event ordering and timestamp-level behavior cannot be reliably analyzed.
* Product-level analysis is outside the available dataset scope.
* The analysis identifies associations and patterns but does not establish causal relationships.
* The dataset represents a historical period from **November 2020 to January 2021** and may not reflect current Google Merchandise Store behavior.
* Funnel analysis is restricted to users who reached the product-view stage.

---

## Project Focus

This project demonstrates practical skills in:

**SQL Analysis • Funnel Analysis • Product Analytics • User Segmentation • Conversion Analysis • Revenue Analysis • Experiment Design • Business Recommendations**
