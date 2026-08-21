## Why

当前脚本只提供单一量化服务故障，无法覆盖 Java 电商微服务常见依赖、资源和消息链路问题，也不足以验证告警、CLS 日志与知识库 SOP 的关联诊断。

## What Changes

- 新增 10 套有因果依据的 Java 电商微服务故障场景。
- 每套场景各生成一份结构化 CLS 关键日志、一条 Alertmanager 告警和一份独立故障处理 SOP。
- 使用一致的 `incident_id`、`service`、`alertname` 与 `sop` 标识串联三类数据。
- 扩展日志上传、告警发布和 SOP 上传索引脚本，使其一次处理全部 10 套场景，并保留现有量化 fixture。
- 增加数据完整性、数量、关联性、安全性和 SOP 内容测试，更新使用文档。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `ecommerce-aiops-fixtures`: 从单场景扩展为 10 套相互独立且三类证据关联的 Java 电商微服务故障。
- `cls-log-generation`: 日志脚本支持上传 10 条不同故障场景的真实 CLS 结构化日志。
- `active-alert-subscription-entry`: 本地 Alertmanager fixture 支持同时发布 10 条可诊断活动告警。

## Impact

影响后端 fixture 定义、三个辅助脚本、AIOps 文档、SOP Markdown 资产及测试；不引入 mock 后端，不改变生产 API。
