# Vireo Audio Customer Support & Refund Intelligence

A Streamlit-based analytics dashboard for exploring customer support tickets, refund patterns, policy exceptions, SLA performance, data quality, and potential refund anomalies.

## Project Overview

This project transforms support and refund datasets into business insights through data cleaning, reconciliation, KPI analysis, interactive filtering, and downloadable reporting.

## Key Features

- **Data Ingestion:** Load and validate five datasets.
- **Data Cleaning:** Reconcile duplicate ticket IDs and normalize refund amounts.
- **Refund Analytics:** Explore refund value, reasons, products, teams, agents, and customers.
- **Policy Review:** Review refund-policy patterns and exceptions.
- **SLA Intelligence:** Examine service-level agreement breaches.
- **Business Summary:** Generate rule-based business insights.
- **Case Explorer:** Search and filter support cases.
- **Executive Dashboard:** Interactive global filters and KPIs.
- **Anomaly Detection:** Flag unusual cases for further review; flags do not prove fraud.
- **Data Quality Monitor:** Inspect missing values and other data-quality indicators.
- **Business Reports:** Download executive summaries and filtered data.

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Data analytics and visualization

## Project Structure

```text
vireo-support-intelligence/
├── app.py
├── requirements.txt
├── .gitignore
├── src/
│   ├── data_loader.py
│   ├── cleaning.py
│   └── analytics.py
└── data/
    └── CSV datasets
```

## Setup and Installation

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

## Responsible Interpretation

Anomaly flags identify cases for review and should not be treated as proof of fraud. Observed correlations or patterns do not independently establish causation. Review data quality and business context before making operational decisions.

## Data and Privacy

Do not publish confidential, personally identifiable, or otherwise sensitive customer information. Use synthetic, anonymized, or appropriately authorized sample datasets when sharing this project publicly.

## Author

Syed Shahed

AI & Data Science | Python | SQL | Power BI | Machine Learning | Generative AI
