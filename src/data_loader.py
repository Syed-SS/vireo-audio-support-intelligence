from pathlib import Path
import pandas as pd


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


REQUIRED_COLUMNS = {
    "tickets": {
        "ticket_id",
        "order_id",
        "customer_id",
        "product_sku",
        "agent_id",
        "channel",
        "created_at",
        "first_response_at",
    },

    "orders": {
        "order_id",
        "customer_id",
        "sku",
    },

    "products": {
        "sku",
    },

    "customers": {
        "customer_id",
    },

    "agents": {
        "agent_id",
    },
}


FILE_NAMES = {
    "tickets": "tickets.csv",
    "orders": "orders.csv",
    "products": "products.csv",
    "customers": "customers.csv",
    "agents": "agents.csv",
}


def load_dataset(name):
    """Load one Vireo CSV dataset."""

    path = DATA_DIR / FILE_NAMES[name]

    if not path.exists():
        raise FileNotFoundError(
            f"{FILE_NAMES[name]} was not found in the data folder."
        )

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(
            f"{FILE_NAMES[name]} is empty."
        )

    missing_columns = REQUIRED_COLUMNS[name] - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{FILE_NAMES[name]} is missing columns: "
            + ", ".join(sorted(missing_columns))
        )

    return df


def load_all_datasets():
    """Load and validate all five Vireo datasets."""

    datasets = {}

    for name in FILE_NAMES:
        datasets[name] = load_dataset(name)

    return datasets