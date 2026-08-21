## ADDED Requirements

### Requirement: Ten active Java e-commerce alerts
Alertmanager 辅助脚本 SHALL 发布与共享 Java 电商场景目录对应的 10 条活动告警。

#### Scenario: Alert batch is published
- **WHEN** 执行告警发布脚本
- **THEN** 请求 MUST 包含 10 条不同 alertname/service 的活动告警，每条 annotations MUST 指向匹配的 incident、trace ID 和 SOP

#### Scenario: Alerts are explicitly test scoped
- **WHEN** AIOps 读取这些告警
- **THEN** 每条告警 MUST 带有 `environment=test` 和 `fixture=java-ecommerce`，不得冒充生产告警
