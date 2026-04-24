import os

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai_like import OpenAILike

from tools import make_tools


MODEL = os.environ.get("LLM_MODEL", "qwen3-80b")
API_BASE = os.environ.get("LLM_API_BASE", "https://api.ukisai.academy/v1")
API_KEY = os.environ.get("LLM_API_KEY", "dummy")


SYSTEM_PROMPT = (
    "You are an expense triage assistant. "
    "Use the provided tools to answer questions about the user's transactions. "
    "You MUST call a tool to get real numbers — never guess or invent amounts. "
    "Amounts are in RSD. "
    "Reply in 1-3 short sentences with concrete numbers."
)


def build_agent(csv_data: str) -> FunctionAgent:
    llm = OpenAILike(
        model=MODEL,
        api_base=API_BASE,
        api_key=API_KEY,
        is_function_calling_model=True,
        is_chat_model=True,
        context_window=128000,
    )
    return FunctionAgent(
        tools=make_tools(csv_data),
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
    )
