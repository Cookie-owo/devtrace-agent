## ADDED Requirements

### Requirement: Alert provenance is retained by a diagnostic task
后端 SHALL 保留从活动警报源中选择的警报的归一化源身份和原始上下文，这些警报来自持久化的诊断输入、证据链、流式处理生命周期和最终报告输入。

#### Scenario: Operator diagnoses an alert from a configured source
- **WHEN** 已认证的操作员从标准化的活动警报中启动 AIOps 诊断
- **THEN** 持久化的诊断输入和初始警报证据 MUST 包括所选的源身份和原始提供者上下文，以及标准化的警报字段。
