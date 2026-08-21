## ADDED Requirements

### Requirement: Authenticated tenant propagation
经过身份验证的后端依赖项 SHALL 将当前 user ID 作为 tenant 范围提供给受保护的数据处理程序。

#### Scenario: Protected handler receives tenant scope
- **WHEN** 已认证的 user 调用知识库、聊天或 AIOps 端点
- **THEN** 处理器 MUST 在下游仓库调用中使用解析后的当前 user ID。

### Requirement: Authenticated authorization failure
后端 SHALL 应区分缺少身份验证和权限不足的情况。

#### Scenario: Missing token remains unauthenticated
- **WHEN** 请求缺少 Bearer 令牌
- **THEN** 后端 MUST 返回统一的未认证错误响应。

#### Scenario: Cross-tenant token is forbidden
- **WHEN** 使用有效的承载令牌访问另一个 user 的受保护资源
- **THEN** 后端 MUST 返回统一的授权错误响应。
