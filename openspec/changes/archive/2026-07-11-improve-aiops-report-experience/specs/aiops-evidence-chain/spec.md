## ADDED Requirements

### Requirement: Evidence sidebar avoids duplicate report body
右侧证据链 SHALL 聚焦最终报告的来源关系、真实证据、工具调用和诊断案例，并 MUST NOT 与中间主区域重复渲染完整报告正文。

#### Scenario: Persisted report has linked evidence
- **WHEN** 选中诊断的报告关联一个或多个证据记录
- **THEN** 右侧 MUST 展示报告标题、生成时间和关联证据标识，同时将完整报告正文保留在中间主区域

#### Scenario: No report has been persisted
- **WHEN** 选中任务尚未生成报告
- **THEN** 右侧 MUST 明确显示报告尚未生成，并继续展示已经存在的证据和工具调用
