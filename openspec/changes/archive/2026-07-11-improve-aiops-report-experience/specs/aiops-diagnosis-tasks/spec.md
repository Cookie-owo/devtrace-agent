## ADDED Requirements

### Requirement: Structured Chinese alert analysis report
Report 节点 SHALL 基于诊断输入、告警上下文、SOP、执行计划和真实工具证据生成纯 Markdown 中文告警分析报告，并按照活跃告警清单、逐告警根因分析、处理方案执行、整体结论和风险评估的顺序组织内容。

#### Scenario: Evidence supports one or more active alerts
- **WHEN** Report 节点收到一个或多个真实活跃告警及对应工具证据
- **THEN** 最终报告 MUST 包含告警清单表格，并为每个告警分别展示详情、症状、日志证据、根因结论、排查步骤、处理建议和预期效果

#### Scenario: Evidence is missing or a tool fails
- **WHEN** 某个字段、SOP、日志证据或工具结果缺失或失败
- **THEN** 报告 MUST 在对应章节明确写出“未获取”“证据不足”或失败原因，MUST NOT 编造告警、日志、根因或执行结果

#### Scenario: Report model invocation fails
- **WHEN** LLM 报告生成调用失败、返回空内容或返回非 Markdown 结构
- **THEN** Report 节点 MUST 生成并持久化结构化中文 Markdown 回退报告，并如实保留已有证据和失败状态

#### Scenario: Report output remains plain Markdown
- **WHEN** Report 节点完成报告生成
- **THEN** 持久化内容和 SSE `report` 事件 MUST 包含纯 Markdown 文本，MUST NOT 包含 JSON 报告对象或包裹全文的代码围栏
