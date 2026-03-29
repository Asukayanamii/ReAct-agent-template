#!/usr/bin/env python3
from agent import agent
from tools.Tools import Tools

if __name__ == '__main__':
    Tools.add_tool("bash","运行bash命令",{"command":{"type":"string","description":"bash命令"}})
    agent = agent.agent()
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
