# Active Alert Subscription Entry Specification

## Purpose

从真实的外部主动警报中定义经过身份验证的读取路径，将其导入 AIOps 诊断信息，同时保留原始警报上下文，并诚实地展示提供方故障。
## Requirements
### Requirement: ### 需求：真实活动警报查询边界
后端 SHALL 从一个或多个配置的外部 Prometheus v1 或 Alertmanager v2 警报 API 中读取活动警报，而不使用运行时模拟配置文件、伪造的备用警报或模块导入网络调用。每个标准化的警报 MUST 将保留其源标识符和原始提供者上下文。

#### Scenario: 配置的提供者返回活跃警报
- **WHEN** 一个经过身份验证的 user 请求当前警报，并且一个或多个配置的提供者返回有效的 Alerts API 响应
- **THEN** 后端 MUST 返回规范化后的活跃警报，包括警报名称、服务、严重性、状态、开始时间、摘要、标签、注释、来源出处以及原始警报上下文。

#### Scenario: 一个配置的提供者不可用
- **WHEN** 一个配置的端点超时，返回失败响应，或返回无效响应体，而另一个配置的提供者返回有效响应
- **THEN** 后端 MUST 返回有效提供者的标准化警报，而不虚构警报数据或暴露提供者凭据。

#### Scenario: 每个配置的提供者都无法查询
- **WHEN** 每个配置的端点均超时、返回失败响应或返回无效响应正文
- **THEN** 后端 MUST 返回一个标准化的服务不可用错误，该错误不泄露凭据或生成警报数据。

### Requirement: Authenticated active-alert subscription entry
前端 SHALL 会向已认证的操作员显示当前激活的外部警报，并提供直接进入现有 AIOps 诊断流程的入口。

#### Scenario: Operator views active alerts
- **WHEN** 已认证的操作员打开 AIOps 工作区
- **THEN** 前端 MUST 请求活动警报 API 并显示每个返回警报的名称、服务、严重程度、状态、开始时间和摘要。

#### Scenario: Operator starts diagnosis from an alert
- **WHEN** 操作员选择一个当前警报进行诊断
- **THEN** 前端 MUST 使用该警报返回的上下文和一个标识所选警报的查询来创建并流式传输 AIOps 诊断。

#### Scenario: Alert request fails
- **WHEN** 活动警报 API 返回一个标准化的错误
- **THEN** 前端 MUST 以重试操作显示错误，并且 MUST NOT 将过时或模拟的警报显示为实时结果。

### Requirement: Responsive alert triage presentation
AIOps 活动警报条目 SHALL 在桌面和窄视口上应保持与诊断工作区的可操作性。

#### Scenario: Operator uses a narrow viewport
- **WHEN** 在窄视口上显示活动警报列表
- **THEN** 其警报字段、刷新控制和诊断操作 MUST 重新排列，而不会出现水平页面溢出。

### Requirement: Ten active Java e-commerce alerts
Alertmanager 辅助脚本 SHALL 发布与共享 Java 电商场景目录对应的 10 条活动告警。

#### Scenario: Alert batch is published
- **WHEN** 执行告警发布脚本
- **THEN** 请求 MUST 包含 10 条不同 alertname/service 的活动告警，每条 annotations MUST 指向匹配的 incident、trace ID 和 SOP

#### Scenario: Alerts are explicitly test scoped
- **WHEN** AIOps 读取这些告警
- **THEN** 每条告警 MUST 带有 `environment=test` 和 `fixture=java-ecommerce`，不得冒充生产告警
