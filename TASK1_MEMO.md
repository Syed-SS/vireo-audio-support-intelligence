# Task 1 Memo: Vireo Audio Customer Support & Refund Intelligence

**Author:** Syed Shahed  
**Project:** Vireo Audio Customer Support & Refund Intelligence  
**Repository:** https://github.com/Syed-SS/vireo-audio-support-intelligence  
**Date:** October 10, 2026

## 1. Executive Summary

I built an interactive Python and Streamlit analytics dashboard to help investigate customer-support performance, refund patterns, SLA breaches, policy-review cases, and potentially unusual refund amounts.

The dashboard combines data validation, refund analytics, channel-specific SLA monitoring, rule-based policy checks, IQR-based anomaly screening, case exploration, and downloadable reports.

The primary objective is to make operational information easier to investigate and support better prioritization. The project is a decision-support prototype; it does not automatically approve refunds, establish fraud, or demonstrate verified financial savings.

## 2. Observed Results

On the current dataset, the dashboard reports:

| Metric | Observed result |
|---|---:|
| Support tickets | 11,600 |
| Refund tickets | 2,340 |
| Total recorded refund value | ₹67,09,932 |
| Average refund amount | ₹2,867.49 |
| Potential refund anomalies flagged | 110 |
| Refund value associated with flagged anomalies | ₹9,24,240 |
| SLA breaches | 1,060 |
| Overall SLA breach rate | 9.14% |

These are analytical results from the available dataset, not independently verified company-wide figures. The refund value associated with flagged anomalies is not confirmed fraud, recovered money, or realized savings.

The expected business benefit is improved visibility and faster prioritization of cases for human review. Time saved and financial impact have not yet been measured in a live workflow.

## 3. Operating Cost

The application uses local Python-based analytics and rule-based logic. It does not make paid external AI or LLM API calls during normal dashboard operation.

Assuming approximately 650 tickets per week:

- Monthly volume: 650 × 52 ÷ 12 ≈ 2,817 tickets.
- Paid AI/API cost per run: ₹0.
- Estimated monthly paid AI/API cost: 2,817 × ₹0 = ₹0.

This estimate covers paid AI/API usage only. It excludes hosting, infrastructure, storage, maintenance, and engineering time.

## 4. Validation and Reliability

I reviewed dashboard aggregates and the implemented data-validation, refund-analysis, SLA, policy-rule, and anomaly-screening outputs against the available dataset.

The anomaly screening uses the Interquartile Range (IQR) method to identify unusually high refund values. The configured first-response targets are 15 minutes for chat, 120 minutes for voice, 240 minutes for social, and 480 minutes for email.

A formal benchmark against independently labelled cases has not been completed. Therefore, I cannot report a verified overall error rate, precision, or recall.

Potential failure cases include legitimate high-value refunds being flagged as anomalies, missing or inconsistent timestamps affecting SLA results, and policy exceptions requiring context not available in the underlying data.

## 5. Scope Decisions

I kept the solution focused on transparent, interpretable analytics rather than automatic refund decisions or a generative-AI workflow. The business summary is rule-based, and anomaly screening is statistical rather than a trained machine-learning model.

This approach avoids paid inference API usage and makes the displayed rules easier to inspect. A production version would require business-owner approval of policies, validation against labelled cases, appropriate access controls, and operational monitoring.

## 6. Known Limitations

- The dashboard is a prototype, not a production-integrated support platform.
- Results depend on source-data quality, timestamps, and configured business rules.
- No independent ground-truth evaluation or verified error rate is available.
- Anomaly flags require human investigation and do not establish fraud.
- Financial savings and operational time savings have not been measured.
- Production authentication, role-based access, scheduled refresh, and deployment hardening are outside the current scope.

## 7. Additional Work

Beyond headline metrics, the dashboard brings together data-quality monitoring, case-level exploration, CSV export, policy-review rules, and statistical anomaly screening. These features help an analyst move from high-level indicators to records that need investigation.

## 8. AI Usage

I used ChatGPT as a development assistant for planning, troubleshooting, and documentation support. Python, Streamlit, Pandas, and NumPy implement the application's analytical functionality.

The deployed dashboard does not call a paid external LLM or AI API at runtime. Its business summary is rule-based, and its IQR anomaly screening is a statistical technique.

## 9. Handover Notes

To run the application locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Ensure the required CSV files are available in the expected local `data/` directory. Review data-validation results before interpreting the dashboard, and confirm policy thresholds and SLA targets with the business owner before operational use.

The repository README documents the project structure, features, screenshots, and setup process.

## Conclusion

Vireo Audio Customer Support & Refund Intelligence provides a unified analytics interface for exploring refund activity, support SLAs, data quality, and cases requiring further review. The current deliverable demonstrates the analytical workflow; production readiness and measurable business impact remain future validation steps.