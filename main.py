#!/usr/bin/env python3
from agent import Agent
from tools.TodoManager import TodoManager
from tools.Tools import Tools

if __name__ == '__main__':
    TODO = TodoManager()
    # 注册工具,properties格式为{"参数名":{"type":"参数类型","description":"参数描述"}}
    Tools.add_tool("bash","运行bash命令",{"command":{"type":"string","description":"bash命令"}},func = Tools.run_bash)
    Tools.add_tool("read_file" ,"读取文件",{"path":{"type":"string","description":"路径"}},func = Tools.read_file)
    Tools.add_tool("write_file" ,"写入文件",{"path":{"type":"string","description":"路径"},"content":{"type":"string","description":"内容"}},
                   func = Tools.write_file)
    Tools.add_tool("todo", "TODO", {
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
                                                                    }
    },func=TODO.update_todo)
    agent = Agent.Agent()
    history = []
    history.append({"role": "system", "content": """CRITICAL: You are running on WINDOWS (cmd.exe), NOT Linux! 

        RULES:
        1. NEVER use Unix commands: cat, <<, heredoc, ls, rm, etc.
        2. For file creation, use ONLY: python -c "open('file.py','w',encoding='utf-8').write('content')"
        3. Keep commands SINGLE-LINE, avoid multi-line strings
        4. If a command fails ONCE, try COMPLETELY different approach
        5. Use UTF-8 encoding for Chinese text
        6. Windows path uses backslash: C:\\path\\to\\file
        
        REMEMBER: WINDOWS != LINUX. Adapt your commands accordingly!"""})
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
