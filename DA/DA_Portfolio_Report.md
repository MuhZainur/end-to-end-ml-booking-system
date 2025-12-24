# British Airways Data Analysis: Portfolio Report

## 1. Executive Summary
**Project Name:** Customer Booking Behavior Analysis
**Role:** Data Analyst
**Goal:** Uncover the primary drivers of customer bookings and provide data-driven recommendations to improve the current 15% conversion rate.
**Tools Used:** Python (Pandas, Matplotlib, Seaborn), Scipy (Hypothesis Testing), Scikit-Learn (Clustering).

---

## 2. Business Problem Statement
British Airways faces a challenge where the majority of customer interactions (approx. 85%) do not result in a finalized booking. The stakeholders need to deeply understand **"Who bookings?"** and **"Why?"** to optimize their marketing spend and digital platform experience.

This analysis moves beyond simple reporting to answer specific strategic questions:
1.  Does the booking platform (Mobile vs. Website) impact success?
2.  Can we predict booking intent based on early user actions (e.g., selecting baggage)?
3.  Are there distinct "Customer Personas" we can target differently?

---

## 3. Methodology & Technical Approach
To ensure the insights are robust and actionable, a multi-layered analytical approach was used:

### A. Dimensional Analysis (Descriptive)
*   **Data Cleaning:** Handled duplicates and outliers in `purchase_lead` and `flight_duration`.
*   **Univariate & Bivariate Analysis:** Visualized conversion rates across Sales Channels, Trip Types, and Flight Days.

### B. Statistical Validation (Diagnostic)
*   **Hypothesis Testing (Chi-Square):** Used `scipy.stats` to scientifically prove that the relationship between variables (e.g., *Sales Channel* and *Booking*) is **statistically significant** (p-value < 0.05), removing "guesswork" from the insights.

---

## 4. Key Insights & "The Story"

### Insight 1: The Digital Experience Gap
*   **Finding:** The **Internet** (Website) sales channel has a significantly higher booking conversion rate compared to the **Mobile** app.
*   **Statistical Proof:** Chi-Square tests confirmed this discrepancy is not random.
*   **Business Implication:** There is likely significant **UI/UX friction** on the mobile application causing users to drop off before payment.

### Insight 2: "Investment" Signals High Intent
*   **Finding:** Users who interact with ancillary services—specifically **Extra Baggage** and **Preferred Seats**—are drastically more likely to complete a booking.
*   **Business Implication:** Comparing "Browsers" vs "Bookers", the act of customization acts as a psychological commitment. Upselling isn't just for revenue; it's a retention mechanic.

### Insight 3: The "Planning Horizon" Curve
*   **Finding:** Booking rates peak in the **1-3 month** lead time window. Very short lead times (<1 week) show high volume but lower consistency.
*   **Business Implication:** Marketing ad spend is most efficient when targeting users searching in that "sweet spot" window.

---

## 5. Strategic Recommendations
Based on the analysis, the following actions are recommended to the management team:

1.  **Mobile Task Force:** prioritization of a UX audit for the Mobile App checkout flow. Reducing friction here offers the highest ROI for conversion improvement.
2.  **Ancillary-First Design:** Experiment with A/B testing a flow where Seat Selection or Baggage options are presented *earlier* in the funnel to increase user psychological commitment.

---
*Created by **[MuhZainur]** - Data Scientist & ML Engineer*
