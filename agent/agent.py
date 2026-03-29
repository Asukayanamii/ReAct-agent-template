#!/usr/bin/env python3
import os
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
from tools import Tools

class agent:
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

    def sent_message(self,message: list,system_content: str = DEFAULT_SYSTEM_CONTENT, stream: bool = False,tools: list = tools):
        response = self.client.chat.completions.create(
            model = self.MODEL_ID,
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": message},
            ],
            tools=tools,  # 把工具传给模型
            tool_choice="auto",  # 自动判断是否调用工具（默认值）
            stream = stream
        )
