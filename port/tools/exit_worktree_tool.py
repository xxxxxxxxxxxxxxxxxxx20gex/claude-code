"""ExitWorktree 工具：移除 git worktree 工作树。

移除成功后会同步更新本地 worktree 状态记录。
"""

from __future__ import annotations

from pathlib import Path

from .base import BaseTool, ToolResult
from .common import WORKTREE_STATE_FILE, load_json, resolve_path, run_process, save_json


class ExitWorktreeTool(BaseTool):
    name = "ExitWorktree"
    description = "Remove a git worktree and update the local worktree state file."
    input_schema = {
        "type": "object",
        "properties": {
            "repo": {"type": "string"},
            "path": {"type": "string"},
            "force": {"type": "boolean"},
        },
        "required": ["repo", "path"],
    }

    def run(self, *, repo: str, path: str, force: bool = False) -> ToolResult:
        repo_path = resolve_path(repo)
        worktree_path = resolve_path(path)
        command = ["git", "-C", str(repo_path), "worktree", "remove"]
        if force:
            command.append("--force")
        command.append(str(worktree_path))
        result = run_process(command, cwd=str(repo_path))
        if result["returncode"] != 0:
            return self.fail("Failed to remove worktree", command=" ".join(command), stderr=result["stderr"])
        state = load_json(WORKTREE_STATE_FILE, {"items": []})
        items = state.get("items", [])
        state["items"] = [
            item
            for item in items
            if Path(item.get("path", "")).resolve() != worktree_path.resolve()
        ]
        save_json(WORKTREE_STATE_FILE, state)
        return self.ok(result, worktree_path=str(worktree_path))


TOOL = ExitWorktreeTool()
