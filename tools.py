import pandas as pd
from io import StringIO


def make_tools(csv_data: str):
    """Build tool callables bound to the uploaded CSV.

    Using closures keeps the CSV out of the LLM's tool-call arguments, so the
    model only has to pass small strings (category / keyword) instead of the
    entire file — this is what usually breaks tool-calling with big inputs.
    """

    def get_total_spending(category: str = "") -> str:
        """Return total spending in RSD. If `category` is non-empty, only sum
        transactions in that category (case-insensitive). Otherwise sum all."""
        df = pd.read_csv(StringIO(csv_data))
        if category:
            filtered = df[df["category"].str.lower() == category.lower()]
            total = filtered["amount"].sum()
            return f"Total spending for {category}: {total} RSD"
        total = df["amount"].sum()
        return f"Total spending: {total} RSD"

    def find_transactions_by_keyword(keyword: str) -> str:
        """Find all transactions whose description contains `keyword`
        (case-insensitive) and return the total amount spent and the count."""
        df = pd.read_csv(StringIO(csv_data))
        filtered = df[df["description"].str.lower().str.contains(keyword.lower())]
        if filtered.empty:
            return f"No transactions found for '{keyword}'"
        total = filtered["amount"].sum()
        return (
            f"You spent {total} RSD on '{keyword}' "
            f"across {len(filtered)} transactions"
        )

    def get_spending_by_category() -> str:
        """Return a breakdown of total spending per category in RSD."""
        df = pd.read_csv(StringIO(csv_data))
        breakdown = df.groupby("category")["amount"].sum().to_dict()
        lines = [f"- {k}: {v} RSD" for k, v in breakdown.items()]
        return "Spending by category:\n" + "\n".join(lines)

    return [get_total_spending, find_transactions_by_keyword, get_spending_by_category]
