## MODIFIED Requirements

### Requirement: Diagnostic SSE lifecycle
AIOps 诊断 SHALL 由持久化后台任务执行，并将计划、步骤、工具、重规划、报告、完成和错误事件持久化后通过 SSE 订阅返回。

#### Scenario: Diagnostic stream disconnects
- **WHEN** 用户在诊断期间关闭或刷新页面
- **THEN** 诊断 MUST 继续执行，重新打开任务 MUST 能恢复事件和最终证据链。
