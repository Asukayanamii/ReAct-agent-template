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
import os
import subprocess
from pathlib import Path
from utils.ConfigUtils import *

class Tools:
    tools = []
    tool_handlers = {}
    @classmethod
    def add_tool(cls,name : str, func_description : str, properties : dict , func : callable = None) -> None:
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
        if func:
            Tools.tool_handlers[name] = func


    @classmethod
    def get_tools(cls) -> list:
        return Tools.tools
    @classmethod
    def run_bash(cls,command: str) -> str:
        #去除了"shutdown"
        dangerous = ["rm -rf /", "sudo", "reboot", "> /dev/"]
        if any(d in command for d in dangerous):
            return "Error: Dangerous command blocked"
        try:
            r = subprocess.run(command, shell=True, cwd=os.getcwd(),
                               capture_output=True, text=True, timeout=120,encoding="utf-8",errors='replace')
            out = (r.stdout + r.stderr).strip()
            return out[:50000] if out else "(no output)"
        except subprocess.TimeoutExpired:
            return "Error: Timeout (120s)"
        except Exception as e:
            return f"Error: {e}"
    @classmethod
    def safe_path(cls,path: str) -> str:
        BASE_PATH = Path(__file__).parent.parent.absolute()
        CONFIG_PATH = os.path.join(BASE_PATH, "config", "config.yaml")
        WORKDIR = ConfigUtils.load_config(CONFIG_PATH)["WORKDIR"]["path"]
        path = Path(WORKDIR + path)
        p = Path(WORKDIR)
        if not path.is_relative_to(p):
            raise ValueError(f"Path escapes workspace: {path}")
        return path.resolve()
    @classmethod
    def read_file(cls,path: str) -> str:
        path = Tools.safe_path(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "File not found"
        except PermissionError:
            return "Permission denied"
        except Exception as e:
            return f"Error: {e}"

    @classmethod
    def write_file(cls,path: str, content: str) -> str:
        path = Tools.safe_path(path)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
                return "OK"
        except FileNotFoundError:
            return "File not found"
        except PermissionError:
            return "Permission denied"
        except Exception as e:
            return f"Error: {e}"

    @classmethod
    def run_edit(cls,path: str, old_text: str, new_text: str) -> str:
        try:
            fp = Tools.safe_path(path)
            content = fp.read_text()
            if old_text not in content:
                return f"Error: Text not found in {path}"
            fp.write_text(content.replace(old_text, new_text, 1))
            return f"Edited {path}"
        except Exception as e:
            return f"Error: {e}"




if __name__ == '__main__':
    print("hello")