from io import StringIO
import re

import pandas as pd


STOPWORDS = {
    "about",
    "amount",
    "answer",
    "category",
    "check",
    "did",
    "expense",
    "expenses",
    "find",
    "for",
    "have",
    "how",
    "much",
    "my",
    "on",
    "paid",
    "rsd",
    "spend",
    "spending",
    "spent",
    "the",
    "total",
    "transaction",
    "transactions",
    "was",
    "what",
}


def _format_amount(amount) -> str:
    if float(amount).is_integer():
        return str(int(amount))
    return f"{amount:.2f}"


def _read_transactions(csv_data: str) -> pd.DataFrame:
    df = pd.read_csv(StringIO(csv_data))
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df


def answer_question(csv_data: str, question: str) -> str | None:
    """Answer common expense questions directly from the CSV.

    The hosted model is not returning structured tool calls, so this keeps the
    Streamlit app useful by calculating the numbers locally.
    """
    df = _read_transactions(csv_data)
    q = question.lower()

    if df.empty:
        return "No transactions found in the uploaded CSV."

    if "category" in df.columns and (
        "by category" in q or "breakdown" in q or "categories" in q
    ):
        totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)
        lines = [f"- {category}: {_format_amount(total)} RSD" for category, total in totals.items()]
        return "Spending by category:\n" + "\n".join(lines)

    if "category" in df.columns and "top" in q and "category" in q:
        totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)
        category = totals.index[0]
        total = totals.iloc[0]
        return f"Your top spending category is {category}: {_format_amount(total)} RSD."

    if "category" in df.columns:
        category_matches = [
            category
            for category in df["category"].dropna().unique()
            if str(category).lower() in q
        ]
        if category_matches:
            category = category_matches[0]
            total = df.loc[
                df["category"].astype(str).str.lower() == str(category).lower(), "amount"
            ].sum()
            return f"You spent {_format_amount(total)} RSD in {category}."

    if "description" in df.columns:
        words = [
            word
            for word in re.findall(r"[a-z0-9]+", q)
            if len(word) >= 3 and word not in STOPWORDS
        ]
        for word in words:
            matches = df["description"].astype(str).str.contains(word, case=False, na=False)
            if matches.any():
                total = df.loc[matches, "amount"].sum()
                count = int(matches.sum())
                return f"You spent {_format_amount(total)} RSD on {word} across {count} transaction(s)."

    if "total" in q or "spend" in q or "spent" in q:
        total = df["amount"].sum()
        return f"Your total spending is {_format_amount(total)} RSD."

    return None


def make_tools(csv_data: str):
    """Build tool callables bound to the uploaded CSV.

    Using closures keeps the CSV out of the LLM's tool-call arguments, so the
    model only has to pass small strings (category / keyword) instead of the
    entire file — this is what usually breaks tool-calling with big inputs.
    """

    def get_total_spending(category: str = "") -> str:
        """Return total spending in RSD. If `category` is non-empty, only sum
        transactions in that category (case-insensitive). Otherwise sum all."""
        df = _read_transactions(csv_data)
        if category:
            filtered = df[df["category"].str.lower() == category.lower()]
            total = filtered["amount"].sum()
            return f"Total spending for {category}: {total} RSD"
        total = df["amount"].sum()
        return f"Total spending: {total} RSD"

    def find_transactions_by_keyword(keyword: str) -> str:
        """Find all transactions whose description contains `keyword`
        (case-insensitive) and return the total amount spent and the count."""
        df = _read_transactions(csv_data)
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
        df = _read_transactions(csv_data)
        breakdown = df.groupby("category")["amount"].sum().to_dict()
        lines = [f"- {k}: {v} RSD" for k, v in breakdown.items()]
        return "Spending by category:\n" + "\n".join(lines)

    return [get_total_spending, find_transactions_by_keyword, get_spending_by_category]
