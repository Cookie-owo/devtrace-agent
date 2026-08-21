## MODIFIED Requirements

### Requirement: Save completed diagnostic as user-scoped knowledge case
系统 SHALL 会将每份成功完成的有证据支持的诊断报告自动保存为结构化案例和可索引的知识文档，存入诊断 owner 的知识库中。

#### Scenario: Successful report becomes a case
- **WHEN** 一个 owner 任务在具有持久化最终报告时达到 `succeeded`
- **THEN** 后端 MUST 会自动创建一个关联的结构化案例、基于报告的知识文档以及带有诊断/报告/证据来源元数据的计划标准索引任务。

#### Scenario: Non-owner cannot access a case
- **WHEN** 一个 user 请求由另一个 owner 创建的诊断案例
- **THEN** 后端 MUST 返回统一的授权错误，并且 MUST NOT 暴露该案例、文档、报告或任务。

#### Scenario: Case persistence repeats
- **WHEN** 相同的成功任务被再次处理  
- **THEN** 后端 MUST 保留现有的 owner 范围内的案例，而不是创建重复的文档或任务。
