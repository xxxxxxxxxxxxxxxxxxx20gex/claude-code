"""EnterWorktree 工具：创建 git worktree 工作树。

创建结果会记录到本地状态文件，便于后续清理和追踪。
"""

from __future__ import annotations

from pathlib import Path

from .base import BaseTool, ToolResult
from .common import WORKTREE_STATE_FILE, load_json, resolve_path, run_process, save_json, slugify, utc_now


class EnterWorktreeTool(BaseTool):
    name = "EnterWorktree"
    description = "Create a git worktree and record it in the local worktree state file."
    input_schema = {
        "type": "object",
        "properties": {
            "repo": {"type": "string"},
            "path": {"type": "string"},
            "ref": {"type": "string"},
            "detach": {"type": "boolean"},
        },
        "required": ["repo"],
    }

    def run(
        self,
        *,
        repo: str,
        path: str | None = None,
        ref: str = "HEAD",
        detach: bool = True,
    ) -> ToolResult:
        repo_path = resolve_path(repo)
        if not (repo_path / ".git").exists() and not repo_path.exists():
            return self.fail(f"Repository path not found: {repo_path}")
        target = resolve_path(path, cwd=str(repo_path)) if path else repo_path.parent / f"{repo_path.name}-{slugify(ref)}-worktree"
        command = ["git", "-C", str(repo_path), "worktree", "add"]
        if detach:
            command.append("--detach")
        command.extend([str(target), ref])
        result = run_process(command, cwd=str(repo_path))
        if result["returncode"] != 0:
            return self.fail("Failed to create worktree", command=" ".join(command), stderr=result["stderr"])
        state = load_json(WORKTREE_STATE_FILE, {"items": []})
        state["items"].append(
            {
                "repo": str(repo_path),
                "path": str(Path(target).resolve()),
                "ref": ref,
                "detach": detach,
                "created_at": utc_now(),
            }
        )
        save_json(WORKTREE_STATE_FILE, state)
        return self.ok(result, worktree_path=str(Path(target).resolve()))


TOOL = EnterWorktreeTool()
