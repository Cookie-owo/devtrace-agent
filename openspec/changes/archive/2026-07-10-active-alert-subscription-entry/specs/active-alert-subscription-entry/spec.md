## ADDED Requirements

### Requirement: ### 需求：真实活动警报查询边界
后端 SHALL 从配置的外部 Alertmanager 兼容的警报 API 中读取活动警报，而不使用运行时模拟配置文件、伪造的回退警报或模块导入网络调用。

#### Scenario: 配置的提供者返回活动警报
- **WHEN** 一个经过身份验证的 user 请求当前警报，配置的提供者返回有效的 Alerts API 响应
- **THEN** 后端 MUST 返回规范化后的活动警报，包括警报名称、服务、严重性、状态、开始时间、摘要、标签、注释以及原始警报上下文。

#### Scenario: 无法查询提供者
- **WHEN** 配置的端点超时，返回失败响应，或返回无效响应正文
- **THEN** 后端 MUST 返回一个标准化的服务不可用错误，不会泄露凭据或生成警报数据。

### Requirement: Authenticated active-alert subscription entry
前端 SHALL 会向已认证的操作员显示当前的活动外部警报，并提供对现有 AIOps 诊断流程的直接入口。

#### Scenario: Operator views active alerts
- **WHEN** 已认证的操作员打开 AIOps 工作区
- **THEN** 前端 MUST 请求活动警报 API 并显示每个返回的警报的名称、服务、严重程度、状态、开始时间和摘要。

#### Scenario: Operator starts diagnosis from an alert
- **WHEN** 一个操作员选择一个当前警报进行诊断  
- **THEN** 前端 MUST 使用该警报返回的上下文和一个标识所选警报的查询来创建并流式传输 AIOps 诊断。

#### Scenario: Alert request fails
- **WHEN** 活动警报 API 返回一个标准化的错误
- **THEN** 前端 MUST 以重试操作显示错误，并且 MUST NOT 将过时或模拟的警报显示为实时结果。

### Requirement: Responsive alert triage presentation
AIOps 活动警报条目 SHALL 在桌面和窄视口上应保持与诊断工作区的可操作性。

#### Scenario: Operator uses a narrow viewport
- **WHEN** 在窄视口上显示活动警报列表
- **THEN** 其警报字段、刷新控制和诊断操作 MUST 重新排列，而不会出现水平页面溢出。
