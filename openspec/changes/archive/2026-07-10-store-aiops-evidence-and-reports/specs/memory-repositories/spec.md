## ADDED Requirements

### Requirement: Diagnostic evidence-chain repository boundary
后端 SHALL 暴露存储库记录以及 owner 范围内的诊断步骤、证据、报告证据链接、历史查询和完整证据链查询，而不会泄露 SQLAlchemy 详细信息。

#### Scenario: Repository writes validate task ownership
- **WHEN** 业务代码存储一个步骤、证据记录或报告证据链接
- **THEN** 仓库 MUST 验证诊断任务是否属于提供的 owner user ID。

#### Scenario: Repository reads complete chain within owner scope
- **WHEN** 业务代码请求一个带有 owner user ID 和任务 ID 的诊断证据链
- **THEN** 仓库 MUST 仅返回属于该 owner 和任务的记录
