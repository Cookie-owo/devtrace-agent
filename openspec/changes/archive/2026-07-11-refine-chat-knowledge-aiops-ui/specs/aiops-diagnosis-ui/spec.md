## ADDED Requirements

### Requirement: Professional Chinese AIOps console presentation
AIOps 工作区 SHALL 使用专业的中文 AI 运维诊断控制台布局，突出任务输入、实时诊断、证据链、最终报告和历史任务，并保持与 ChatGPT 网页式对话工作台一致的克制视觉语言。

#### Scenario: Operator opens the diagnosis workspace
- **WHEN** 已认证的 operator 打开 `/aiops`
- **THEN** 前端 MUST 显示中文的诊断输入区、实时诊断时间线、证据/报告区和历史/告警入口，并以清晰状态标签区分等待中、执行中、成功和失败。

#### Scenario: Diagnostic task is running
- **WHEN** AIOps 诊断任务正在等待、规划、执行、重规划或生成报告
- **THEN** 前端 MUST 在主工作区显示可见的运行状态，而不是只依赖按钮禁用或空白区域表达进度。

#### Scenario: Operator reviews evidence and report
- **WHEN** 一个诊断任务包含证据链、工具调用、引用或最终报告
- **THEN** 前端 MUST 将证据和报告放在可扫描的中文区域中展示，并保留来源、时间和状态信息。

#### Scenario: Responsive diagnosis workspace
- **WHEN** AIOps 工作区在窄视口中显示
- **THEN** 输入、时间线、证据、报告和历史区域 MUST 重新排列为单列或可读的纵向结构，MUST NOT 出现横向页面溢出。
