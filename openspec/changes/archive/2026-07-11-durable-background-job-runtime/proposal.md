## Why

文档索引目前依赖进程内 `asyncio.create_task`，AIOps 诊断依赖浏览器保持 SSE 连接。服务重启或客户端断开时，任务无法可靠恢复，也没有统一的取消、重试、租约和执行历史边界。

## What Changes

- 增加 SQLite 持久化后台任务与事件表，以及 Repository 抽象。
- 增加基于租约的本地 Worker Runtime，支持启动恢复、并发限制、重试、超时和取消。
- 文档索引与 AIOps 诊断统一提交到后台任务运行时。
- AIOps SSE 改为订阅已持久化事件，客户端断开不终止诊断。
- 提供用户范围内的后台任务查询、取消和重试 API。

## Capabilities

### New Capabilities
- `background-job-runtime`: 定义可靠后台任务、租约、恢复、事件流和用户控制能力。

### Modified Capabilities
- `document-indexing-jobs`: 索引任务由持久化 Worker 执行。
- `aiops-diagnosis-tasks`: 诊断与 SSE 订阅解耦。
- `api-and-sse-contracts`: 增加后台任务契约。

## Impact

- SQLite 模型、Alembic 迁移、Repository 和应用生命周期。
- 文档索引调度与 AIOps 诊断端点。
- API contracts、前端任务状态和测试。
