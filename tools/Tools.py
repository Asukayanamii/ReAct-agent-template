#!/usr/bin/env python3\
'''
template:
    tools = [
        {
            "type": "function",        # 🔒 写死，不能改
            "function": {              # 🔒 写死，不能改
                "name": "get_current_weather",  # ✅ 可改（函数名）
                "description": "获取指定城市的当前天气",  # ✅ 可改（描述）
                "parameters": {         # 🔒 写死，不能改
                    "type": "object",   # 🔒 写死，不能改
                    "properties": {     # 🔒 写死，不能改
                        # =====================
                        # 下面全部 👉 可自由定义
                        # =====================
                        "city": {  # ✅ 参数名可改
                            "type": "string",  # ✅ 参数类型可改
                            "description": "城市名称"  # ✅ 可改
                        },
                        "unit": {  # ✅ 参数名可改
                            "type": "string",
                            "description": "温度单位",
                            "enum": ["celsius", "fahrenheit"]  # ✅ 可改
                        }
                    },
                    "required": ["city"]  # ✅ 可改（必填参数）
                }
            }
        }
    ]
'''


class Tools:
    tools = []
    @classmethod
    def add_tool(cls,name : str, func_description : str, properties : dict ) -> None:
        Tools.tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": func_description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": list(properties.keys())
                }
            }
        })

    @classmethod
    def get_tools(cls) -> list:
        return Tools.tools