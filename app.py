import asyncio

import streamlit as st
import pandas as pd

from agent import build_agent
from tools import answer_question

st.set_page_config(
    page_title="Expense Triage Agent",
    page_icon="💸",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(79, 70, 229, 0.18), transparent 32rem),
                linear-gradient(180deg, #020617 0%, #0f172a 100%);
            color: #f9fafb;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        .custom-card,
        .hero-card,
        .step-card,
        .empty-state-card {
            background: rgba(17, 24, 39, 0.78);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 1.4rem;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(10px);
            color: #f9fafb;
        }

        .custom-card *,
        .hero-card *,
        .step-card *,
        .empty-state-card * {
            color: inherit;
        }

        .step-card:hover,
        .custom-card:hover {
            transform: translateY(-3px);
            border-color: rgba(129, 140, 248, 0.45);
            transition: all 0.2s ease;
        }

        .hero {
            text-align: center;
            padding: 3rem 1rem 2rem;
            max-width: 820px;
            margin: 0 auto;
        }
        .hero h1 {
            font-size: 3rem;
            letter-spacing: -0.04em;
            margin-bottom: 1rem;
            line-height: 1.05;
            color: #ffffff;
        }
        .hero p {
            color: #c7d2fe;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 0;
        }
        .hero-divider {
            width: 140px;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(129, 140, 248, 0.8), transparent);
            margin: 0 auto 1.5rem;
        }
        .step-card {
            padding: 1.25rem 1rem;
            min-height: 130px;
        }
        .step-icon {
            font-size: 1.9rem;
            line-height: 1;
            margin-bottom: 0.9rem;
        }
        .step-title {
            color: #f9fafb;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .step-label {
            color: #9ca3af;
            font-size: 0.78rem;
            margin-bottom: 0.35rem;
        }
        .step-description {
            color: #9ca3af;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        .empty-card {
            text-align: center;
            padding: 3.25rem 2.25rem;
        }
        .empty-card h3 {
            color: #f9fafb;
            font-size: 1.6rem;
            margin: 0 0 0.75rem;
        }
        .empty-card p {
            color: #9ca3af;
            line-height: 1.6;
            margin: 0 0 1rem;
        }
        .empty-card .example-columns {
            color: #d1d5db;
        }
        .empty-cta {
            color: #93c5fd;
            font-weight: 600;
            margin-top: 1.25rem;
        }
        .muted {
            color: #6b7280;
        }

        div[data-testid="stMetric"] {
            background: rgba(17, 24, 39, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.25rem;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
            color: #f9fafb;
        }

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] p {
            color: #cbd5e1 !important;
            font-weight: 500;
        }

        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] div {
            color: #ffffff !important;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] div {
            color: #a5b4fc !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #4F46E5, #6366F1);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.65rem 1.3rem;
            font-weight: 600;
            box-shadow: 0 10px 22px rgba(79, 70, 229, 0.25);
        }

        .stButton > button:hover {
            opacity: 0.92;
            border: none;
            transform: translateY(-1px);
        }

        .stTextInput input {
            border-radius: 12px;
            padding: 0.65rem;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        hr {
            border-color: rgba(255, 255, 255, 0.08);
        }
    </style>
    <div class="hero hero-card">
        <h1>💸 Expense Triage Agent</h1>
        <p>Analyze your spending and ask AI questions about your transactions</p>
    </div>
    <div class="hero-divider"></div>
    """,
    unsafe_allow_html=True,
)

st.write("")

step1, step2, step3 = st.columns(3)
with step1:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">📂</div>
            <div class="step-label">Step 1</div>
            <div class="step-title">Upload your data</div>
            <div class="step-description">Upload your CSV file from the sidebar</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with step2:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">📊</div>
            <div class="step-label">Step 2</div>
            <div class="step-title">Explore dashboard</div>
            <div class="step-description">View insights and spending overview</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with step3:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">🤖</div>
            <div class="step-label">Step 3</div>
            <div class="step-title">Ask the AI agent</div>
            <div class="step-description">Ask questions about your transactions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.sidebar:
    st.header("📂 Upload your data")
    st.write("Upload a CSV file with columns: date, description, amount, category")
    uploaded_file = st.file_uploader("Upload your transactions CSV", type=["csv"])
    if uploaded_file is not None:
        st.success("File uploaded successfully")

st.divider()

if uploaded_file is None:
    left, center, right = st.columns([1, 1.4, 1])
    with center:
        st.markdown(
            """
            <div class="empty-card empty-state-card">
                <h3>No data yet</h3>
                <p>Upload your CSV file from the sidebar to get started.</p>
                <p class="example-columns">Example columns: date, description, amount, category</p>
                <div class="empty-cta">👉 Upload your CSV from the sidebar to begin</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

else:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Spending Overview")
    st.write("")

    total_spend = df["amount"].sum()
    num_transactions = len(df)
    top_category = df["category"].value_counts().idxmax()

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric("Total Spend", f"{total_spend} RSD")
    with col2:
        with st.container(border=True):
            st.metric("Transactions", num_transactions)
    with col3:
        with st.container(border=True):
            st.metric("Top Category", top_category)

    st.write("")
    st.write("")
    st.write("")

    st.subheader("Spending by Category")
    category_spend = df.groupby("category")["amount"].sum()
    st.bar_chart(category_spend)

    st.write("")

    with st.expander("📄 View raw data"):
        st.dataframe(df)
        st.write(f"Number of transactions: {len(df)}")

    st.divider()

    st.subheader("🤖 Ask the AI Agent")
    st.write("Ask natural language questions about your transactions")

    example_col1, example_col2, example_col3, example_col4 = st.columns(4)
    if example_col1.button("Total spending"):
        st.session_state["question"] = "What is my total spending?"
    if example_col2.button("Top category"):
        st.session_state["question"] = "What is my top category?"
    if example_col3.button("Coffee spending"):
        st.session_state["question"] = "How much did I spend on coffee?"
    if example_col4.button("Subscriptions"):
        st.session_state["question"] = "How much did I spend on subscriptions?"

    question = st.text_input(
        "Ask a question about your spending",
        key="question",
        placeholder="e.g. How much did I spend on subscriptions?",
    )
    st.info(
        "Try: What is my total spending? What is my top category? "
        "How much did I spend on coffee?"
    )

    if st.button("Analyze"):
        if uploaded_file is None:
            st.error("Please upload a CSV file first.")
        elif question == "":
            st.error("Please enter a question.")
        else:
            csv_data = df.to_csv(index=False)
            agent = build_agent(csv_data)

            async def _ask(q: str):
                local_answer = answer_question(csv_data, q)
                if local_answer is not None:
                    return local_answer

                result = await agent.run(q)
                if hasattr(result, "response") and result.response is not None:
                    msg = result.response
                    text = getattr(msg, "content", None)
                    if text is not None:
                        return text
                    return str(msg)
                return str(result)

            try:
                with st.spinner("Analyzing your data..."):
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
