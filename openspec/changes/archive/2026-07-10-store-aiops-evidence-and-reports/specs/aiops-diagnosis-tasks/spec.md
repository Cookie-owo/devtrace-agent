## ADDED Requirements

### Requirement: Diagnostic workflow writes evidence-chain records
LangGraph Planner、Executor、Replanner 和 Report 节点 SHALL 通过诊断证据链存储库边界持续保留其计划、执行、证据和报告的来源信息。

#### Scenario: Workflow persists node artifacts
- **WHEN** 诊断在图节点中进行
- **THEN** 节点 MUST 存储有序步骤记录以及最终报告发出前生成的任何证据。
