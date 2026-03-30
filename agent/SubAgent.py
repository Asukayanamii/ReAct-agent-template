from pathlib import Path

from tools.Tools import Tools


class SubAgent():
    def __init__(self):
        self.message = [{"role": "system", "content": f"You are a coding subagent at {Path.cwd()}. Complete the given task, then summarize your findings."}]
    def run_SubAgent(self,task : str) -> str:
        from agent.Agent import Agent
        agent = Agent()
        sub_agent_tools = [tool for tool in Tools.get_tools() if tool["function"]["name"] != "task" and tool["function"]["name"] != "todo"]
        agent.sent_message( self.message + [{"role": "user", "content": task}], tools=sub_agent_tools)
        return self.message[-1]["content"]


