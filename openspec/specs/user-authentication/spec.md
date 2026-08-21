# user-authentication Specification

## Purpose

定义 user 身份、凭证存储、会话令牌生命周期、已认证的后端依赖关系以及前端认证状态。
## Requirements
### Requirement: User registration
系统 SHALL 允许新的 user 使用电子邮件、显示名称和密码进行注册。

#### Scenario: 成功注册创建已认证的会话
- **WHEN** 一个新 user 使用唯一电子邮件和有效密码进行注册
- **THEN** 后端 MUST 创建 user，仅存储安全密码哈希，创建认证会话，并在统一的成功响应中返回当前 user 和承载令牌。

#### Scenario: Duplicate email is rejected
- **WHEN** 注册时使用的邮箱已被分配给一个 user
- **THEN** 后端 MUST 返回统一的业务错误响应，不泄露密码数据。

### Requirement: User login and logout
系统 SHALL 允许已注册的 user 用户使用可撤销的会话进行登录和注销。

#### Scenario: 成功登录返回会话令牌
- **WHEN** 一个 user 提交有效的电子邮件和密码
- **THEN** 后端 MUST 验证密码哈希，并在统一的成功响应中返回当前 user 加上承载令牌。

#### Scenario: Invalid login fails safely
- **WHEN** 一个 user 提交了未知的电子邮件或无效的密码
- **THEN** 后端 MUST 返回相同的统一身份验证错误结构，而不会指出哪个凭据出错。

#### Scenario: Logout revokes session
- **WHEN** 一个经过身份验证的 user 注销
- **THEN** 后端 MUST 撤销当前会话，因此相同的令牌将无法再访问已认证的 API。

### Requirement: ### 需求：当前 user 查询
系统 SHALL 必须公开一个经过身份验证的当前-user 端点。

#### Scenario: Authenticated user reads profile
- **WHEN** 请求包含有效的承载会话令牌
- **THEN** 后端 MUST 在统一的成功响应中返回当前 user 的 id、电子邮件、显示名称和创建时间戳。

#### Scenario: Missing or revoked token fails
- **WHEN** 一个请求缺少令牌或使用了被吊销/未知的令牌
- **THEN** 后端 MUST 返回统一的未认证错误响应。

### Requirement: Authenticated access control
系统 SHALL 需要对知识库、聊天和 AIOps 数据 APIs 进行身份验证。

#### Scenario: Protected data rejects anonymous request
- **WHEN** 未经过身份验证的请求访问受保护的知识库、聊天或 AIOps 端点
- **THEN** 后端 MUST 返回统一的未经过身份验证的错误响应。

#### Scenario: Protected data accepts authenticated request
- **WHEN** 身份验证的请求访问受保护的知识库、聊天或 AIOps 端点
- **THEN** 后端 MUST 接受请求并通过共享的身份验证依赖项解析当前 user

### Requirement: Frontend authentication experience
前端 SHALL 支持登录、注册、注销、当前 user 加载和持久化的认证状态。

#### Scenario: User can register and remain authenticated
- **WHEN** 前端注册成功
- **THEN** 前端 MUST 存储返回的令牌，显示已认证的应用外壳，并在重新加载后保留认证状态。

#### Scenario: User can log in and log out
- **WHEN** 登录成功，之后 user 注销
- **THEN** 前端 MUST 在登录期间发送经过身份验证的 API 请求，在注销时清除持久化的身份验证状态，并返回到未经过身份验证的表单。

#### Scenario: Auth error is displayed
- **WHEN** 一个认证 API 返回统一的错误响应
- **THEN** 前端 MUST 显示错误信息，而不依赖于临时的错误结构。

### Requirement: Authenticated tenant propagation
经过身份验证的后端依赖 SHALL 将当前 user ID 作为 tenant 范围提供给受保护的数据处理程序。

#### Scenario: Protected handler receives tenant scope
- **WHEN** 已认证的 user 调用知识库、聊天或 AIOps 端点
- **THEN** 处理器 MUST 在下游仓库调用中使用解析后的当前 user ID。

### Requirement: Authenticated authorization failure
后端 SHALL 能够区分缺少身份验证和权限不足的情况。

#### Scenario: Missing token remains unauthenticated
- **WHEN** 请求缺少承载令牌
- **THEN** 后端 MUST 返回统一的未认证错误响应。

#### Scenario: Cross-tenant token is forbidden
- **WHEN** 使用有效的承载令牌访问另一个 user 的受保护资源
- **THEN** 后端 MUST 返回统一的授权错误响应
