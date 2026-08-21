## Why

AIOps 工作区可以读取一个 Alertmanager 兼容的 feed 并查询 CLS，但它没有可重复的一组相关现实世界信号来演示从警报到诊断的调查。操作员需要一个本地的 Alertmanager 源、一个真实的外部 Prometheus 读取源，以及故意植入的 Java 电商量化服务证据，以诚实的方式测试完整路径。

## 什么更改

- 添加由 Docker 管理的本地 Alertmanager 配置和一个独立的发布器，通过其 v2 API 发布真实的活跃量化服务警报。
- 读取并聚合配置的 Alertmanager v2 和 Prometheus v1 活跃警报源，保留源上下文并安全地报告源故障。
- 用与本地警报相关的安全、结构化的 Java 电子商务量化服务事件日志替换通用的 CLS 种子内容。
- 添加显式的 SOP 固件上传工作流和文档，以便 user 可以播种一个拥有的知识文档，对其进行索引，并针对真实的 CLS 数据执行警报驱动的诊断。
- 保持所有固件生成的显式性：应用启动和普通前端使用不会伪造警报、日志或文档。

## 能力

### 新功能
- `ecommerce-aiops-fixtures`: 用于关联电子商务量化服务事件演示的显式、真实集成测试工具。

### 修改的功能
- `active-alert-subscription-entry`: 支持配置的 Prometheus v1 和 Alertmanager v2 告警源作为单一的身份验证主动告警数据流。
- `cls-log-generation`: 生成与已记录的警报和标准操作程序相关的结构化 Java 电子商务量化服务日志。
- `aiops-diagnosis-tasks`: 在执行现有的以 SOP 优先的诊断工作流时，保留选定的警报源上下文。

## 影响

影响的区域包括`infra/compose.yaml`、跟踪项目配置、后端活动警报边界和测试、CLS种子脚本、显式的本地演示脚本、AIOps文档，以及现有的前端警报列表契约。本地Alertmanager镜像为新增的Docker服务；CLS仍为腾讯云，外部Prometheus端点为只读。
