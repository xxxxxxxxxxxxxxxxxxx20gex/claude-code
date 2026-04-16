# `port` 目录说明

这个目录是 `claude-code` 里的一套轻量 Python 版基础层，目标是把原本偏 TypeScript/Claude Code 主程序中的一部分能力，抽成便于本地脚本、技能和工具复用的 Python 模块。

当前 `port` 主要分成 5 类内容：
- `config/`：配置解析、markdown/frontmatter 加载、output styles、keybindings
- `memory/`：项目记忆路径规则与 markdown 扫描
- `skills/`：Python 版 skill 定义与注册
- `tools/`：Python 版 tool 定义与注册
- `tests/`：对 `config/` 和 `memory/` 的最小 `pytest` 覆盖

说明约定：
- 下面只介绍源码、文档和测试文件
- 不包含 `__pycache__/`、`.state/` 这类缓存或运行时状态目录

## 根目录文件

### [`__init__.py`](/home/lyq/claude-code/port/__init__.py)
`port` 包入口文件。当前只放一个简短包说明，方便把整个 `port` 当成 Python package 导入。

### [`README.md`](/home/lyq/claude-code/port/README.md)
当前这份说明文档。用于快速了解 `port` 目录下每个文件的职责。

## `config/`

### [`config/__init__.py`](/home/lyq/claude-code/port/config/__init__.py)
`config` 子包导出入口。把 frontmatter、markdown loader、output styles、keybindings 的主要类型和函数统一 re-export，方便上层按稳定接口导入。

### [`config/frontmatter.py`](/home/lyq/claude-code/port/config/frontmatter.py)
解析 markdown 顶部 YAML frontmatter 的基础模块。提供 `ParsedMarkdown` 数据结构和 `parse_frontmatter()`，在解析失败时不会直接抛致命异常，而是把错误信息挂在结果对象里返回。

### [`config/markdown_loader.py`](/home/lyq/claude-code/port/config/markdown_loader.py)
统一的 markdown 配置扫描器。支持从给定根目录列表里按子目录名读取 `.md` 文件，提取 frontmatter、正文和来源类型，并提供 `extract_description_from_markdown()` 这样的描述提取辅助函数。

### [`config/output_styles.py`](/home/lyq/claude-code/port/config/output_styles.py)
基于 `markdown_loader` 构建 output style 加载能力。负责把 `output-styles/*.md` 转成结构化的 `OutputStyleSpec`，包括名称、描述、prompt 正文和 `keep-coding-instructions` 标记。

### [`config/keybindings.py`](/home/lyq/claude-code/port/config/keybindings.py)
快捷键配置与解析模块。实现 keystroke/chord 解析、展示字符串生成、`keybindings.json` 读取和默认绑定合并，供 `keybindings_help_skill` 和后续配置相关逻辑复用。

## `docs/`

### [`docs/extraction-roadmap.md`](/home/lyq/claude-code/port/docs/extraction-roadmap.md)
后续抽取方向的中文思路文档。记录了 `hooks`、`permissions`、`structured IO`、`remote session`、`plugin loader` 等高耦合模块为什么这轮不做、未来适合什么时候做、以及建议先抽哪一层。

## `memory/`

### [`memory/__init__.py`](/home/lyq/claude-code/port/memory/__init__.py)
`memory` 子包导出入口。把 auto-memory 路径函数、扫描函数和 manifest 格式化函数统一暴露给外部调用。

### [`memory/paths.py`](/home/lyq/claude-code/port/memory/paths.py)
项目记忆路径规则模块。负责判断 auto-memory 是否启用，计算记忆根目录、项目级 memory 目录、`MEMORY.md` 入口文件以及按日期组织的 daily log 路径。

### [`memory/scan.py`](/home/lyq/claude-code/port/memory/scan.py)
记忆 markdown 扫描模块。负责扫描 memory 目录下的 `.md` 文件，读取 `description` 和 `type` frontmatter，生成 `MemoryHeader` 列表，并把这些条目格式化成便于给模型或技能使用的 manifest 文本。

