## ADDED Requirements

### Requirement: Ten correlated Java e-commerce incident fixtures
系统 SHALL 提供 10 套不同的 Java 电商微服务后端故障 fixture，每套包含一条关键日志、一条告警和一份处理 SOP。

#### Scenario: Fixture catalog is generated
- **WHEN** 构建 Java 电商 fixture 目录
- **THEN** 目录 MUST 恰好包含 10 个不同 service/alert 故障场景和 10 个不同 trace ID

#### Scenario: Evidence types correlate
- **WHEN** 为任一场景生成日志、告警和 SOP
- **THEN** 三类数据 MUST 具有一致的 `incident_id`、`service`、`alertname` 与 `sop` 标识，且日志 trace ID MUST 可用于 CLS 查询

#### Scenario: Scenario has operational rationale
- **WHEN** 检查任一 fixture
- **THEN** 它 MUST 包含可观测症状、触发阈值、合理根因、排查步骤、恢复动作和验证标准
