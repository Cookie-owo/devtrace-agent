## ADDED Requirements

### Requirement: Generic tool call audit repository
后端 SHALL 为创建、完成和查询 tenant 范围的工具调用审计记录提供了一个仓库协议，而不会向业务服务暴露 SQLite 或 SQLAlchemy 的详细信息。

#### Scenario: Chat tool audit can be updated by lifecycle id
- **WHEN** 业务代码创建了一个聊天工具审计记录，之后收到了同一工具调用ID的终端事件
- **THEN** 它会MUST 完成现有的owner作用域的审计记录，而不是创建重复的记录。

#### Scenario: Diagnostic tool audit can use the common boundary
- **WHEN** 一个未来的 AIOps 诊断流程记录工具调用
- **THEN** 它应该能够通过相同的通用仓库协议，使用其诊断任务 ID 创建和查询该记录。
