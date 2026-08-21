## ADDED Requirements

### Requirement: User chat configuration repository
内存层 SHALL 为读取和更新聊天组装配置提供一个 user 范围的 Repository，而不会将 SQLite 模型或 SQL 细节泄露给业务服务。

#### Scenario: Repository scopes reads and writes by user
- **WHEN** 服务读取或更新聊天配置
- **THEN** 仓库 MUST 需要 owner user id 并仅返回或修改该 user 的行。

#### Scenario: 迁移创建配置存储
- **WHEN** 初始化或升级内存模式
- **THEN** Alembic MUST 使用唯一的 owner 边界和 JSON 安全的技能选择持久化创建 user 聊天配置存储。
