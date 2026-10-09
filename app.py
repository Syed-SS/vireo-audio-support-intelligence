import streamlit as st
import pandas as pd
from src.data_loader import load_all_datasets
from src.cleaning import (
    reconcile_tickets,
    get_reconciliation_summary,
    normalize_refund_amounts,
    validate_cleaned_data,
)
from src.analytics import (
    calculate_refund_kpis,
    analyze_refund_reasons,
    analyze_monthly_refunds,
    analyze_product_refunds,
    analyze_team_refunds,
    analyze_agent_refunds,
    analyze_customer_refunds,
    get_customer_refund_summary,
    analyze_gw_other,
)

# PAGE CONFIG
st.set_page_config(
    page_title="Vireo Audio Intelligence",
    page_icon="📊",
    layout="wide",
)

# TITLE
st.title("Vireo Audio Customer Support & Refund Intelligence")
st.write("AI-assisted customer support, refund, policy and SLA analytics.")

# STEP 5B — DATA INGESTION
st.header("5B — Data Ingestion")

if st.button("Load Vireo Data", type="primary") or st.session_state.get("vireo_data_loaded", False):
    st.session_state["vireo_data_loaded"] = True
    try:
        # STEP 5B — LOAD DATA
        datasets = load_all_datasets()
        st.success("All five Vireo datasets loaded successfully.")

        # DATASET VALIDATION
        st.subheader("Dataset Validation")
        for name, df in datasets.items():
            st.write(f"### ✅ {name.title()}.csv")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Rows", f"{len(df):,}")
            with col2:
                st.metric("Columns", f"{len(df.columns):,}")

        # STEP 5C — CLEANING & RECONCILIATION
        st.header("5C — Cleaning & Reconciliation")

        # 5C.1 — DUPLICATE RECONCILIATION
        original_tickets = datasets["tickets"]
        cleaned_tickets = reconcile_tickets(original_tickets)
        reconciliation = get_reconciliation_summary(
            original_tickets, cleaned_tickets
        )

        st.subheader("5C.1 — Duplicate Reconciliation")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Original Tickets",
                f"{reconciliation['original_rows']:,}",
            )
        with col2:
            st.metric(
                "Canonical Tickets",
                f"{reconciliation['unique_ticket_ids']:,}",
            )
        with col3:
            st.metric(
                "Duplicates Removed",
                f"{reconciliation['duplicate_rows_removed']:,}",
            )
        st.success("Duplicate reconciliation completed successfully.")

        # 5C.2 — MONEY NORMALIZATION
        cleaned_tickets = normalize_refund_amounts(cleaned_tickets)
        datasets["tickets"] = cleaned_tickets
        st.subheader("5C.2 — Money Normalization")
        total_refund = cleaned_tickets["refund_amount_inr"].fillna(0).sum()
        st.metric("Normalized Refund Value", f"₹{total_refund:,.2f}")
        st.success("Money normalization completed successfully.")

        # 5C.3 — FINAL DATA VALIDATION
        validation = validate_cleaned_data(cleaned_tickets)
        st.subheader("5C.3 — Final Data Validation")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Duplicate Ticket IDs",
                f"{validation['duplicate_ticket_ids']:,}",
            )
        with col2:
            st.metric(
                "Refund Without Reason",
                f"{validation['refund_without_reason']:,}",
            )
        with col3:
            st.metric(
                "Reason Without Refund",
                f"{validation['reason_without_refund']:,}",
            )

        col4, col5 = st.columns(2)
        with col4:
            st.metric("Negative Refunds", f"{validation['negative_refunds']:,}")
        with col5:
            st.metric("Zero Refunds", f"{validation['zero_refunds']:,}")

        all_checks_passed = all(value == 0 for value in validation.values())
        if all_checks_passed:
            st.success("All final data-quality validation checks passed.")
        else:
            st.warning("Some data-quality checks require review.")

        # STEP 5D — REFUND ANALYTICS
        st.header("5D — Refund Analytics")

        # 5D.1 — BASIC REFUND KPIs
        kpis = calculate_refund_kpis(cleaned_tickets)
        st.subheader("5D.1 — Basic Refund KPIs")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tickets", f"{kpis['total_tickets']:,}")
        with col2:
            st.metric("Refund Tickets", f"{kpis['refund_tickets']:,}")
        with col3:
            st.metric("Total Refund Value", f"₹{kpis['total_refund_value']:,.2f}")
        with col4:
            st.metric("Refund Rate", f"{kpis['refund_rate']:.2f}%")
        st.metric("Average Refund", f"₹{kpis['average_refund']:,.2f}")

        # 5D.2 — REFUND REASON ANALYSIS
        reason_analysis = analyze_refund_reasons(cleaned_tickets)
        st.subheader("5D.2 — Refund Reason Analysis")
        display_reason_analysis = reason_analysis.copy()
        display_reason_analysis["refund_value"] = display_reason_analysis[
            "refund_value"
        ].map(lambda x: f"₹{x:,.2f}")
        display_reason_analysis["refund_value_pct"] = display_reason_analysis[
            "refund_value_pct"
        ].map(lambda x: f"{x:.2f}%")
        st.dataframe(
            display_reason_analysis,
            use_container_width=True,
            hide_index=True,
        )

        # 5D.3 — MONTHLY REFUND TREND
        monthly_analysis = analyze_monthly_refunds(cleaned_tickets)
        st.subheader("5D.3 — Monthly Refund Trend")
        display_monthly = monthly_analysis.copy()
        display_monthly["refund_value"] = display_monthly["refund_value"].map(
            lambda x: f"₹{x:,.2f}"
        )
        st.dataframe(
            display_monthly,
            use_container_width=True,
            hide_index=True,
        )
        st.line_chart(monthly_analysis.set_index("month")[["refund_value"]])

        # 5D.4 — PRODUCT REFUND ANALYSIS
        product_analysis = analyze_product_refunds(
            cleaned_tickets, datasets["products"]
        )
        st.subheader("5D.4 — Product Refund Analysis")
        display_product = product_analysis.copy()
        display_product["refund_value"] = display_product["refund_value"].map(
            lambda x: f"₹{x:,.2f}"
        )
        display_product["refund_value_pct"] = display_product[
            "refund_value_pct"
        ].map(lambda x: f"{x:.2f}%")
        st.dataframe(
            display_product,
            use_container_width=True,
            hide_index=True,
        )

        # 5D.5 — TEAM REFUND ANALYSIS
        team_analysis = analyze_team_refunds(cleaned_tickets)
        st.subheader("5D.5 — Team Refund Analysis")
        display_team = team_analysis.copy()
        display_team["refund_value"] = display_team["refund_value"].map(
            lambda x: f"₹{x:,.2f}"
        )
        display_team["refund_value_pct"] = display_team["refund_value_pct"].map(
            lambda x: f"{x:.2f}%"
        )
        st.dataframe(
            display_team,
            use_container_width=True,
            hide_index=True,
        )

        # 5D.6 — AGENT REFUND ANALYSIS
        agent_analysis = analyze_agent_refunds(
            cleaned_tickets, datasets["agents"]
        )
        st.subheader("5D.6 — Agent Refund Analysis")
        display_agent = agent_analysis.copy()
        display_agent["refund_value"] = display_agent["refund_value"].map(
            lambda x: f"₹{x:,.2f}"
        )
        display_agent["refund_value_pct"] = display_agent[
            "refund_value_pct"
        ].map(lambda x: f"{x:.2f}%")
        st.dataframe(
            display_agent,
            use_container_width=True,
            hide_index=True,
        )

        # 5D.7 — CUSTOMER REFUND ANALYSIS
        customer_analysis = analyze_customer_refunds(cleaned_tickets)
        customer_summary = get_customer_refund_summary(cleaned_tickets)
        st.subheader("5D.7 — Customer Refund Analysis")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Refund Customers",
                f"{customer_summary['refund_customers']:,}",
            )
        with col2:
            st.metric(
                "Repeat Customers (2+)",
                f"{customer_summary['repeat_customers']:,}",
            )
        with col3:
            st.metric(
                "Customers with 3+ Refunds",
                f"{customer_summary['three_plus_customers']:,}",
            )
        with col4:
            st.metric(
                "Repeat Refund Value",
                f"₹{customer_summary['repeat_refund_value']:,.2f}",
            )
        st.metric(
            "Repeat Refund Value %",
            f"{customer_summary['repeat_refund_pct']:.2f}%",
        )
        display_customer_analysis = customer_analysis.copy()
        display_customer_analysis["refund_value"] = display_customer_analysis[
            "refund_value"
        ].map(lambda x: f"₹{x:,.2f}")
        st.dataframe(
            display_customer_analysis.head(20),
            use_container_width=True,
            hide_index=True,
        )

        # 5D.8 — GW-OTHER INTELLIGENCE
        gw_analysis = analyze_gw_other(cleaned_tickets)
        st.subheader("5D.8 — GW-OTHER Intelligence")
        display_gw_analysis = gw_analysis.copy()
        display_gw_analysis["refund_value"] = display_gw_analysis[
            "refund_value"
        ].map(lambda x: f"₹{x:,.2f}")
        display_gw_analysis["ticket_pct"] = display_gw_analysis[
            "ticket_pct"
        ].map(lambda x: f"{x:.2f}%")
        display_gw_analysis["refund_value_pct"] = display_gw_analysis[
            "refund_value_pct"
        ].map(lambda x: f"{x:.2f}%")
        st.dataframe(
            display_gw_analysis,
            use_container_width=True,
            hide_index=True,
        )
                # STEP 5E — POLICY REVIEW
        st.header("5E — Policy Review")

        # 5E.1 — GOODWILL REVIEW
        st.subheader("5E.1 — Goodwill Credit Review")
        refund_df = cleaned_tickets[
            pd.to_numeric(
                cleaned_tickets["refund_amount_inr"],
                errors="coerce",
            ).fillna(0) > 0
        ].copy()

        gw_df = refund_df[
            refund_df["refund_reason_code"]
            .astype(str)
            .str.upper()
            .eq("GW-OTHER")
        ].copy()

        gw_df["refund_amount_inr"] = pd.to_numeric(
            gw_df["refund_amount_inr"], errors="coerce"
        ).fillna(0)

        goodwill_over_cap = gw_df[
            gw_df["refund_amount_inr"] > 500
        ].copy()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("GW-OTHER Refund Tickets", f"{len(gw_df):,}")
        with col2:
            st.metric("Above ₹500 Cap", f"{len(goodwill_over_cap):,}")
        with col3:
            st.metric(
                "Above-Cap Refund Value",
                f"₹{goodwill_over_cap['refund_amount_inr'].sum():,.2f}",
            )

        if not goodwill_over_cap.empty:
            st.warning(
                "These GW-OTHER cases exceed the ₹500 goodwill cap "
                "and should be reviewed for Team Lead approval evidence."
            )
            display_goodwill = goodwill_over_cap[
                [
                    "ticket_id",
                    "customer_id",
                    "refund_amount_inr",
                    "refund_reason_code",
                ]
            ].copy()
            display_goodwill["refund_amount_inr"] = display_goodwill[
                "refund_amount_inr"
            ].map(lambda x: f"₹{x:,.2f}")
            st.dataframe(
                display_goodwill.head(50),
                use_container_width=True,
                hide_index=True,
            )

        # 5E.2 — REFUND + REPLACEMENT REVIEW
        st.subheader("5E.2 — Refund + Replacement Review")
        replacement_column = None
        possible_replacement_columns = [
            "replacement",
            "replacement_flag",
            "replacement_issued",
            "replacement_status",
        ]

        for column in possible_replacement_columns:
            if column in cleaned_tickets.columns:
                replacement_column = column
                break

        if replacement_column is not None:
            replacement_mask = (
                cleaned_tickets[replacement_column]
                .astype(str)
                .str.lower()
                .isin(["true", "1", "yes", "y", "replacement", "issued"])
            )
            refund_replacement = cleaned_tickets[
                (
                    pd.to_numeric(
                        cleaned_tickets["refund_amount_inr"],
                        errors="coerce",
                    ).fillna(0) > 0
                ) & replacement_mask
            ].copy()

            st.metric(
                "Refund + Replacement Cases",
                f"{len(refund_replacement):,}",
            )
            if not refund_replacement.empty:
                st.warning(
                    "Review these cases to confirm whether both a refund "
                    "and replacement were issued for the same order."
                )
                replacement_columns = [
                    "ticket_id",
                    "order_id",
                    "customer_id",
                    "refund_amount_inr",
                ]
                st.dataframe(
                    refund_replacement[
                        [
                            c for c in replacement_columns
                            if c in refund_replacement.columns
                        ]
                    ].head(50),
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            st.info(
                "No explicit replacement field is available in the ticket "
                "dataset. Refund + replacement cannot be confirmed."
            )

        # 5E.3 — POLICY REVIEW SUMMARY
        st.subheader("5E.3 — Policy Review Summary")
        policy_col1, policy_col2 = st.columns(2)
        with policy_col1:
            st.metric("GW-OTHER Above ₹500", f"{len(goodwill_over_cap):,}")
        with policy_col2:
            st.metric(
                "Policy Review Status",
                "Review Required" if len(goodwill_over_cap) > 0 else "No Flag",
            )
        st.caption(
            "Exceeding the goodwill cap is a review flag, not a confirmed "
            "violation when approval evidence is unavailable."
        )

        # STEP 5F — SLA INTELLIGENCE
        st.header("5F — SLA Intelligence")
        st.subheader("5F.1 — SLA Performance")

        sla_targets = {
            "chat": 15,
            "voice": 120,
            "social": 240,
            "email": 480,
        }

        sla_df = cleaned_tickets.copy()
        sla_df["created_at"] = pd.to_datetime(
            sla_df["created_at"], errors="coerce"
        )
        sla_df["first_response_at"] = pd.to_datetime(
            sla_df["first_response_at"], errors="coerce"
        )
        sla_df["response_minutes"] = (
            sla_df["first_response_at"] - sla_df["created_at"]
        ).dt.total_seconds() / 60
        sla_df["sla_minutes"] = (
            sla_df["channel"].astype(str).str.lower().map(sla_targets)
        )

        sla_applicable = sla_df[
            sla_df["response_minutes"].notna()
            & sla_df["sla_minutes"].notna()
        ].copy()

        sla_applicable["sla_breach"] = (
            sla_applicable["response_minutes"] > sla_applicable["sla_minutes"]
        )
        total_sla_tickets = len(sla_applicable)
        total_breaches = int(sla_applicable["sla_breach"].sum())
        overall_breach_rate = (
            total_breaches / total_sla_tickets * 100
            if total_sla_tickets > 0 else 0
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Applicable SLA Tickets", f"{total_sla_tickets:,}")
        with col2:
            st.metric("SLA Breaches", f"{total_breaches:,}")
        with col3:
            st.metric("Overall Breach Rate", f"{overall_breach_rate:.2f}%")

        # 5F.2 — SLA BY CHANNEL
        st.subheader("5F.2 — SLA by Channel")
        channel_sla = (
            sla_applicable.groupby("channel")
            .agg(
                tickets=("ticket_id", "count"),
                sla_breaches=("sla_breach", "sum"),
            )
            .reset_index()
        )
        channel_sla["breach_rate_pct"] = (
            channel_sla["sla_breaches"] / channel_sla["tickets"] * 100
        )
        display_channel_sla = channel_sla.copy()
        display_channel_sla["breach_rate_pct"] = display_channel_sla[
            "breach_rate_pct"
        ].map(lambda x: f"{x:.2f}%")
        st.dataframe(
            display_channel_sla,
            use_container_width=True,
            hide_index=True,
        )

        # 5F.3 — SLA BY PRIORITY
        st.subheader("5F.3 — SLA by Priority")
        priority_sla = (
            sla_applicable.groupby("priority")
            .agg(
                tickets=("ticket_id", "count"),
                sla_breaches=("sla_breach", "sum"),
            )
            .reset_index()
        )
        priority_sla["breach_rate_pct"] = (
            priority_sla["sla_breaches"] / priority_sla["tickets"] * 100
        )
        display_priority_sla = priority_sla.copy()
        display_priority_sla["breach_rate_pct"] = display_priority_sla[
            "breach_rate_pct"
        ].map(lambda x: f"{x:.2f}%")
        st.dataframe(
            display_priority_sla,
            use_container_width=True,
            hide_index=True,
        )

        # 5F.4 — SLA BY TEAM
        st.subheader("5F.4 — SLA by Team")
        if "assigned_team" in sla_applicable.columns:
            team_sla = (
                sla_applicable.groupby("assigned_team")
                .agg(
                    tickets=("ticket_id", "count"),
                    sla_breaches=("sla_breach", "sum"),
                )
                .reset_index()
            )
            team_sla["breach_rate_pct"] = (
                team_sla["sla_breaches"] / team_sla["tickets"] * 100
            )
            display_team_sla = team_sla.copy()
            display_team_sla["breach_rate_pct"] = display_team_sla[
                "breach_rate_pct"
            ].map(lambda x: f"{x:.2f}%")
            st.dataframe(
                display_team_sla.sort_values(
                    "sla_breaches", ascending=False
                ),
                use_container_width=True,
                hide_index=True,
            )

        # 5F.5 — SLA VS REFUND
        st.subheader("5F.5 — SLA Breach vs Refund")
        sla_refund = sla_applicable.copy()
        sla_refund["refund_amount_inr"] = pd.to_numeric(
            sla_refund["refund_amount_inr"], errors="coerce"
        ).fillna(0)
        sla_refund["refund_ticket"] = sla_refund["refund_amount_inr"] > 0
        sla_refund_group = (
            sla_refund.groupby("sla_breach")
            .agg(
                tickets=("ticket_id", "count"),
                refund_tickets=("refund_ticket", "sum"),
                total_refund_inr=("refund_amount_inr", "sum"),
            )
            .reset_index()
        )
        sla_refund_group["refund_rate_pct"] = (
            sla_refund_group["refund_tickets"] / sla_refund_group["tickets"] * 100
        )
        sla_refund_group["avg_refund_per_ticket"] = (
            sla_refund_group["total_refund_inr"] / sla_refund_group["tickets"]
        )
        display_sla_refund = sla_refund_group.copy()
        display_sla_refund["total_refund_inr"] = display_sla_refund[
            "total_refund_inr"
        ].map(lambda x: f"₹{x:,.2f}")
        display_sla_refund["avg_refund_per_ticket"] = display_sla_refund[
            "avg_refund_per_ticket"
        ].map(lambda x: f"₹{x:,.2f}")
        display_sla_refund["refund_rate_pct"] = display_sla_refund[
            "refund_rate_pct"
        ].map(lambda x: f"{x:.2f}%")
        display_sla_refund["sla_breach"] = display_sla_refund[
            "sla_breach"
        ].map({True: "Breach", False: "No Breach"})
        st.dataframe(
            display_sla_refund,
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "SLA breach and refund relationship is descriptive only; "
            "it does not establish causation."
        )

        # STEP 5G — AI BUSINESS SUMMARY
        st.header("5G — AI Business Summary")
        st.caption(
            "Automatically generated business insights from refund and SLA data."
        )

        summary_refund_values = pd.to_numeric(
            cleaned_tickets["refund_amount_inr"], errors="coerce"
        ).fillna(0).clip(lower=0)
        summary_total_refund = float(summary_refund_values.sum())
        summary_refund_tickets = int((summary_refund_values > 0).sum())
        summary_average_refund = (
            summary_total_refund / summary_refund_tickets
            if summary_refund_tickets > 0 else 0
        )

        summary_col1, summary_col2, summary_col3 = st.columns(3)
        with summary_col1:
            st.metric("Total Refund Value", f"₹{summary_total_refund:,.2f}")
        with summary_col2:
            st.metric("Refund Tickets", f"{summary_refund_tickets:,}")
        with summary_col3:
            st.metric("Average Refund", f"₹{summary_average_refund:,.2f}")

        st.subheader("Key Business Findings")
        if not reason_analysis.empty:
            top_reason = reason_analysis.iloc[0]
            st.write(
                f"**1. Largest refund category:** "
                f"{top_reason['refund_reason_code']} accounts for "
                f"₹{float(top_reason['refund_value']):,.2f} "
                f"({float(top_reason['refund_value_pct']):.2f}% "
                f"of total refund value)."
            )
        else:
            st.write("**1. Refund category:** No refund records were found.")

        if not gw_analysis.empty:
            gw_total_value = float(gw_analysis["refund_value"].sum())
            gw_total_tickets = int(gw_analysis["refund_tickets"].sum())
            gw_share_pct = (
                gw_total_value / summary_total_refund * 100
                if summary_total_refund > 0 else 0
            )
            st.write(
                f"**2. GW-OTHER review priority:** {gw_total_tickets:,} "
                f"refund tickets represent ₹{gw_total_value:,.2f}, or "
                f"{gw_share_pct:.2f}% of total refund value. Review "
                "reason-code accuracy and approval evidence."
            )
        else:
            st.write("**2. GW-OTHER:** No GW-OTHER refund records were found.")

        st.write(
            f"**3. SLA performance:** {total_breaches:,} out of "
            f"{total_sla_tickets:,} applicable tickets breached their SLA "
            f"({overall_breach_rate:.2f}%)."
        )

        if not channel_sla.empty:
            worst_channel = channel_sla.sort_values(
                "breach_rate_pct", ascending=False
            ).iloc[0]
            st.write(
                f"**4. Channel requiring attention:** "
                f"{str(worst_channel['channel']).title()} has the highest "
                f"observed SLA breach rate at "
                f"{float(worst_channel['breach_rate_pct']):.2f}%."
            )

        st.write(
            f"**5. Repeat-refund customers:** "
            f"{customer_summary['repeat_customers']:,} customers have "
            f"refunds on two or more tickets. Their refunds account for "
            f"{customer_summary['repeat_refund_pct']:.2f}% of total refund value."
        )
        st.info(
            "This is a rule-based business summary, not an external "
            "generative-AI model. It describes patterns and does not "
            "establish causation."
        )
                # 5I — EXECUTIVE DASHBOARD + GLOBAL FILTERS
        st.header("5I — Executive Dashboard & Global Filters")
        st.caption(
            "These filters apply to the Executive Dashboard and Case Explorer."
        )

        global_df = cleaned_tickets.copy()
        if "created_at" in global_df.columns:
            global_df["created_at"] = pd.to_datetime(
                global_df["created_at"], errors="coerce"
            )

        filter_cols = st.columns(4)
        global_filter_values = {}

        for idx, col_name in enumerate(
            ["channel", "priority", "assigned_team"]
        ):
            if col_name in global_df.columns:
                vals = sorted(
                    global_df[col_name].dropna().astype(str).unique().tolist()
                )
                with filter_cols[idx]:
                    global_filter_values[col_name] = st.multiselect(
                        f"Global {col_name.replace('_', ' ').title()}",
                        options=vals,
                        default=[],
                        key=f"global_filter_{col_name}",
                    )

        date_start = date_end = None
        if (
            "created_at" in global_df.columns
            and global_df["created_at"].notna().any()
        ):
            min_date = global_df["created_at"].min().date()
            max_date = global_df["created_at"].max().date()
            with filter_cols[3]:
                date_range = st.date_input(
                    "Global Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="global_date_range",
                )
            if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
                date_start, date_end = date_range

        global_filtered_cases = global_df.copy()
        for col_name, selected_values in global_filter_values.items():
            if selected_values:
                global_filtered_cases = global_filtered_cases[
                    global_filtered_cases[col_name].astype(str).isin(
                        selected_values
                    )
                ]

        if (
            date_start is not None
            and date_end is not None
            and "created_at" in global_filtered_cases.columns
        ):
            global_filtered_cases = global_filtered_cases[
                global_filtered_cases["created_at"].dt.date.between(
                    date_start, date_end
                )
            ]

        global_refunds = pd.to_numeric(
            global_filtered_cases.get(
                "refund_amount_inr",
                pd.Series(0, index=global_filtered_cases.index),
            ),
            errors="coerce",
        ).fillna(0).clip(lower=0)

        global_refund_tickets = int((global_refunds > 0).sum())
        global_refund_total = float(global_refunds.sum())
        global_avg_refund = (
            global_refund_total / global_refund_tickets
            if global_refund_tickets else 0
        )

        exec_cols = st.columns(4)
        exec_cols[0].metric(
            "Filtered Tickets", f"{len(global_filtered_cases):,}"
        )
        exec_cols[1].metric("Refund Tickets", f"{global_refund_tickets:,}")
        exec_cols[2].metric("Refund Value", f"₹{global_refund_total:,.2f}")
        exec_cols[3].metric("Average Refund", f"₹{global_avg_refund:,.2f}")

        if "refund_reason_code" in global_filtered_cases.columns:
            exec_reason_df = (
                global_filtered_cases.assign(_refund_value=global_refunds)
                .query("_refund_value > 0")
                .groupby("refund_reason_code", dropna=False)["_refund_value"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )
            if not exec_reason_df.empty:
                st.subheader("Executive View — Top Refund Reasons")
                st.bar_chart(exec_reason_df)

        if "created_at" in global_filtered_cases.columns:
            exec_monthly = global_filtered_cases.assign(
                _refund_value=global_refunds
            )
            exec_monthly = exec_monthly[
                exec_monthly["created_at"].notna()
            ].copy()
            if not exec_monthly.empty:
                exec_monthly["month"] = (
                    exec_monthly["created_at"].dt.to_period("M").astype(str)
                )
                exec_monthly = exec_monthly.groupby("month")[
                    "_refund_value"
                ].sum()
                if not exec_monthly.empty:
                    st.subheader("Executive View — Monthly Refund Trend")
                    st.line_chart(exec_monthly)

        # 5J — REFUND ANOMALY DETECTION
        st.header("5J — Refund Anomaly Detection")
        anomaly_df = global_filtered_cases.copy()
        anomaly_df["refund_amount_inr"] = pd.to_numeric(
            anomaly_df.get("refund_amount_inr", 0), errors="coerce"
        ).fillna(0)

        positive_refunds = anomaly_df.loc[
            anomaly_df["refund_amount_inr"] > 0, "refund_amount_inr"
        ]

        if not positive_refunds.empty:
            q1 = positive_refunds.quantile(0.25)
            q3 = positive_refunds.quantile(0.75)
            iqr = q3 - q1
            upper_limit = q3 + (1.5 * iqr)

            anomaly_df["anomaly_flag"] = (
                anomaly_df["refund_amount_inr"] > upper_limit
            )
            anomaly_cases = anomaly_df[anomaly_df["anomaly_flag"]].copy()

            ac1, ac2, ac3 = st.columns(3)
            ac1.metric("High-Value Refund Threshold", f"₹{upper_limit:,.2f}")
            ac2.metric(
                "Potential High-Value Anomalies", f"{len(anomaly_cases):,}"
            )
            ac3.metric(
                "Potential Anomaly Value",
                f"₹{anomaly_cases['refund_amount_inr'].sum():,.2f}",
            )

            st.caption(
                "The IQR statistical rule flags cases for review. "
                "An anomaly is not proof of fraud or a policy violation."
            )

            if not anomaly_cases.empty:
                anomaly_cols = [
                    c for c in [
                        "ticket_id",
                        "customer_id",
                        "order_id",
                        "refund_reason_code",
                        "refund_amount_inr",
                        "channel",
                        "created_at",
                    ]
                    if c in anomaly_cases.columns
                ]
                st.dataframe(
                    anomaly_cases[anomaly_cols].sort_values(
                        "refund_amount_inr", ascending=False
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            st.info(
                "No positive refund records are available for anomaly "
                "detection under the current filters."
            )

        # 5K — DATA QUALITY MONITOR
        st.header("5K — Data Quality Monitor")
        dq1, dq2, dq3 = st.columns(3)

        dq1.metric("Rows in Cleaned Dataset", f"{len(cleaned_tickets):,}")
        dq2.metric(
            "Duplicate Ticket IDs",
            f"{cleaned_tickets['ticket_id'].duplicated().sum():,}"
            if "ticket_id" in cleaned_tickets.columns else "N/A",
        )
        dq3.metric(
            "Columns with Missing Values",
            f"{int(cleaned_tickets.isna().any().sum()):,}",
        )

        missing_summary = (
            cleaned_tickets.isna()
            .sum()
            .rename_axis("column")
            .reset_index(name="missing_values")
        )
        missing_summary["missing_pct"] = (
            missing_summary["missing_values"]
            / max(len(cleaned_tickets), 1)
            * 100
        ).round(2)
        missing_summary = missing_summary[
            missing_summary["missing_values"] > 0
        ].sort_values("missing_values", ascending=False)

        if not missing_summary.empty:
            st.subheader("Missing Values by Column")
            st.dataframe(
                missing_summary,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success("No missing values found in the cleaned dataset.")

        with st.expander("View validation check results"):
            st.json(validation)

        # 5L — DOWNLOADABLE BUSINESS REPORT
        st.header("5L — Downloadable Business Report")
        report_text = (
            "VIREO AUDIO CUSTOMER SUPPORT & REFUND INTELLIGENCE\n"
            "===============================================\n"
            f"Tickets in selected filters: {len(global_filtered_cases):,}\n"
            f"Refund tickets: {global_refund_tickets:,}\n"
            f"Total refund value: INR {global_refund_total:,.2f}\n"
            f"Average refund: INR {global_avg_refund:,.2f}\n"
            f"Overall SLA breaches (full dataset): {total_breaches:,} / "
            f"{total_sla_tickets:,} ({overall_breach_rate:.2f}%)\n"
            f"GW-OTHER above-cap cases (full dataset): "
            f"{len(goodwill_over_cap):,}\n"
            f"Data quality: {int(cleaned_tickets.isna().any().sum())} "
            "columns contain missing values.\n\n"
            "Notes: Anomaly flags are statistical review candidates only. "
            "SLA/refund patterns are descriptive and do not prove causation.\n"
        )

        st.download_button(
            "Download Executive Report (TXT)",
            data=report_text.encode("utf-8"),
            file_name="vireo_executive_business_report.txt",
            mime="text/plain",
            key="download_executive_report",
        )
        st.download_button(
            "Download Filtered Executive Data (CSV)",
            data=global_filtered_cases.to_csv(index=False).encode("utf-8-sig"),
            file_name="vireo_executive_filtered_data.csv",
            mime="text/csv",
            key="download_executive_data",
        )
                # 5H — CASE EXPLORER
        st.header("5H — Case Explorer")
        st.caption(
            "Search, filter and export individual customer support cases."
        )

        case_df = global_filtered_cases.copy()

        # Search controls
        search_col1, search_col2 = st.columns(2)

        with search_col1:
            ticket_search = st.text_input(
                "Search Ticket ID",
                key="case_ticket_search",
            )

        with search_col2:
            customer_search = st.text_input(
                "Search Customer ID",
                key="case_customer_search",
            )

        # Refund reason filter
        reason_options = (
            sorted(
                case_df["refund_reason_code"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
            if "refund_reason_code" in case_df.columns else []
        )

        selected_reasons = st.multiselect(
            "Refund Reason",
            options=reason_options,
            default=[],
            key="case_reason_filter",
        )

        # Channel filter
        channel_options = (
            sorted(
                case_df["channel"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
            if "channel" in case_df.columns else []
        )

        selected_channels = st.multiselect(
            "Channel",
            options=channel_options,
            default=[],
            key="case_channel_filter",
        )

        # Refund status filter
        refund_filter = st.selectbox(
            "Refund Status",
            ["All", "Refunded", "Not Refunded"],
            key="case_refund_filter",
        )

        # Apply filters
        filtered_cases = case_df.copy()

        if ticket_search.strip() and "ticket_id" in filtered_cases.columns:
            filtered_cases = filtered_cases[
                filtered_cases["ticket_id"]
                .astype(str)
                .str.contains(
                    ticket_search.strip(),
                    case=False,
                    na=False,
                    regex=False,
                )
            ]

        if customer_search.strip() and "customer_id" in filtered_cases.columns:
            filtered_cases = filtered_cases[
                filtered_cases["customer_id"]
                .astype(str)
                .str.contains(
                    customer_search.strip(),
                    case=False,
                    na=False,
                    regex=False,
                )
            ]

        if selected_reasons and "refund_reason_code" in filtered_cases.columns:
            filtered_cases = filtered_cases[
                filtered_cases["refund_reason_code"]
                .astype(str)
                .isin(selected_reasons)
            ]

        if selected_channels and "channel" in filtered_cases.columns:
            filtered_cases = filtered_cases[
                filtered_cases["channel"].astype(str).isin(selected_channels)
            ]

        case_refund_amount = pd.to_numeric(
            filtered_cases["refund_amount_inr"],
            errors="coerce",
        ).fillna(0)

        if refund_filter == "Refunded":
            filtered_cases = filtered_cases[case_refund_amount > 0]
        elif refund_filter == "Not Refunded":
            filtered_cases = filtered_cases[case_refund_amount <= 0]

        # Results summary
        st.subheader("Filtered Cases")
        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.metric("Matching Tickets", f"{len(filtered_cases):,}")

        with result_col2:
            filtered_refund_total = pd.to_numeric(
                filtered_cases["refund_amount_inr"],
                errors="coerce",
            ).fillna(0).clip(lower=0).sum()

            st.metric(
                "Matching Refund Value",
                f"₹{filtered_refund_total:,.2f}",
            )

        # Display relevant columns
        preferred_columns = [
            "ticket_id",
            "customer_id",
            "order_id",
            "product_sku",
            "channel",
            "priority",
            "assigned_team",
            "agent_id",
            "refund_reason_code",
            "refund_amount_inr",
            "created_at",
            "first_response_at",
            "resolved_at",
        ]

        visible_columns = [
            column
            for column in preferred_columns
            if column in filtered_cases.columns
        ]

        st.dataframe(
            filtered_cases[visible_columns],
            use_container_width=True,
            hide_index=True,
        )

        # Export filtered cases
        csv_data = filtered_cases.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="Download Filtered Cases as CSV",
            data=csv_data,
            file_name="vireo_filtered_cases.csv",
            mime="text/csv",
            key="case_export_csv",
        )

        # EXTRA FEATURE 3 — CASE DETAILS PANEL
        st.subheader("Case Details Panel")

        if (
            not filtered_cases.empty
            and "ticket_id" in filtered_cases.columns
        ):
            detail_ids = (
                filtered_cases["ticket_id"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_ticket_detail = st.selectbox(
                "Select a ticket to inspect",
                detail_ids,
                key="case_detail_ticket",
            )

            selected_case_rows = filtered_cases[
                filtered_cases["ticket_id"].astype(str)
                == selected_ticket_detail
            ]

            if not selected_case_rows.empty:
                selected_case = selected_case_rows.iloc[0]
                detail_data = {
                    str(key): (None if pd.isna(value) else str(value))
                    for key, value in selected_case.items()
                }
                st.json(detail_data)
        else:
            st.info(
                "No cases match the current filters, so there is no case to inspect."
            )

        # COMPLETION
        st.success(
            "Steps 5B–5L completed successfully: ingestion, cleaning, "
            "analytics, policy review, SLA intelligence, business summary, "
            "Case Explorer, Executive Dashboard, global filters, anomaly "
            "detection, data quality monitor and business report."
        )

    except Exception as error:
        st.error(f"Data processing failed: {error}")