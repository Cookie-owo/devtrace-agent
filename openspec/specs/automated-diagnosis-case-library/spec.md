# Automated Diagnosis Case Library Specification

## Purpose

定义自动的 owner 作用域的持久化、索引和已完成的 AIOps 诊断案例的展示。

## Requirements

### Requirement: Automatic structured diagnosis case persistence
后端为每个成功完成的 AIOps 诊断（带有最终报告）创建一个 owner 范围的结构化诊断案例，并且当 SHALL 时不会为失败的诊断创建案例。

#### Scenario: Diagnostic succeeds
- **WHEN** 报告节点会保留成功的最终报告
- **THEN** 后端 MUST 会保留与任务、报告、证据 ID、生成的知识文档和索引任务相关联的案例，包括警报名称、服务、关键词、根本原因字段、纠正措施字段和摘要。

#### Scenario: Diagnostic fails
- **WHEN** 诊断在成功最终报告之前失败
- **THEN** 后端 MUST NOT 为该失败任务创建诊断案例、知识文档、索引任务或向量数据

#### Scenario: Successful task is processed more than once
- **WHEN** 案例持久化重新进入相同的 owner 和任务
- **THEN** 后端 MUST 返回现有的案例和 MUST NOT 创建重复的案例文档或索引任务。

### Requirement: Case knowledge indexing and retrieval traceability
后端 SHALL 通过现有的文档流程对自动创建的用例进行索引，并保留对结构化用例字段的可追溯性。

#### Scenario: Case is indexed
- **WHEN** 会自动生成一个用例
- **THEN** 后端 MUST 使用包含 owner、tenant 和 `diagnostic-case` 分类元数据的文档，异步创建并安排标准索引任务。

#### Scenario: Indexing fails
- **WHEN** 自动用例索引失败
- **THEN** 结构化用例及其关联的文档/索引任务 MUST 在标准索引失败状态下仍可通过 owner 查询。

### Requirement: Owner-scoped diagnosis case library
系统 SHALL 提供经过身份验证的案例列表和 AIOps 展示，该展示仅显示当前 user 的结构化诊断案例。

#### Scenario: Owner lists cases
- **WHEN** 已认证的 user 请求或打开诊断病例库
- **THEN** 系统 MUST 返回并显示该 user 的病例，按最新优先排序，并包含其任务/报告/文档链接和结构化摘要字段。

#### Scenario: Other user attempts case access
- **WHEN** 一个 user 请求属于另一个 user 的案例
- **THEN** 后端 MUST 返回统一的授权错误，不暴露案例字段或关联的工件。