## `skills/`

### [`skills/__init__.py`](/home/lyq/claude-code/port/skills/__init__.py)
`skills` 包初始化文件。目前主要用于把这个目录当作 Python 包组织，没有复杂逻辑。

### [`skills/base.py`](/home/lyq/claude-code/port/skills/base.py)
所有 Python skill 的基础抽象层。定义了 `SkillSpec` 数据结构和 `BaseSkill` 基类，负责统一 skill 元数据、prompt 构造方式以及 `spec()` 导出行为。

### [`skills/registry.py`](/home/lyq/claude-code/port/skills/registry.py)
skill 注册表。集中导入所有 Python skill，维护 `SKILLS`、`SKILLS_BY_NAME`，并提供 `list_skills()` / `get_skill()` 这类统一访问入口。

### [`skills/batch_skill.py`](/home/lyq/claude-code/port/skills/batch_skill.py)
`batch` 技能定义。用于引导大规模批量改动的拆分、分组和并行执行规划。

### [`skills/claude_api_skill.py`](/home/lyq/claude-code/port/skills/claude_api_skill.py)
`claude-api` 技能定义。提供 Claude API、Agent SDK、模型调用等相关使用指导。

### [`skills/claude_in_chrome_skill.py`](/home/lyq/claude-code/port/skills/claude_in_chrome_skill.py)
`claude-in-chrome` 技能定义。面向浏览器自动化、网页交互或 Chrome 相关工作流。

### [`skills/debug_skill.py`](/home/lyq/claude-code/port/skills/debug_skill.py)
`debug` 技能定义。帮助分析 Claude Code 会话里的调试日志、状态信息或异常线索。

### [`skills/keybindings_help_skill.py`](/home/lyq/claude-code/port/skills/keybindings_help_skill.py)
`keybindings-help` 技能定义。现在已经接入 `config/keybindings.py`，会读取当前 `keybindings.json`、给出配置路径、绑定条数、告警信息和 chord 语法示例，不再只是纯静态说明。

### [`skills/loop_skill.py`](/home/lyq/claude-code/port/skills/loop_skill.py)
`loop` 技能定义。用于把提示词、命令或任务调度成周期性执行。

### [`skills/lorem_ipsum_skill.py`](/home/lyq/claude-code/port/skills/lorem_ipsum_skill.py)
`lorem-ipsum` 技能定义。用于生成接近指定 token 数量的占位文本。

### [`skills/remember_skill.py`](/home/lyq/claude-code/port/skills/remember_skill.py)
`remember` 技能定义。用于审查 auto-memory、`CLAUDE.md`、`CLAUDE.local.md` 这类多层记忆内容，并提出整理、提升或清理建议。

### [`skills/schedule_remote_agents_skill.py`](/home/lyq/claude-code/port/skills/schedule_remote_agents_skill.py)
`schedule-remote-agents` 技能定义。帮助规划远程代理的定时触发或调度方式。

### [`skills/simplify_skill.py`](/home/lyq/claude-code/port/skills/simplify_skill.py)
`simplify` 技能定义。用于审查现有实现并收敛成更简单、更稳、更易维护的版本。

### [`skills/skillify_skill.py`](/home/lyq/claude-code/port/skills/skillify_skill.py)
`skillify` 技能定义。用于把一次会话里已经跑顺的流程沉淀成可复用的 skill。

### [`skills/stuck_skill.py`](/home/lyq/claude-code/port/skills/stuck_skill.py)
`stuck` 技能定义。用于排查本机上可能卡死、阻塞或异常缓慢的 Claude Code 会话。

### [`skills/update_config_skill.py`](/home/lyq/claude-code/port/skills/update_config_skill.py)
`update-config` 技能定义。帮助生成或修改 Claude Code 的配置文件内容。

### [`skills/verify_skill.py`](/home/lyq/claude-code/port/skills/verify_skill.py)
`verify` 技能定义。用于验证代码改动、配置变更或流程调整是否真的按预期工作。

