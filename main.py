#!/usr/bin/env python3
import os

from pathlib import Path

from agent import Agent
from tools.TodoManager import TodoManager
from tools.Tools import Tools
from utils.ConfigUtils import *

if __name__ == '__main__':
    config_path = os.path.join(Path(__file__).parent.absolute(), "config", "config.yaml")
    data_dir = str(Path(os.getcwd()))+"\\"
    ConfigUtils.save_config(config_path, {"WORKDIR": {"path": data_dir}})
    TODO = TodoManager()
    # 注册工具,properties格式为{"参数名":{"type":"参数类型","description":"参数描述"}}
    Tools.add_tool("bash","运行bash命令",{"command":{"type":"string","description":"bash命令"}},func = Tools.run_bash)
    Tools.add_tool("read_file" ,"读取文件",{"path":{"type":"string","description":"路径"}},func = Tools.read_file)
    Tools.add_tool("write_file" ,"写入文件",{"path":{"type":"string","description":"路径"},"content":{"type":"string","description":"内容"}},
                   func = Tools.write_file)
    Tools.add_tool("todo", "Update task list. Track progress on multi-step tasks.", {
                                                                    "items": {
                                                                        "type": "array",
                                                                        "items": {
                                                                            "type": "object",
                                                                            "properties": {
                                                                                "id": {"type": "string"}, "text": {"type": "string"},
                                                                                "status": {"type": "string", "enum": ["pending", "in_progress", "completed"]}
                                                                            },
                                                                            "required": ["id", "text", "status"]
                                                                        }
                                                                    }},func=TODO.update_todo)
    Tools.add_tool("edit_file","Replace exact text in file.",
                   {"path":{"type":"string","description":"路径"},"old_text":{"type":"string","description":"旧文本"},"new_text":{"type":"string","description":"新文本"}},
                func = Tools.run_edit)
    Tools.add_tool("task","Spawn a subagent with fresh context. It shares the filesystem but not conversation history.",
                   {"prompt": {"type": "string", "description": "Prompt for the subagent"},
                    "description": {"type": "string", "description": "Short description of the task"}})
    agent = Agent.Agent()
    history = []
    history.append({"role": "system", "content": f"""You are a coding agent at {Path.cwd()}.
Use the todo tool to plan multi-step tasks. Mark in_progress before starting, completed when done.
Prefer tools over prose.Use the task tool to delegate exploration or subtasks."""})
    while True:
        try:
            try :
                message = input("\033[94m>> \033[0m")
            except (EOFError, KeyboardInterrupt):
                break
            if message.strip().lower() in ("q", "exit", ""):
                break
            history.append({"role": "user", "content": message})
            agent.sent_message(history)
            response_content = history[-1]["content"]
            print("\033[92m" + response_content + "\033[0m")
        except Exception as e:
            print(f"\033[91m{e}\033[0m")
