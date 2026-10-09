import pandas as pd


def get_source_column(df):
    """
    Identify the source-system column.
    """

    if "source_system" in df.columns:
        return "source_system"

    if "source" in df.columns:
        return "source"

    raise KeyError(
        "Source column not found. Expected 'source_system'."
    )


def reconcile_tickets(tickets_df):
    """
    Remove duplicate ticket IDs.

    Current helpdesk records are preferred over legacy_fd records.
    """

    df = tickets_df.copy()

    source_column = get_source_column(df)

    df["_source_priority"] = (
        df[source_column]
        .astype(str)
        .str.lower()
        .eq("helpdesk")
        .astype(int)
    )

    df = df.sort_values(
        by=["ticket_id", "_source_priority"],
        ascending=[True, False]
    )

    df = df.drop_duplicates(
        subset=["ticket_id"],
        keep="first"
    )

    df = df.drop(
        columns=["_source_priority"]
    )

    return df.reset_index(drop=True)


def get_reconciliation_summary(original_df, cleaned_df):
    """
    Return duplicate-reconciliation statistics.
    """

    original_rows = len(original_df)
    cleaned_rows = len(cleaned_df)

    return {
        "original_rows": original_rows,
        "unique_ticket_ids": cleaned_rows,
        "duplicate_rows_removed": (
            original_rows - cleaned_rows
        ),
    }


def normalize_refund_amounts(tickets_df):
    """
    Normalize refund amounts.

    Helpdesk values remain unchanged.
    Legacy_fd values are divided by 100.
    """

    df = tickets_df.copy()

    source_column = get_source_column(df)

    refund_column = "refund_amount_inr"

    if refund_column not in df.columns:
        raise KeyError(
            "Refund amount column not found. "
            "Expected 'refund_amount_inr'."
        )

    # Preserve original raw value
    df["refund_amount_raw"] = df[refund_column]

    # Convert refund values to numeric
    df["refund_amount_inr"] = pd.to_numeric(
        df["refund_amount_inr"],
        errors="coerce"
    )

    # Identify legacy records
    legacy_mask = (
        df[source_column]
        .astype(str)
        .str.lower()
        .eq("legacy_fd")
    )

    # Normalize legacy values
    df.loc[legacy_mask, "refund_amount_inr"] = (
        df.loc[legacy_mask, "refund_amount_inr"] / 100
    )

    return df


def validate_cleaned_data(tickets_df):
    """
    Validate the cleaned Vireo ticket dataset.
    """

    df = tickets_df.copy()

    # Duplicate ticket IDs
    duplicate_ticket_ids = int(
        df["ticket_id"].duplicated().sum()
    )

    # Refund and reason consistency
    refund_values = pd.to_numeric(
        df["refund_amount_inr"],
        errors="coerce"
    )

    has_refund = (
        refund_values.notna()
        & (refund_values > 0)
    )

    has_reason = (
        df["refund_reason_code"].notna()
        & df["refund_reason_code"]
        .astype(str)
        .str.strip()
        .ne("")
    )

    refund_without_reason = int(
        (has_refund & ~has_reason).sum()
    )

    reason_without_refund = int(
        (~has_refund & has_reason).sum()
    )

    # Invalid refund values
    negative_refunds = int(
        (refund_values < 0).sum()
    )

    zero_refunds = int(
        (refund_values == 0).sum()
    )

    return {
        "duplicate_ticket_ids": duplicate_ticket_ids,
        "refund_without_reason": refund_without_reason,
        "reason_without_refund": reason_without_refund,
        "negative_refunds": negative_refunds,
        "zero_refunds": zero_refunds,
    }