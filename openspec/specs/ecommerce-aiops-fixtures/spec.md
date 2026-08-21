# ecommerce-aiops-fixtures Specification

## Purpose
TBD - 由归档更改 create-ecommerce-aiops-fixtures 创建。更新归档后的用途。
## Requirements
### Requirement: Explicit correlated e-commerce AIOps fixtures
仓库 SHALL 提供显式的命令，在真实的腾讯云 CLS 中生成一个安全的 Java 电商量化服务日志事件，向本地 Alertmanager 发布匹配的主动警报，并通过运行中的后端 API 上传/索引一个匹配的 owner 范围 SOP。这些命令 MUST 不会在应用程序启动时自动运行。

#### Scenario: Developer seeds the demonstration incident
- **WHEN** 开发人员在配置的实时服务上运行记录的fixture命令
- **THEN** CLS 接收结构化的quant-service事件日志，本地 Alertmanager 暴露匹配的活动警报，owner 范围内的 SOP 在索引后可用于知识检索。

#### Scenario: Developer runs the alert-driven diagnosis
- **WHEN** 在 SOP 之后选择记录的活动警报进行诊断，并且日志可用
- **THEN** 的 AIOps 工作流 MUST 保留警报来源，查询其限定的真实 CLS 之前获取匹配的 SOP，并持久化生成的工具证据和报告。

#### Scenario: Application starts normally
- **WHEN** 后端应用程序在未运行开发人员的fixture命令时启动
- **THEN** 它 MUST NOT 发布警报，上传 CLS 日志，创建 user，或上传知识文档。

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
