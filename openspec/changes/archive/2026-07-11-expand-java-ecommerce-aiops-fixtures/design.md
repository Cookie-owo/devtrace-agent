## Context

现有 fixture 只描述 `quant-risk-service` 的一个告警。新增数据需要真实上传到 CLS、本地 Alertmanager 和 owner 范围知识库，因此三类脚本必须共享同一份场景目录，避免各自维护后发生错配。

## Goals / Non-Goals

**Goals:**

- 定义 10 个不同 Java 电商微服务故障，每个具有唯一 trace ID。
- 每个场景生成一条关键错误日志、一条活动告警和一份可执行 SOP。
- 让三类数据通过稳定标识可由 AIOps 追溯。

**Non-Goals:**

- 不伪造生产系统或自动触发诊断。
- 不替换现有量化 fixture，不在应用启动时自动上传。

## Decisions

- 在 `super_ai.aiops.fixtures` 定义不可变 `JavaEcommerceIncident` 目录，包含 service、alert、SOP、trace、症状、阈值、根因、验证与恢复步骤。
- 日志、Alertmanager payload 和 SOP 文档都从同一目录生成；`incident_id`、`trace_id`、`service`、`alertname`、`sop` 必须一一对应。
- 10 个 trace ID 均不同且固定，便于 CLS 精确查询和测试复现。
- 现有三个脚本扩展为默认处理新目录，量化 fixture 函数继续保留用于兼容测试。

## Risks / Trade-offs

- [一次发布 10 条活动告警增加界面噪声] → 全部使用 `environment=test` 和明确的 `fixture=java-ecommerce` 标签。
- [SOP 内容与场景漂移] → SOP 文本从同一场景目录渲染，并用完整关联测试约束。
- [重复执行产生重复文档] → 上传使用 overwrite，稳定文件名确保幂等替换。
