## ADDED Requirements

### Requirement: Auth memory schema
后端 SHALL 通过 user 和可撤销的认证会话扩展内存数据库模式。

#### Scenario: User and session tables are migrated
- **WHEN** Alembic 将全新的 SQLite 数据库升级到最新版本
- **THEN** 的内存模式 MUST 包含 `users` 和 `auth_sessions` 表，并为电子邮件和令牌哈希查找建立了索引。

#### Scenario: Plaintext secrets are not stored
- **WHEN** 一个 user 注册或登录
- **THEN** 的数据库 MUST 存储密码哈希和令牌哈希，而不是明文密码或明文承载令牌。

### Requirement: Auth repository boundary
后端 SHALL 为 users 和认证会话提供仓库操作，而不会将 SQLAlchemy 模型泄露给认证服务。

#### Scenario: 用户查找支持电子邮件和ID
- **WHEN** 身份验证服务需要注册或认证一个 user
- **THEN** 仓库 MUST 支持创建 user 并通过规范化的电子邮件或ID查找 user。

#### Scenario: 会话查找支持令牌哈希
- **WHEN** 身份验证依赖项验证承载令牌
- **THEN** 仓库 MUST 通过令牌哈希查找活动会话并拒绝被撤销的会话。

#### Scenario: Session revocation is persisted
- **WHEN** 一个 user 注销
- **THEN** 仓库 MUST 标记认证会话已撤销，并阻止该令牌的未来验证。
