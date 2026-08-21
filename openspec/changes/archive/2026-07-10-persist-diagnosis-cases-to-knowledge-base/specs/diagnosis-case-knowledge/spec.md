## ADDED Requirements

### Requirement: Save completed diagnostic as user-scoped knowledge case
系统 SHALL 允许诊断 owner 将完成的有证据支持的报告作为知识文档显式保存到该 owner 的知识库中。

#### Scenario: Owner saves a completed report
- **WHEN** 一个任务 owner 请求保存一份已完成的诊断报告
- **THEN** 后端 MUST 创建一个包含报告和相关证据摘要的文档，并带有诊断/报告来源元数据，并安排其标准索引任务。

#### Scenario: Non-owner requests a diagnostic case save
- **WHEN** 一个 user 请求保存另一个 user 的诊断
- **THEN** 后端 MUST 返回统一的授权错误，MUST NOT 创建文档或任务。

#### Scenario: Report is saved more than once
- **WHEN** 同一份报告已为 owner 保存
- **THEN** 后端 MUST 应返回统一的业务冲突，而不是静默创建重复的知识案例。

### Requirement: AIOps report retention action
AIOps 前端 SHALL 为选定的已完成报告显示显式的保存到知识库命令，并呈现返回的文档/索引状态或标准化的失败信息。

#### Scenario: Operator saves the selected report
- **WHEN** 选定的诊断报告是完整的，操作员调用保存命令  
- **THEN** 前端 MUST 调用类型化的保存端点并显示已保存的病例文档及其索引状态。
