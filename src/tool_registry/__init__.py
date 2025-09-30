# src/tool_registry/__init__.py
from typing import Callable, List

from mcp.server.fastmcp import FastMCP

ToolRegistrar = Callable[[FastMCP], None]


def register_all_tools(mcp: FastMCP, registrars: List[ToolRegistrar]):
    """Register all tools from provided registrars"""
    for registrar in registrars:
        registrar(mcp)
