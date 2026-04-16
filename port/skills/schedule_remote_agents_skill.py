"""schedule-remote-agents 技能：帮助配置远程代理的定时触发。"""

from __future__ import annotations

from .base import BaseSkill


class ScheduleRemoteAgentsSkill(BaseSkill):
    name = "schedule-remote-agents"
    description = "Set up or manage scheduled remote agents and remote triggers."
    when_to_use = "当用户想创建、查看或调整远程代理的定时触发任务时使用。"
    allowed_tools = ["RemoteTrigger", "AskUserQuestion"]
    user_invocable = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/scheduleRemoteAgents.ts"

    def get_prompt_text(self) -> str:
        return """# Schedule Remote Agents Skill

帮助用户配置远程代理的计划任务和触发器。

## Workflow
1. 检查当前环境是否满足远程执行前提
2. 发现可用连接器和远端环境
3. 让用户确认希望的调度方式
4. 创建或更新远程触发配置
"""


SKILL = ScheduleRemoteAgentsSkill()