## `tests/`

### [`tests/conftest.py`](/home/lyq/claude-code/port/tests/conftest.py)
测试公共配置文件。负责把仓库根目录加入 `sys.path`，确保 `pytest` 运行时可以正确导入 `port` 包。

### [`tests/test_frontmatter_and_loader.py`](/home/lyq/claude-code/port/tests/test_frontmatter_and_loader.py)
覆盖 `frontmatter.py` 和 `markdown_loader.py` 的测试。主要验证 frontmatter 解析、无 frontmatter 场景、非法 YAML 回退、描述提取逻辑和多 root 加载来源标记。

### [`tests/test_output_styles.py`](/home/lyq/claude-code/port/tests/test_output_styles.py)
覆盖 `output_styles.py` 的测试。验证 output style 的加载、frontmatter 字段覆盖和从 markdown 正文回退描述的行为。

### [`tests/test_keybindings.py`](/home/lyq/claude-code/port/tests/test_keybindings.py)
覆盖 `keybindings.py` 和 `keybindings_help_skill.py` 的测试。主要验证按键解析、平台化展示、绑定合并、错误处理，以及 skill 对新 keybindings 模块的接入。

### [`tests/test_memory.py`](/home/lyq/claude-code/port/tests/test_memory.py)
覆盖 `memory/paths.py` 和 `memory/scan.py` 的测试。验证 auto-memory 路径规则、daily log 路径、环境变量控制、memory 扫描排序、`MEMORY.md` 跳过和 manifest 输出。

## `tools/`

### [`tools/__init__.py`](/home/lyq/claude-code/port/tools/__init__.py)
`tools` 包初始化文件。目前主要作为包标记文件，没有额外逻辑。

### [`tools/base.py`](/home/lyq/claude-code/port/tools/base.py)
所有 Python tool 的基础抽象层。定义 `ToolResult` 和 `BaseTool`，统一工具的元数据、输入 schema、成功/失败返回结构和调用方式。

### [`tools/common.py`](/home/lyq/claude-code/port/tools/common.py)
工具公共辅助模块。集中放置路径解析、文件读写、JSON 持久化、子进程执行、网页抓取、DuckDuckGo 搜索、技能发现和本地 `.state` 文件路径常量，是多数工具依赖的底层通用层。

### [`tools/registry.py`](/home/lyq/claude-code/port/tools/registry.py)
工具注册表。集中导入所有 Python tool，维护 `TOOLS`、`TOOLS_BY_NAME`，并提供 `list_tools()` / `get_tool()` 访问接口。

### [`tools/bash_tool.py`](/home/lyq/claude-code/port/tools/bash_tool.py)
`Bash` 工具实现。执行 bash shell 命令并返回标准输出、标准错误与退出码。

### [`tools/powershell_tool.py`](/home/lyq/claude-code/port/tools/powershell_tool.py)
`PowerShell` 工具实现。优先调用 `pwsh`，不可用时回退到传统 `powershell`。

### [`tools/read_tool.py`](/home/lyq/claude-code/port/tools/read_tool.py)
`Read` 工具实现。读取文本文件内容，供上层流程做查看、检查或后续分析。

### [`tools/write_tool.py`](/home/lyq/claude-code/port/tools/write_tool.py)
`Write` 工具实现。写入或追加文本文件内容，适合生成新文件或覆盖目标文件。

### [`tools/edit_tool.py`](/home/lyq/claude-code/port/tools/edit_tool.py)
`Edit` 工具实现。对现有文本文件做局部编辑，适合替换片段或按条件更新内容。

### [`tools/notebook_edit_tool.py`](/home/lyq/claude-code/port/tools/notebook_edit_tool.py)
`NotebookEdit` 工具实现。面向 Jupyter Notebook 文件，支持按 cell 类型等结构化方式编辑 notebook 内容。

### [`tools/glob_tool.py`](/home/lyq/claude-code/port/tools/glob_tool.py)
`Glob` 工具实现。按 glob 模式查找文件路径，适合快速列出候选文件。

