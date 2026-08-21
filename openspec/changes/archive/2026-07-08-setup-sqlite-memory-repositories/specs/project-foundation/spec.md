## MODIFIED Requirements

### Requirement: Foundation verification commands
仓库 SHALL 为 OpenSpec、后端和前端基础检查提供可执行的验证路径，包括后端数据库迁移和仓库测试。

#### Scenario: OpenSpec validates the change
- **WHEN** `openspec validate --all` 会运行
- **THEN** 对 OpenSpec 配置、活动更改和规范 MUST 进行验证，成功通过。

#### Scenario: Backend checks pass
- **WHEN** 后端 lint、类型、迁移和测试命令是从 `apps/backend` 运行的  
- **THEN** 它们在 scaffold 上成功完成。

#### Scenario: Frontend checks pass
- **WHEN** 前端类型、测试和构建命令从 `apps/frontend` 运行  
- **THEN** 它们在模板上成功完成 MUST。
