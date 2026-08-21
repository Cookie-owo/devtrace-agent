## 1. 持久化与运行时

- [x] 1.1 增加 background job/event ORM、迁移和 Repository
- [x] 1.2 实现租约领取、恢复、重试、取消和事件持久化
- [x] 1.3 在应用生命周期启动和关闭 Worker Runtime

## 2. 业务接入

- [x] 2.1 将文档索引调度切换为 durable job handler
- [x] 2.2 将 AIOps 执行切换为 durable job，并让 SSE 订阅持久化事件
- [x] 2.3 增加后台任务查询、取消和重试 API 契约

## 3. 验证

- [x] 3.1 覆盖恢复、租约、隔离、取消、重试和 SSE 重连测试
- [x] 3.2 运行后端、契约、前端与 OpenSpec 验证
