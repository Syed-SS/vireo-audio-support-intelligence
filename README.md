<div align="center">

# Vireo Audio Intelligence

### Customer Support, Refund & SLA Analytics

An interactive Streamlit business-intelligence dashboard for analyzing customer-support operations, refund trends, policy-review cases, service-level performance, data quality, and potential refund anomalies.

<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/NumPy-Analytics-013243?logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Project-Portfolio%20Demo-2E8B57" alt="Portfolio demo">
</p>

</div>

---

## Overview

Vireo Audio Intelligence brings support-ticket and refund data into one interactive workspace. It helps users move from high-level operational metrics to individual case review through refund analytics, SLA monitoring, policy checks, anomaly screening, data-quality checks, and downloadable reports.

Built with **Python, Streamlit, Pandas, and NumPy**. The business summary uses rule-based insights calculated from the loaded data; it is not an external generative-AI integration.

## Dashboard Screenshots

Add your screenshots to a `screenshots/` folder and use these filenames, or update the image paths below to match your chosen filenames.

### 1. Executive Dashboard
Global filters, headline KPIs, refund-reason comparison, and monthly refund trends.

![Executive Dashboard](screenshots/executive-dashboard.png)

### 2. Refund Analytics
Refund KPIs, reason breakdown, and monthly refund trend.

![Refund Analytics](screenshots/refund-analytics.png)

### 3. SLA Intelligence
First-response performance and SLA breach analysis across channels, priorities, and support teams.

![SLA Intelligence](screenshots/sla-intelligence.png)

### 4. Policy Review
Goodwill-refund cases above the configured review cap and refund-plus-replacement cases for investigation.

![Policy Review](screenshots/policy-review.png)

### 5. Refund Anomaly Detection
IQR-based high-value refund screening. Flags indicate cases for review, not confirmed fraud.

![Refund Anomaly Detection](screenshots/anomaly-detection.png)

### 6. AI Business Summary
Rule-based business findings generated from refund and SLA metrics.

![AI Business Summary](screenshots/ai-business-summary.png)

### 7. Data Ingestion & Validation
Dataset loading status, row counts, column counts, and validation information.

![Data Ingestion and Validation](screenshots/data-ingestion.png)

### 8. Case Explorer
Search, filter, inspect, and export support-ticket records.

![Case Explorer](screenshots/case-explorer.png)

---

## Key Features

| Area | Capabilities |
|---|---|
| **Data ingestion & validation** | Loads five project datasets and displays basic validation details. |
| **Cleaning & reconciliation** | Ticket reconciliation, refund-amount normalization, and validation checks. |
| **Refund analytics** | Refund volume and value, refund rate, refund reasons, monthly trends, and breakdowns by product, team, agent, and customer. |
| **Policy review** | Flags goodwill refunds above the configured ₹500 review cap and surfaces refund-plus-replacement cases. |
| **SLA intelligence** | Calculates first-response time and evaluates applicable tickets against channel-specific SLA targets; summarizes breach counts and rates by channel, priority, team, and refund group. |
| **Executive dashboard** | Global channel, priority, team, and date filters for supported views. |
| **Business summary** | Rule-based findings from observed refund and SLA metrics. |
| **Refund anomaly screening** | Interquartile-range (IQR) threshold for identifying unusually high refund amounts for investigation. |
| **Data quality monitor** | Row counts, duplicate-ID checks, missing-value summaries, and validation output. |
| **Case explorer** | Ticket/customer search, filters, selected-case details, and CSV export. |
| **Business report exports** | Downloadable report and filtered-data outputs. |

## SLA Rules Used in This Project

The dashboard uses the following configured first-response targets by channel:

| Channel | Target first response |
|---|---:|
| Chat | 15 minutes |
| Voice | 120 minutes |
| Social | 240 minutes |
| Email | 480 minutes |

SLA results depend on the timestamps available in the dataset and the configured targets. Review these assumptions against the intended business policy before using the metrics for operational decisions.

## Technology Stack

- **Python** — application logic
- **Streamlit** — interactive dashboard
- **Pandas** — tabular data processing and analysis
- **NumPy** — numerical calculations

## Project Structure

```text
vireo-support-intelligence/
├── app.py
├── requirements.txt
├── src/
│   ├── analytics.py
│   ├── cleaning.py
│   └── data_loader.py
├── data/                         # Local datasets; not committed
└── screenshots/
    ├── executive-dashboard.png
    ├── refund-analytics.png
    ├── sla-intelligence.png
    ├── policy-review.png
    ├── anomaly-detection.png
    ├── ai-business-summary.png
    ├── data-ingestion.png
    └── case-explorer.png
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Syed-SS/vireo-audio-support-intelligence.git
cd vireo-audio-support-intelligence
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Add local datasets

Place the required CSV files in the project's `data/` directory using the filenames expected by `src/data_loader.py`.

The local data directory is excluded from Git. Do not commit real customer, ticket, or order information. Use synthetic, anonymized, or otherwise approved data for public demonstrations.

### 5. Launch the dashboard

```bash
python -m streamlit run app.py
```

Streamlit will print a local URL, typically `http://localhost:8501`.

## Analytical Notes & Responsible Interpretation

- **Anomaly flags are review signals, not proof of fraud.** The IQR threshold identifies unusually high values relative to the observed distribution.
- **Policy flags require context.** Goodwill refunds above the configured ₹500 cap should be checked against the applicable policy and approval evidence.
- **SLA results depend on configured targets and timestamps.** Validate the business rules before making operational decisions.
- **The business summary is rule-based.** It describes patterns in the loaded data and does not establish causation.
- **Protect customer information.** Keep private datasets out of public repositories and use approved or anonymized data for demonstrations.

## Author

**Syed Shahed**  
AI & Data Science | Analytics | Python | SQL | Power BI | Machine Learning

- GitHub: [Syed-SS](https://github.com/Syed-SS)
- LinkedIn: [Syed Shahed](https://www.linkedin.com/in/syedshahed-ai)

---

<div align="center">

**Built as an applied analytics portfolio project.**

</div>