### [`tools/grep_tool.py`](/home/lyq/claude-code/port/tools/grep_tool.py)
`Grep` 工具实现。按文本模式搜索文件内容，适合代码或文档中的关键字检索。

### [`tools/web_fetch_tool.py`](/home/lyq/claude-code/port/tools/web_fetch_tool.py)
`WebFetch` 工具实现。抓取网页内容并清洗成纯文本，适合做网页阅读和简单抽取。

### [`tools/web_search_tool.py`](/home/lyq/claude-code/port/tools/web_search_tool.py)
`WebSearch` 工具实现。执行网页搜索并返回结果列表，当前底层依赖 DuckDuckGo 搜索结果页解析。

### [`tools/skill_tool.py`](/home/lyq/claude-code/port/tools/skill_tool.py)
`Skill` 工具实现。扫描预设技能目录，列出或读取可用的 `SKILL.md` 文件。

### [`tools/structured_output_tool.py`](/home/lyq/claude-code/port/tools/structured_output_tool.py)
`StructuredOutput` 工具实现。用于输出结构化数据，不执行实际副作用，常适合流程中的中间格式化或规范化返回。

### [`tools/tool_search_tool.py`](/home/lyq/claude-code/port/tools/tool_search_tool.py)
`ToolSearch` 工具实现。搜索已经导出的 Python 工具定义，帮助快速发现工具能力。

### [`tools/todo_write_tool.py`](/home/lyq/claude-code/port/tools/todo_write_tool.py)
`TodoWrite` 工具实现。维护轻量待办事项列表，数据落在 `.state/todos.json`。

### [`tools/task_create_tool.py`](/home/lyq/claude-code/port/tools/task_create_tool.py)
`TaskCreate` 工具实现。向本地任务存储写入新任务记录。

### [`tools/task_get_tool.py`](/home/lyq/claude-code/port/tools/task_get_tool.py)
`TaskGet` 工具实现。按任务 ID 读取单条任务记录。

### [`tools/task_list_tool.py`](/home/lyq/claude-code/port/tools/task_list_tool.py)
`TaskList` 工具实现。列出当前本地任务记录。

### [`tools/task_update_tool.py`](/home/lyq/claude-code/port/tools/task_update_tool.py)
`TaskUpdate` 工具实现。更新已有任务记录的状态或内容。

### [`tools/send_message_tool.py`](/home/lyq/claude-code/port/tools/send_message_tool.py)
`SendMessage` 工具实现。把消息写入本地消息信箱记录，数据落在 `.state/messages.jsonl`。

### [`tools/cron_create_tool.py`](/home/lyq/claude-code/port/tools/cron_create_tool.py)
`CronCreate` 工具实现。创建本地 cron 计划任务记录。

### [`tools/cron_delete_tool.py`](/home/lyq/claude-code/port/tools/cron_delete_tool.py)
`CronDelete` 工具实现。删除本地保存的 cron 计划任务记录。

### [`tools/cron_list_tool.py`](/home/lyq/claude-code/port/tools/cron_list_tool.py)
`CronList` 工具实现。列出当前本地保存的 cron 计划任务记录。

### [`tools/enter_worktree_tool.py`](/home/lyq/claude-code/port/tools/enter_worktree_tool.py)
`EnterWorktree` 工具实现。创建 git worktree 工作树，并记录本地 worktree 状态。

### [`tools/exit_worktree_tool.py`](/home/lyq/claude-code/port/tools/exit_worktree_tool.py)
`ExitWorktree` 工具实现。移除 git worktree 工作树，并清理本地 worktree 状态记录。

## 相关但不在 `port/` 目录内的文件

### [`pyproject.toml`](/home/lyq/claude-code/pyproject.toml)
虽然它不在 `port/` 目录里，但和 `port` 直接相关。这里声明了 `claude-code-port` 这个 Python 项目的依赖、开发依赖和 `pytest` 测试路径配置。
