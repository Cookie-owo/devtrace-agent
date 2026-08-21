## Why

当前聊天输入仍允许浏览器拖拽放大，回车不能直接发送，用户消息气泡还会占用过大的固定宽度；AIOps 右栏同时展示原始证据、载荷和字符串化工具结果，导致长 JSON 淹没真正的执行过程。项目也缺少可直接上传验证的 Skill 样例。

## What Changes

- 聊天输入框禁止拖拽缩放，普通 Enter 直接发送，Shift+Enter 保留换行能力。
- 用户消息气泡按内容自适应宽度并设置合理最大宽度，长文本可换行且不会撑大页面。
- 在项目中提供 5 个符合 `*SKILL.md`、UTF-8、64KB 限制的示例 Skill 文件，供上传、多选和 Agent 注入验证。
- AIOps 右栏移除独立原始证据列表、证据 ID 和载荷 JSON，改为 Planner、Executor、Replanner 的持久化执行链。
- 每个执行步骤显示一句话标题和缩进后的可读输出，不直接渲染任意 JSON。
- 工具调用只默认显示工具名与状态，输出放入默认收起的缩进详情框，并将 SearchLog、知识检索等结果转换为中文摘要。
- 实时时间线不再直接字符串化工具调用输出，避免重复长 JSON。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `chat-experience`: 改进输入键盘行为和用户消息气泡尺寸。
- `chat-prompt-skill-configuration`: 提供 5 个可上传验证的 Skill Markdown 样例。
- `aiops-diagnosis-ui`: 将右栏改为紧凑、可扫描的执行步骤和工具输出视图。
- `aiops-evidence-chain`: 以 Planner、Executor、Replanner 和工具审计为用户可见证据链，不显示原始证据载荷。

## Impact

- Vue 聊天输入、消息列表、AIOps 时间线和右栏执行链组件。
- 前端组件测试与浏览器交互验证。
- `docs/examples/skills/` 下新增 5 个示例文件。
- 不修改后端 API、数据库 schema 或 SSE 契约。
