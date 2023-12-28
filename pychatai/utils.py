"""Utility functions and constants."""

from enum import Enum
from functools import partial
from typing import Callable

from langchain.tools import DuckDuckGoSearchRun, WikipediaQueryRun, YouTubeSearchTool
from langchain.utilities import WikipediaAPIWrapper
from langchain_experimental.tools.python.tool import PythonREPLTool


class OutputType(str, Enum):
    """Enum for the type of output to be generated."""

    TOKEN = "token"  # noqa: S105
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    AGENT_FINISH = "agent_finish"
    LLM_ERROR = "llm_error"
    INTERRUPT = "interrupt"


class MessagePartType(str, Enum):
    """Enum for the type of message part."""

    TEXT = "text"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    AGENT_FINISH = "agent_finish"
    ERROR = "error"
    INTERRUPT = "interrupt"


plugin_tool: dict[str, Callable] = {
    "Python": PythonREPLTool,
    "DuckDuckGo": DuckDuckGoSearchRun,
    "Wikipedia": partial(WikipediaQueryRun, api_wrapper=WikipediaAPIWrapper()),
    "YouTube": YouTubeSearchTool,
}

providers_models = {
    "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-1106-preview"],
    "anthropic": ["claude-2", "claude-instant-1"],
}
