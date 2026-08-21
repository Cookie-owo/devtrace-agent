## ADDED Requirements

### Requirement: Auth API contracts
系统 SHALL 为注册、登录、注销和当前user 查询定义共享的认证请求、响应和 OpenAPI 合同。

#### Scenario: Auth paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含 `/auth/register`、`/auth/login`、`/auth/logout` 和 `/auth/me` 路径，并具有统一的响应模式。

#### Scenario: Auth DTOs are shared
- **WHEN** 前端或后端代码需要身份验证请求或响应的结构
- **THEN** 它 MUST 将使用共享的契约定义来处理身份验证 user、令牌响应、注册请求和登录请求。

### Requirement: Auth error code catalog
系统 SHALL 定义统一的认证错误代码，具有稳定的分类、HTTP 状态映射和默认消息。

#### Scenario: Unauthenticated error is reusable
- **WHEN** 端点会拒绝缺失、无效或被吊销的认证令牌
- **THEN** 它 MUST 使用共享的认证错误代码和统一的错误响应封装。

#### Scenario: Invalid credentials error is safe
- **WHEN** 登录凭据无效
- **THEN** 共享错误目录 MUST 仅暴露一个无效凭据代码，无法揭示是邮箱还是密码错误。

### Requirement: Protected API contract security
系统 SHALL 将知识库、聊天和 AIOps API 合同标记为认证表面。

#### Scenario: Protected paths include unauthorized response
- **WHEN** 保护的聊天、知识库或 AIOps OpenAPI 路径将被检查
- **THEN** 它们 MUST 将使用统一的错误响应模式返回 401 响应

#### Scenario: Protected paths declare bearer auth
- **WHEN** 保护聊天、知识库或 AIOps OpenAPI 操作将被检查
- **THEN** 它们通过 OpenAPI 安全方案声明承载者身份验证。
