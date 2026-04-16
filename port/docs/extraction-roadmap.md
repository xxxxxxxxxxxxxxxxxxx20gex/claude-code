# 其他高耦合模块抽取思路

这份文档记录本轮不实现、但后续值得继续抽取的能力方向。目标不是立刻搬代码，而是帮助下一轮快速判断“值不值得抽”“先抽哪一层”“风险在哪”。

## Hooks

适用场景：
- 需要在工具调用前后插入策略、审计、自动补充上下文
- 需要把本地 Python `port` 接到外部 HTTP 服务、脚本或模型判断流程

抽取价值：
- 扩展性很强，适合作为 `port` 的事件机制基础层
- 一旦落地，`tools`、`skills`、memory 分析都能复用同一套回调结构

依赖风险：
- 上游 hooks 同时涉及权限、异步任务、输出回传、模型调用
- 如果第一刀就抽完整，会把执行引擎和协议层一起带进来

为什么本轮不做：
- 当前 `port` 还没有统一配置层和 memory 基础层
- 先做 hooks 会让接口设计被高耦合执行链路反向绑住

推荐时机：
- 等 `config` 和 `memory` 稳定后再做

推荐先抽：
- 先抽 hook 配置结构和事件枚举
- 再抽最简单的同步 shell/HTTP hook
- 最后再考虑异步 hook registry

## Permissions

适用场景：
- 需要对工具执行做 allow/deny 规则控制
- 需要根据命令、路径、工具名做细粒度的安全策略

抽取价值：
- 能显著提升 `tools` 的可控性
- 适合作为 Bash、PowerShell、Write、Edit 等工具的统一前置层

依赖风险：
- 上游权限系统不只是 parser，还涉及模式切换、分类器、规则持久化
- 一次性抽全会把安全策略与工具执行强绑定

为什么本轮不做：
- 当前 `port` 还没有统一工具执行上下文
- 现在先把配置层和 keybindings/memory 基础设施做好，更容易定义权限输入面

推荐时机：
- 当 `port/tools` 需要更细粒度控制时开始

推荐先抽：
- `permissionRuleParser`
- 最小 allow/deny matcher
- 之后再加 permission mode 与持久化

## Structured IO

适用场景：
- 需要让 `port` 和外部宿主进程之间以结构化消息通信
- 需要把本地代理嵌到别的前端或服务里

抽取价值：
- 能把当前 `port` 从“本地 Python 模块集合”升级为“可嵌入代理内核”
- 对未来 Web UI、桌面壳、远端控制都很关键

依赖风险：
- 会直接碰到 session 协议、消息类型、权限请求与流式输出
- 这不是单纯的 utility，属于执行引擎边界

为什么本轮不做：
- 现在还没有统一的内部配置与记忆层，过早上协议层会扩大范围

推荐时机：
- 当 `port` 需要被别的进程稳定调用时

推荐先抽：
- 最小消息 schema
- stdin/stdout JSONL 编解码
- 之后再补请求-响应跟踪与中断控制

## Remote Session

适用场景：
- 需要远程 agent、远程 REPL、跨进程或跨机器协作
- 需要 viewer/controller 分离

抽取价值：
- 适合和 `schedule_remote_agents_skill` 一类能力结合
- 能把 `port` 的本地执行扩展到远端 session 管理

依赖风险：
- 高度依赖 transport、认证、权限桥接、session 生命周期
- 如果协议层没先稳定，remote 层会非常容易返工

为什么本轮不做：
- 这是明显的第二阶段能力，不是基础层
- 目前先保证本地配置、keybindings、memory 抽取完整更划算

推荐时机：
- Structured IO 稳定之后

推荐先抽：
- Direct-connect 风格的最小 session manager
- 再考虑 websocket transport 和权限请求桥

## Plugin Loader

适用场景：
- 需要让 `port` 按目录装载扩展、命令、skill、hooks
- 需要插件来源、版本和缓存管理

抽取价值：
- 一旦做好，`port` 可以从“内置集合”变成“插件式平台”
- 与本轮新增的 markdown/frontmatter loader 很契合

依赖风险：
- 上游 loader 很重，带 marketplace、依赖解析、缓存、策略校验
- 如果全量照搬，会远超当前 `port` 的实际需要

为什么本轮不做：
- 当前最需要的是内部基础层，不是完整插件生态
- 本轮先让 markdown/frontmatter 具备作为“插件内容基础格式”的能力

推荐时机：
- 当现有 Python skill/tool 已经出现明显扩展管理痛点时

推荐先抽：
- 本地目录插件发现
- markdown 组件装载
- 最后再考虑版本缓存、市场和策略控制

