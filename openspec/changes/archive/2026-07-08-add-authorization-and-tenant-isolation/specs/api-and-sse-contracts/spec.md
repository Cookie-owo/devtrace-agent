## ADDED Requirements

### Requirement: Authorization error code catalog
系统 SHALL 为未获得访问资源权限的已认证调用者定义统一的授权错误代码。

#### Scenario: Forbidden error is reusable
- **WHEN** 一个受保护的端点会拒绝跨tenant访问
- **THEN** 它应与认证类别使用共享错误代码，HTTP 403 状态，并且使用安全的默认消息。

### Requirement: Protected API contract authorization responses
系统 SHALL 除了对认证失败的响应外，还会对授权失败的响应标记受保护的知识库、聊天和 AIOps 操作。

#### Scenario: Protected paths include forbidden response
- **WHEN** 保护的聊天、知识库或 AIOps OpenAPI 路径将被检查
- **THEN** 它们 MUST 将使用统一的错误响应模式返回 403 响应

#### Scenario: Resource id paths are tenant scoped
- **WHEN** 受保护的路径针对特定的知识库、聊天会话或诊断ID
- **THEN** 其合同 MUST 需要持有者认证，并通过共享的授权错误响应描述被禁止的访问。
