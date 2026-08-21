## Context

聊天 composer 当前只支持 Meta+Enter 发送且 textarea 使用 `resize: vertical`；用户消息容器继承统一 `max-width: 90%`，短消息也会呈现过大的视觉块。AIOps 时间线会对工具输出调用 `JSON.stringify`，右栏证据链又直接展示 `evidence.summary` 和格式化 payload，导致同一批 SearchLog 记录以长 JSON 重复出现。

## Goals / Non-Goals

**Goals:**

- 让聊天输入符合常见 AI 对话习惯：Enter 发送、Shift+Enter 换行、不可拖拽缩放。
- 用户消息气泡按内容宽度收缩，长内容在合理最大宽度内自然换行。
- 提供 5 个可直接上传的 Skill 样例，不需要改动 Skill 后端契约。
- 将 AIOps 右栏变为可扫描的持久化执行链和默认收起的工具调用输出。
- 所有工具输出经过语义摘要，不在时间线、右栏或折叠框中直接显示 JSON 对象字符串。

**Non-Goals:**

- 不修改聊天发送 API、SSE 事件或消息持久化方式。
- 不删除后端持久化的诊断 evidence；仅调整前端可见信息架构。
- 不改变 Planner、Executor、Replanner 或 Report 的执行逻辑。
- 不自动上传示例 Skill 到任何用户账号。

## Decisions

- Composer 在 `keydown` 中识别 Enter：未按 Shift 时阻止默认换行并调用现有 submit；Shift+Enter 保持原生换行。IME 组合输入期间不发送，避免中文候选确认误触。
- textarea 使用 `resize: none` 和受控的紧凑高度。用户气泡使用 `width: fit-content`、`max-width` 和 `overflow-wrap: anywhere`，助手消息继续保持适合长文阅读的宽度。
- 示例 Skill 放在 `docs/examples/skills/`，文件名全部以 `SKILL.md` 结尾，内容为简体中文 Markdown，分别覆盖日志分析、知识检索、API 排障、事件报告和变更风险检查。
- 继续使用现有 `AiopsEvidenceChain` 组件名以减少调用面变化，但其界面语义改为“执行链”。只读取 `chain.steps` 中的 `planner`、`executor`、`replanner`，按 sequence 排序；步骤标题由 phase 和 payload 生成一句中文摘要，输出放在缩进块。
- 工具审计按名称和状态展示，每项使用原生 `<details>`，默认关闭。SearchLog 的 `recordCount/records` 转成最多 5 条可读日志行；知识检索转成命中数量和来源；其他对象转换为受限键值摘要，无法解析时只显示截断文本。
- 实时时间线不显示工具输出正文，只显示工具生命周期；详细输出统一进入右栏，避免重复。

## Risks / Trade-offs

- [Enter 发送可能让习惯 Enter 换行的用户误操作] -> 保留 Shift+Enter 换行，并在输入框下提供简短提示。
- [历史工具摘要可能是截断或无效 JSON] -> 使用安全解析和纯文本截断回退，界面不抛异常。
- [步骤 payload 结构随节点变化] -> 每个 phase 使用容错字段读取，缺失时显示状态与“未返回结构化输出”。
- [示例 Skill 被误认为内置启用] -> README 说明这些文件仅用于手动上传验证，系统不会自动加载。

## Migration Plan

无需数据库或 API 迁移。部署后现有聊天和诊断历史立即使用新展示方式；回滚仅涉及 Vue 组件和示例文档。

## Open Questions

无。
