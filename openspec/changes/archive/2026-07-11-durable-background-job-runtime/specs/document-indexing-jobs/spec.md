## MODIFIED Requirements

### Requirement: Non-blocking indexing execution
文档索引 SHALL 作为持久化 `document_index` 后台任务执行，请求 MUST 立即返回，服务重启后 queued 或租约过期的索引 MUST 恢复。

#### Scenario: Indexing task is accepted
- **WHEN** 用户创建或重试文档索引任务
- **THEN** API MUST 同时创建业务索引记录和 durable background job，并返回 202。
