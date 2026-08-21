## ADDED Requirements

### Requirement: Explicit correlated e-commerce AIOps fixtures
仓库 SHALL 提供了显式的命令，在真实的腾讯云 CLS 中生成一个安全的 Java 电商量化服务日志事件，向本地 Alertmanager 发布匹配的主动警报，并通过运行中的后端 API 上传/索引一个匹配的 owner 范围的 SOP。这些命令 MUST 不会在应用程序启动时自动运行。

#### Scenario: Developer seeds the demonstration incident
- **WHEN** 开发人员在配置的实时服务上运行记录的fixture命令
- **THEN** CLS 接收结构化的quant-service事件日志，本地 Alertmanager 暴露匹配的活动警报，owner 范围内的 SOP 在索引后可用于知识检索。

#### Scenario: Developer runs the alert-driven diagnosis
- **WHEN** 在 SOP 之后选择记录的活动警报进行诊断，并且日志可用
- **THEN** 的 AIOps 工作流 MUST 保留警报来源，检索其有界实际 CLS 查询之前的匹配 SOP，并持久化生成的工具证据和报告。

#### Scenario: Application starts normally
- **WHEN** 后端应用程序在没有开发人员运行fixture命令的情况下启动
- **THEN** 它 MUST NOT 发布警报，上传 CLS 日志，创建 user，或上传知识文档。
