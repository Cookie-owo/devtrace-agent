## ADDED Requirements

### Requirement: Background job API contracts
共享契约 SHALL 定义后台任务列表、详情、取消、重试和事件订阅结构，包含 kind、resource、status、attempt、时间和安全错误。

#### Scenario: 前端观察后台任务
- **WHEN** 前端查询当前用户任务
- **THEN** 前后端 MUST 使用同一 `BackgroundJob` 契约且状态 MUST 限定为 queued、running、succeeded、failed、cancelled。
