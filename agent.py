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
    # streaming=True uses astream_chat_with_tools, which some OpenAI-compatible
    # backends mishandle: tool_calls never populate and the model leaves markers
    # like "{{tool_call}}" in plain text. Non-streaming achat usually fixes that.
    # initial_tool_choice="required" nudges the API to return real tool_calls on
    # the first turn (falls back via env if a provider rejects "required").
    _first_tool = os.environ.get("AGENT_FIRST_TOOL_CHOICE", "required")
    return FunctionAgent(
        tools=make_tools(csv_data),
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
        streaming=False,
        initial_tool_choice=_first_tool if _first_tool else None,
    )
