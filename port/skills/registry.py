from __future__ import annotations

from .base import BaseSkill
from .batch_skill import SKILL as BATCH_SKILL
from .claude_api_skill import SKILL as CLAUDE_API_SKILL
from .claude_in_chrome_skill import SKILL as CLAUDE_IN_CHROME_SKILL
from .debug_skill import SKILL as DEBUG_SKILL
from .keybindings_help_skill import SKILL as KEYBINDINGS_HELP_SKILL
from .loop_skill import SKILL as LOOP_SKILL
from .lorem_ipsum_skill import SKILL as LOREM_IPSUM_SKILL
from .remember_skill import SKILL as REMEMBER_SKILL
from .schedule_remote_agents_skill import SKILL as SCHEDULE_REMOTE_AGENTS_SKILL
from .simplify_skill import SKILL as SIMPLIFY_SKILL
from .skillify_skill import SKILL as SKILLIFY_SKILL
from .stuck_skill import SKILL as STUCK_SKILL
from .update_config_skill import SKILL as UPDATE_CONFIG_SKILL
from .verify_skill import SKILL as VERIFY_SKILL


SKILLS: list[BaseSkill] = [
    BATCH_SKILL,  # 批量拆分与并行执行
    CLAUDE_API_SKILL,  # Claude API 与 SDK 指南
    CLAUDE_IN_CHROME_SKILL,  # 浏览器自动化
    DEBUG_SKILL,  # 调试日志排查
    KEYBINDINGS_HELP_SKILL,  # 快捷键配置帮助
    LOOP_SKILL,  # 周期性任务调度
    LOREM_IPSUM_SKILL,  # 占位文本生成
    REMEMBER_SKILL,  # 记忆层整理
    SCHEDULE_REMOTE_AGENTS_SKILL,  # 远程代理调度
    SIMPLIFY_SKILL,  # 代码简化与复查
    SKILLIFY_SKILL,  # 会话流程沉淀为技能
    STUCK_SKILL,  # 卡死会话诊断
    UPDATE_CONFIG_SKILL,  # 配置更新指导
    VERIFY_SKILL,  # 改动效果验证
]

SKILLS_BY_NAME = {skill.name: skill for skill in SKILLS}


def list_skills() -> list[BaseSkill]:
    return list(SKILLS)


def get_skill(name: str) -> BaseSkill | None:
    return SKILLS_BY_NAME.get(name)
