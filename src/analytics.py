import pandas as pd


# =========================================================
# 5D.1 — Basic Refund KPIs
# =========================================================

def calculate_refund_kpis(tickets_df):
    """
    Calculate core refund KPIs.
    """

    df = tickets_df.copy()

    refund_values = pd.to_numeric(
        df["refund_amount_inr"],
        errors="coerce"
    ).fillna(0)

    total_tickets = len(df)

    refund_tickets = int(
        (refund_values > 0).sum()
    )

    total_refund_value = float(
        refund_values[refund_values > 0].sum()
    )

    average_refund = (
        total_refund_value / refund_tickets
        if refund_tickets > 0
        else 0
    )

    refund_rate = (
        (refund_tickets / total_tickets) * 100
        if total_tickets > 0
        else 0
    )

    return {
        "total_tickets": total_tickets,
        "refund_tickets": refund_tickets,
        "total_refund_value": total_refund_value,
        "average_refund": average_refund,
        "refund_rate": refund_rate,
    }


# =========================================================
# 5D.2 — Refund Reason Analysis
# =========================================================

def analyze_refund_reasons(tickets_df):
    """
    Analyze refund tickets by refund reason.
    """

    df = tickets_df.copy()

    df["refund_amount_inr"] = pd.to_numeric(
        df["refund_amount_inr"],
        errors="coerce"
    ).fillna(0)

    refund_df = df[
        df["refund_amount_inr"] > 0
    ].copy()

    total_refund_value = refund_df[
        "refund_amount_inr"
    ].sum()

    reason_analysis = (
        refund_df
        .groupby(
            "refund_reason_code",
            dropna=False
        )
        .agg(
            refund_tickets=("ticket_id", "count"),
            refund_value=("refund_amount_inr", "sum")
        )
        .reset_index()
    )

    if total_refund_value > 0:
        reason_analysis["refund_value_pct"] = (
            reason_analysis["refund_value"]
            / total_refund_value
            * 100
        )
    else:
        reason_analysis["refund_value_pct"] = 0

    return (
        reason_analysis
        .sort_values(
            by="refund_value",
            ascending=False
        )
        .reset_index(drop=True)
    )


# =========================================================
# 5D.3 — Monthly Refund Trend
# =========================================================

