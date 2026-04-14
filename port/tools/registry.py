from __future__ import annotations

from .base import BaseTool
from .bash_tool import TOOL as BASH_TOOL
from .cron_create_tool import TOOL as CRON_CREATE_TOOL
from .cron_delete_tool import TOOL as CRON_DELETE_TOOL
from .cron_list_tool import TOOL as CRON_LIST_TOOL
from .edit_tool import TOOL as EDIT_TOOL
from .enter_worktree_tool import TOOL as ENTER_WORKTREE_TOOL
from .exit_worktree_tool import TOOL as EXIT_WORKTREE_TOOL
from .glob_tool import TOOL as GLOB_TOOL
from .grep_tool import TOOL as GREP_TOOL
from .notebook_edit_tool import TOOL as NOTEBOOK_EDIT_TOOL
from .powershell_tool import TOOL as POWERSHELL_TOOL
from .read_tool import TOOL as READ_TOOL
from .send_message_tool import TOOL as SEND_MESSAGE_TOOL
from .skill_tool import TOOL as SKILL_TOOL
from .structured_output_tool import TOOL as STRUCTURED_OUTPUT_TOOL
from .task_create_tool import TOOL as TASK_CREATE_TOOL
from .task_get_tool import TOOL as TASK_GET_TOOL
from .task_list_tool import TOOL as TASK_LIST_TOOL
from .task_update_tool import TOOL as TASK_UPDATE_TOOL
from .todo_write_tool import TOOL as TODO_WRITE_TOOL
from .tool_search_tool import TOOL as TOOL_SEARCH_TOOL
from .web_fetch_tool import TOOL as WEB_FETCH_TOOL
from .web_search_tool import TOOL as WEB_SEARCH_TOOL
from .write_tool import TOOL as WRITE_TOOL


TOOLS: list[BaseTool] = [
    READ_TOOL,  # 读取文本文件
    WEB_SEARCH_TOOL,  # 搜索网页结果
    TODO_WRITE_TOOL,  # 维护待办列表
    GREP_TOOL,  # 搜索文件内容
    WEB_FETCH_TOOL,  # 抓取网页正文
    GLOB_TOOL,  # 按模式查找文件
    BASH_TOOL,  # 执行 Bash 命令
    POWERSHELL_TOOL,  # 执行 PowerShell 命令
    EDIT_TOOL,  # 编辑文本文件
    WRITE_TOOL,  # 写入文本文件
    NOTEBOOK_EDIT_TOOL,  # 编辑 Notebook 文件
    SKILL_TOOL,  # 列出或读取技能
    STRUCTURED_OUTPUT_TOOL,  # 输出结构化结果
    TOOL_SEARCH_TOOL,  # 搜索工具定义
    ENTER_WORKTREE_TOOL,  # 创建 git worktree
    EXIT_WORKTREE_TOOL,  # 移除 git worktree
    TASK_CREATE_TOOL,  # 创建任务记录
    TASK_GET_TOOL,  # 查询单个任务
    TASK_LIST_TOOL,  # 列出任务记录
    TASK_UPDATE_TOOL,  # 更新任务记录
    SEND_MESSAGE_TOOL,  # 写入消息信箱
    CRON_CREATE_TOOL,  # 创建计划任务
    CRON_DELETE_TOOL,  # 删除计划任务
    CRON_LIST_TOOL,  # 列出计划任务
]

TOOLS_BY_NAME = {tool.name: tool for tool in TOOLS}


def list_tools() -> list[BaseTool]:
    return list(TOOLS)


def get_tool(name: str) -> BaseTool | None:
    return TOOLS_BY_NAME.get(name)
