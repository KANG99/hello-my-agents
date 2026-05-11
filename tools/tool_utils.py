from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import json
import asyncio


class ToolExecutor:
    """
    一个工具执行器，负责管理和执行工具。
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self,model: BaseModel, name: str, func: callable):
        """
        向工具箱中注册一个新工具。
        """
        if name in self.tools:
            print(f"警告：工具 '{name}' 已存在，将被覆盖。")
        
        self.tools[name] = {"description": func.__doc__,  "func": func,"param_schema": model.schema()}
        print(f"工具 '{name}' 已注册。")

    def get_tool(self, name: str) -> callable:
        """
        根据名称获取一个工具的执行函数。
        """
        return self.tools.get(name, {}).get("func")

    def get_available_tools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        """
        return "\n".join([
            f"{name}: {info['description']}" 
            for name, info in self.tools.items()
        ])

    def get_tool_list(self) -> list:
        """
        获取所有已注册工具的schema列表。
        """
        return [
            generate_openai_tool_schema(name, info["description"],info["param_schema"])
            for name, info in self.tools.items()
        ]


def generate_openai_tool_schema(function_name: str, function_description: str,param_schema: dict) -> dict:
    """生成符合OpenAI格式的工具Schema"""
    return {
        "type": "function",
        "function": {
            "name": function_name,
            "description": function_description,
            "parameters": param_schema
        }
    }

def handle_tool_call(tool_call, toolExecutor: ToolExecutor):
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    return toolExecutor.get_tool(function_name)(**arguments)


def create_tool_response_message(tool_call, tool_result):
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": tool_call.function.name,
        "content": json.dumps(tool_result)}


