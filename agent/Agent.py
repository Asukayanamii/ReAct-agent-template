#!/usr/bin/env python3
import os

import json

from openai import OpenAI
from dotenv import load_dotenv

from tools.TodoManager import TodoManager
from tools.Tools import Tools

class Agent:
    API_KEY = None
    BASE_URL = None
    MODEL_ID = None
    tools = None
    DEFAULT_SYSTEM_CONTENT = "You are a helpful assistant"
    def __init__(self):
        # 初始化
        load_dotenv()
        self.API_KEY = os.getenv("API_KEY")
        self.BASE_URL = os.getenv("BASE_URL")
        self.MODEL_ID = os.getenv("MODEL_ID")
        self.tools = Tools.get_tools()
        self.client = OpenAI(
            api_key = self.API_KEY,
            base_url = self.BASE_URL)


    def sent_message(self,message: list, stream: bool = False,tools: list = Tools.get_tools()):
        rounds_since_todo = 0
        while True:
            response = self.client.chat.completions.create(
                model = self.MODEL_ID,
                messages = message,
                tools=tools,  # 把工具传给模型
                tool_choice="auto",  # 自动判断是否调用工具（默认值）
                stream = stream
            )
            content = response.choices[0].message.content
            stop_reason = response.choices[0].finish_reason
            if stop_reason!= "tool_calls":
                message.append({"role" : "assistant", "content" : content})
                return
            # results = []
            used_todo = False
            message.append({"role" : "assistant", "content" : None ,
                            "tool_calls": [{"id": tool_call.id,
                            "type": "function",
                            "function": {"name": tool_call.function.name,
                            "arguments": tool_call.function.arguments}} for tool_call in response.choices[0].message.tool_calls]})
            for tool_call in response.choices[0].message.tool_calls:
                tool_id = tool_call.id
                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments
                arguments = json.loads(arguments)
                print(f"\033[33m$ {arguments}\033[0m")
                func = Tools.tool_handlers[tool_name]
                result = func(**arguments) if func else f"Unknown tool: {tool_name}"
                print(f"\033[34m{tool_name} result:{result}\033[0m")
                # results.append({"type" : "tool_result","tool_call_id": tool_id,"content": result})
                message.append({"role" : "tool", "tool_call_id": tool_id, "content": result })
                if tool_name == "todo":
                    used_todo = True
            rounds_since_todo = 0 if used_todo else rounds_since_todo + 1
            if rounds_since_todo > 3:
                message.append({"role" : "user", "content" : "reminder:Update your todos."})


