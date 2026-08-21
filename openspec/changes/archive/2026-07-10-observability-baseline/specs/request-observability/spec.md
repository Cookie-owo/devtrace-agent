## ADDED Requirements

### Requirement: Correlated safe request completion logs
后端 SHALL 会分配或尊重请求相关性 ID，并将其作为 `X-Request-ID` 返回，同时发出包含请求 ID、方法、路径、状态和延迟的结构化完成日志。

#### Scenario: Request has no correlation id
- **WHEN** 一个请求省略了 `X-Request-ID`
- **THEN** 后端 MUST 生成一个，将其包含在响应头中，并在完成日志中使用它。

#### Scenario: Request supplies a correlation id
- **WHEN** 一个请求提供 `X-Request-ID`
- **THEN** 后端 MUST 返回相同的 id 并将其包含在完成日志中。

#### Scenario: Request contains credentials
- **WHEN** 一个请求具有授权或提供者凭据
- **THEN** 完成日志 MUST NOT 包括请求头、承载令牌、API 密钥或请求体。

### Requirement: Local operational request metrics
后端 SHALL 通过轻量级指标端点公开本地聚合的请求总数、失败次数和延迟。

#### Scenario: Requests complete
- **WHEN** 通过应用程序完成的请求
- **THEN** 的指标端点 MUST 会报告汇总的请求次数、失败次数和延迟数据，而不包含敏感的请求内容。
