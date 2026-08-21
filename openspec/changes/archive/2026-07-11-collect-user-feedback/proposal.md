## Why

聊天回答、知识引用和 AIOps 报告已经可追溯，但用户无法标记有用性、说明问题或给出纠正内容，系统也没有可用于后续评测和改进的质量数据。

## What Changes

- 增加 owner-scoped 统一反馈模型，覆盖聊天消息、引用、诊断步骤和报告。
- 支持赞同、反对、原因、评论和纠正内容，并允许更新或删除。
- 增加反馈 API 和共享契约，严格验证目标归属。
- 在聊天回答、引用详情、AIOps 步骤与报告中提供紧凑反馈控件。

## Capabilities

### New Capabilities
- `user-feedback`: 定义统一反馈数据、权限、API 和展示行为。

### Modified Capabilities
- `chat-experience`: 回答与引用反馈。
- `aiops-diagnosis-ui`: 步骤与报告反馈。
- `api-and-sse-contracts`: 反馈契约。

## Impact

- SQLite/Alembic、Repository、API contracts。
- 聊天和 AIOps 前端组件及状态管理。
