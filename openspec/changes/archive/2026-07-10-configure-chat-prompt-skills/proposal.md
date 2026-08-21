## Why

当前聊天只能使用固定的系统提示词，用户无法明确控制回答方式，也看不到工具调用或模型推理过程的可展开上下文。需要让用户在网页端选择并保存自己的对话装配，同时保持实际工具与模型行为可追溯。

## 什么更改

- 提供用户级系统提示词预设单选和受控 Skill 多选配置；首次访问自动创建默认系统提示词和默认 `frontend-design` Skill。
- 将已保存的装配动态注入后续聊天 Agent 的系统消息，而不是在前端临时拼接或依赖本机环境。
- 通过共享 API 契约读取和更新配置，并用 SQLite Repository 按用户持久化；刷新网页后恢复同一选择。
- 将助手消息下的工具调用和可用深度思考过程呈现为默认折叠的中文详情区，不伪造模型没有返回的推理内容。
- 在对话页提供紧凑的配置入口和可见的当前装配摘要，不改变现有聊天会话、SSE 或权限边界。

## 功能

### 新功能
- `chat-prompt-skill-configuration`: 定义每个用户的提示词与 Skill 装配、默认值、持久化和聊天应用行为。

### 修改后的功能
- `api-and-sse-contracts`: 增加用户聊天装配的 typed HTTP 协议与可选的流式推理上下文表达。
- `memory-repositories`: 为用户级聊天装配配置增加 Repository 边界和 SQLite 持久化。
- `stream-rag-chat`: 使用已保存的装配构建每次 Agent 的系统消息，并传递真实工具与可用推理上下文。
- `chat-experience`: 展示和编辑当前装配，并以折叠详情展示工具调用与模型返回的思考过程。

## 影响

影响 `packages/api-contracts`、`apps/backend` 的 SQLAlchemy/Alembic、Repository、聊天服务和 FastAPI 路由，以及 `apps/frontend` 的聊天 Store、组件和测试。不会调用 DashScope 私有 SDK，不改变现有会话数据或用户隔离规则。
