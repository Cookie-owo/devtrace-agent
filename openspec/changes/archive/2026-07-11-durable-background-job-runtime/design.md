## Context

项目是本地优先单进程应用，但任务状态已经持久化。缺失的是可恢复的执行控制面。引入外部 Redis/Celery 会扩大安装面，因此先使用 SQLite 租约队列，同时保留未来替换外部 Worker 的 Repository 边界。

## Goals / Non-Goals

**Goals:**
- 服务重启后恢复 queued 或过期 running 任务。
- 文档索引和 AIOps 使用同一任务生命周期。
- SSE 只订阅事件，不持有任务执行权。
- 支持用户查询、取消、失败重试和隔离。

**Non-Goals:**
- 不实现跨机器分布式调度。
- 不替换现有业务任务表、诊断证据或 LangGraph checkpoint。

## Decisions

### SQLite 租约队列

`background_jobs` 保存 kind、resource、payload、状态、attempt、availableAt、leaseOwner、leaseExpiresAt、cancelRequestedAt 和错误。Worker 原子领取 queued 或租约过期任务，执行期间续租，终态释放租约。

### 持久化事件日志

`background_job_events` 按 job 和 sequence 保存共享 SSE payload。AIOps handler 将现有诊断事件逐条写入；订阅端从指定 sequence 轮询，直到 job 终态。浏览器断开不会取消 Worker。

### Handler Registry

Runtime 只理解任务生命周期，不依赖文档或 AIOps 细节。应用启动时注册 `document_index` 与 `aiops_diagnosis` handler。Repository 和 handler registry 可在未来迁移到独立 Worker。

### 取消和重试

queued 任务立即取消；running 任务设置 cancel requested，Worker 在事件边界协作停止。只有 failed/cancelled 可创建新 job 重试，原任务保留审计链。

## Risks / Trade-offs

- SQLite 只适合本地单机；租约与原子更新减少重复执行但不承诺跨区域 exactly-once。
- AIOps 事件轮询有轻微延迟，换取断线恢复与简单部署。

## Migration Plan

1. 增加表和 Repository。
2. 接入 Runtime 生命周期和 handlers。
3. 切换索引与诊断端点。
4. 验证重启恢复、断线继续、取消和重试。
