import asyncio

import streamlit as st
import pandas as pd

from agent import build_agent

st.title("📊 Expense Triage Agent")

uploaded_file = st.file_uploader("Upload your transactions CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Data")
    st.dataframe(df)

    st.write(f"Number of transactions: {len(df)}")
    st.write("Columns:", list(df.columns))

    st.subheader("📊 Dashboard")

    total_spend = df["amount"].sum()
    num_transactions = len(df)
    top_category = df["category"].value_counts().idxmax()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spend", f"{total_spend} RSD")
    col2.metric("Transactions", num_transactions)
    col3.metric("Top Category", top_category)

    st.subheader("Spending by Category")
    category_spend = df.groupby("category")["amount"].sum()
    st.bar_chart(category_spend)

question = st.text_input("Ask a question about your spending")

if st.button("Analyze"):
    if uploaded_file is None:
        st.error("Please upload a CSV file first.")
    elif question == "":
        st.error("Please enter a question.")
    else:
        csv_data = df.to_csv(index=False)
        agent = build_agent(csv_data)

        async def _ask(q: str):
            result = await agent.run(q)
            if hasattr(result, "response"):
                return str(result.response)
            return str(result)

        try:
            with st.spinner("Thinking..."):
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_closed():
                        raise RuntimeError("loop closed")
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                response = loop.run_until_complete(_ask(question))
            st.subheader("🤖 Agent Answer")
            st.write(response)
        except Exception as e:
            st.error("The agent request failed. Try again or switch models in agent.py.")
            st.caption(f"Details: {type(e).__name__}: {e}")