def analyze_monthly_refunds(tickets_df):
    """
    Analyze refund value and ticket count by month.
    """

    df = tickets_df.copy()

    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="coerce"
    )

    df["refund_amount_inr"] = pd.to_numeric(
        df["refund_amount_inr"],
        errors="coerce"
    ).fillna(0)

    refund_df = df[
        df["refund_amount_inr"] > 0
    ].copy()

    refund_df["month"] = (
        refund_df["created_at"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly = (
        refund_df
        .groupby("month")
        .agg(
            refund_tickets=("ticket_id", "count"),
            refund_value=("refund_amount_inr", "sum")
        )
        .reset_index()
    )

    return (
        monthly
        .sort_values("month")
        .reset_index(drop=True)
    )


# =========================================================
# 5D.4 — Product Refund Analysis
# =========================================================

def analyze_product_refunds(tickets_df, products_df):
    """
    Analyze refunds by product.

    Handles both:
    - products.csv using "sku"
    - products.csv using "product_sku"
    """

    df = tickets_df.copy()
    products = products_df.copy()

    df["refund_amount_inr"] = pd.to_numeric(
        df["refund_amount_inr"],
        errors="coerce"
    ).fillna(0)

    refund_df = df[
        df["refund_amount_inr"] > 0
    ].copy()

    product_analysis = (
        refund_df
        .groupby("product_sku")
        .agg(
            refund_tickets=("ticket_id", "count"),
            refund_value=("refund_amount_inr", "sum")
        )
        .reset_index()
    )

    total_refund = product_analysis[
        "refund_value"
    ].sum()

    if total_refund > 0:
        product_analysis["refund_value_pct"] = (
            product_analysis["refund_value"]
            / total_refund
            * 100
        )
    else:
        product_analysis["refund_value_pct"] = 0

    # -----------------------------------------------------
    # Product lookup
    # -----------------------------------------------------

    if "sku" in products.columns:

        name_columns = [
            column
            for column in products.columns
            if "name" in column.lower()
        ]

        if name_columns:

            product_name_column = name_columns[0]

            products_lookup = products[
                [
                    "sku",
                    product_name_column
                ]
            ].drop_duplicates(
                subset=["sku"]
            )

            products_lookup = products_lookup.rename(
                columns={
                    "sku": "product_sku",
                    product_name_column: "product_name"
                }
            )

        else:

            products_lookup = products[
                ["sku"]
            ].drop_duplicates(
                subset=["sku"]
            )

            products_lookup = products_lookup.rename(
                columns={
                    "sku": "product_sku"
                }
            )

            products_lookup["product_name"] = (
                products_lookup["product_sku"]
            )

    elif "product_sku" in products.columns:

        name_columns = [
            column
            for column in products.columns
            if "name" in column.lower()
        ]

        if name_columns:

            product_name_column = name_columns[0]

            products_lookup = products[
                [
                    "product_sku",
                    product_name_column
                ]
            ].drop_duplicates(
                subset=["product_sku"]
            )

            products_lookup = products_lookup.rename(
                columns={
                    product_name_column: "product_name"
                }
            )

        else:

            products_lookup = products[
                ["product_sku"]
            ].drop_duplicates(
                subset=["product_sku"]
            )

            products_lookup["product_name"] = (
                products_lookup["product_sku"]
            )

    else:

        products_lookup = pd.DataFrame(
            columns=[
                "product_sku",
                "product_name"
            ]
        )

    # -----------------------------------------------------
    # Merge product information
    # -----------------------------------------------------

    product_analysis = product_analysis.merge(
        products_lookup,
        on="product_sku",
        how="left"
    )

    product_analysis["product_name"] = (
        product_analysis["product_name"]
        .fillna(product_analysis["product_sku"])
    )

    return (
        product_analysis
        .sort_values(
            "refund_value",
            ascending=False
        )
        .reset_index(drop=True)
    )


# =========================================================
# 5D.5 — Team Refund Analysis
# =========================================================

def analyze_team_refunds(tickets_df):
    """
    Analyze refunds by assigned team.
    """

    df = tickets_df.copy()

    df["refund_amount_inr"] = pd.to_numeric(
        df["refund_amount_inr"],
        errors="coerce"
    ).fillna(0)

    refund_df = df[
        df["refund_amount_inr"] > 0
    ].copy()

    team_analysis = (
        refund_df
        .groupby(
            "assigned_team",
            dropna=False
        )
        .agg(
            refund_tickets=("ticket_id", "count"),
            refund_value=("refund_amount_inr", "sum")
        )
        .reset_index()
    )

    total_refund = team_analysis[
        "refund_value"
    ].sum()

    if total_refund > 0:
        team_analysis["refund_value_pct"] = (
            team_analysis["refund_value"]
            / total_refund
            * 100
        )
    else:
        team_analysis["refund_value_pct"] = 0

    return (
        team_analysis
        .sort_values(
            "refund_value",
            ascending=False
        )
        .reset_index(drop=True)
    )


# =========================================================
# 5D.6 — Agent Refund Analysis
# =========================================================

def analyze_agent_refunds(tickets_df, agents_df):
    """
    Analyze refunds by agent.
    """

    df = tickets_df.copy()
    agents = agents_df.copy()

    df["refund_amount_inr"] = pd.to_numeric(
        df["refund_amount_inr"],
        errors="coerce"
    ).fillna(0)

    refund_df = df[
        df["refund_amount_inr"] > 0
    ].copy()

    agent_analysis = (
        refund_df
        .groupby(
            "agent_id",
            dropna=False
        )
        .agg(
            refund_tickets=("ticket_id", "count"),
            refund_value=("refund_amount_inr", "sum")
        )
        .reset_index()
    )

    total_refund = agent_analysis[
        "refund_value"
    ].sum()

    if total_refund > 0:
        agent_analysis["refund_value_pct"] = (
            agent_analysis["refund_value"]
            / total_refund
            * 100
        )
    else:
        agent_analysis["refund_value_pct"] = 0

    # -----------------------------------------------------
    # Detect agent name and team columns
    # -----------------------------------------------------

    name_columns = [
        column
        for column in agents.columns
        if "name" in column.lower()
    ]

    team_columns = [
        column
        for column in agents.columns
        if "team" in column.lower()
    ]

    lookup_columns = [
        "agent_id"
    ]

    if name_columns:
        lookup_columns.append(
            name_columns[0]
        )

    if team_columns:
        lookup_columns.append(
            team_columns[0]
        )

    agents_lookup = (
        agents[
            lookup_columns
        ]
        .drop_duplicates(
            subset=["agent_id"]
        )
    )

    rename_map = {}

    if name_columns:
        rename_map[
            name_columns[0]
        ] = "name"

    if team_columns:
        rename_map[
            team_columns[0]
        ] = "team"

    agents_lookup = agents_lookup.rename(
        columns=rename_map
    )

    agent_analysis = agent_analysis.merge(
        agents_lookup,
        on="agent_id",
        how="left"
    )

    if "name" not in agent_analysis.columns:
        agent_analysis["name"] = (
            agent_analysis["agent_id"]
        )

    if "team" not in agent_analysis.columns:
        agent_analysis["team"] = "Unknown"

    return (
        agent_analysis
        .sort_values(
            "refund_value",
            ascending=False
        )
        .reset_index(drop=True)
    )


# =========================================================
# 5D.7 — Customer Refund Analysis
# =========================================================

def analyze_customer_refunds(tickets_df):
    """
    Analyze customer refund frequency and concentration.
    """

    df = tickets_df.copy()

    df["refund_amount_inr"] = pd.to_numeric(
        df["refund_amount_inr"],
        errors="coerce"
    ).fillna(0)

    refund_df = df[
        df["refund_amount_inr"] > 0
    ].copy()

    customer_analysis = (
        refund_df
        .groupby(
            "customer_id",
            dropna=False
        )
        .agg(
            refund_tickets=("ticket_id", "count"),
            refund_value=("refund_amount_inr", "sum")
        )
        .reset_index()
    )

    customer_analysis[
        "repeat_customer"
    ] = (
        customer_analysis["refund_tickets"] >= 2
    )

    return (
        customer_analysis
        .sort_values(
            [
                "refund_tickets",
                "refund_value"
            ],
            ascending=[
                False,
                False
            ]
        )
        .reset_index(drop=True)
    )


def get_customer_refund_summary(tickets_df):
    """
    Calculate high-level customer refund metrics.
    """

    customer_analysis = (
        analyze_customer_refunds(
            tickets_df
        )
    )

    refund_customers = len(
        customer_analysis
    )

    repeat_customers = int(
        (
            customer_analysis[
                "refund_tickets"
            ] >= 2
        ).sum()
    )

    three_plus_customers = int(
        (
            customer_analysis[
                "refund_tickets"
            ] >= 3
        ).sum()
    )

    repeat_refund_value = float(
        customer_analysis.loc[
            customer_analysis[
                "refund_tickets"
            ] >= 2,
            "refund_value"
        ].sum()
    )

    three_plus_refund_value = float(
        customer_analysis.loc[
            customer_analysis[
                "refund_tickets"
            ] >= 3,
            "refund_value"
        ].sum()
    )

    total_refund_value = float(
        customer_analysis[
            "refund_value"
        ].sum()
    )

    repeat_refund_pct = (
        repeat_refund_value
        / total_refund_value
        * 100
        if total_refund_value > 0
        else 0
    )

    return {
        "refund_customers": refund_customers,
        "repeat_customers": repeat_customers,
        "three_plus_customers": three_plus_customers,
        "repeat_refund_value": repeat_refund_value,
        "three_plus_refund_value": three_plus_refund_value,
        "repeat_refund_pct": repeat_refund_pct,
    }


# =========================================================
# 5D.8 — GW-OTHER Intelligence
# =========================================================

def classify_gw_other_text(text):
    """
    Rule-based first-pass classification of GW-OTHER cases.
    """

    if pd.isna(text):
        return "Manual Review"

    text = str(text).lower()

    payment_words = [
        "payment",
        "paid",
        "charge",
        "charged",
        "billing",
        "card",
        "transaction",
        "upi",
        "amount deducted",
        "money deducted",
        "double payment",
    ]

    refund_words = [
        "refund",
        "money back",
        "return my money",
        "give my money",
        "reimburse",
    ]

    delivery_words = [
        "delivery",
        "delivered",
        "shipping",
        "shipment",
        "courier",
        "late",
        "delay",
        "delayed",
        "package",
        "parcel",
        "not received",
    ]

    pickup_words = [
        "pickup",
        "pick up",
        "collection",
        "collect",
        "return pickup",
        "return collection",
    ]

    cancellation_words = [
        "cancel",
        "cancellation",
        "changed my mind",
        "change of mind",
        "don't want",
        "do not want",
    ]

    defect_words = [
        "defect",
        "defective",
        "broken",
        "damage",
        "damaged",
        "not working",
        "faulty",
        "dead",
        "damaged product",
    ]

    goodwill_words = [
        "sorry",
        "dissatisfied",
        "unhappy",
        "goodwill",
    ]

    if any(
        word in text
        for word in payment_words
    ):
        return "Payment / Billing"

    if any(
        word in text
        for word in refund_words
    ):
        return "Refund / Money Request"

    if any(
        word in text
        for word in delivery_words
    ):
        return "Delivery / Shipping"

    if any(
        word in text
        for word in pickup_words
    ):
        return "Pickup / Return"

    if any(
        word in text
        for word in cancellation_words
    ):
        return "Cancellation / Change of Mind"

    if any(
        word in text
        for word in defect_words
    ):
        return "Product Defect / Damage"

    if any(
        word in text
        for word in goodwill_words
    ):
        return "Goodwill / Dissatisfaction"

    return "Manual Review"


def analyze_gw_other(tickets_df):
    """
    Deep-dive analysis of GW-OTHER refunds.
    """

    df = tickets_df.copy()

    df["refund_amount_inr"] = pd.to_numeric(
        df["refund_amount_inr"],
        errors="coerce"
    ).fillna(0)

    gw_df = df[
        (df["refund_amount_inr"] > 0)
        & (
            df["refund_reason_code"]
            .astype(str)
            .str.upper()
            .eq("GW-OTHER")
        )
    ].copy()

    # Safely handle missing text columns
    if "customer_message" not in gw_df.columns:
        gw_df["customer_message"] = ""

    if "agent_notes" not in gw_df.columns:
        gw_df["agent_notes"] = ""

    gw_df["combined_text"] = (
        gw_df["customer_message"]
        .fillna("")
        .astype(str)
        + " "
        + gw_df["agent_notes"]
        .fillna("")
        .astype(str)
    )

    gw_df["gw_category"] = (
        gw_df["combined_text"]
        .apply(
            classify_gw_other_text
        )
    )

    analysis = (
        gw_df
        .groupby("gw_category")
        .agg(
            refund_tickets=("ticket_id", "count"),
            refund_value=("refund_amount_inr", "sum")
        )
        .reset_index()
    )

    total_value = analysis[
        "refund_value"
    ].sum()

    total_tickets = analysis[
        "refund_tickets"
    ].sum()

    if total_tickets > 0:
        analysis["ticket_pct"] = (
            analysis["refund_tickets"]
            / total_tickets
            * 100
        )
    else:
        analysis["ticket_pct"] = 0

    if total_value > 0:
        analysis["refund_value_pct"] = (
            analysis["refund_value"]
            / total_value
            * 100
        )
    else:
        analysis["refund_value_pct"] = 0

    return (
        analysis
        .sort_values(
            "refund_value",
            ascending=False
        )
        .reset_index(drop=True)
    )