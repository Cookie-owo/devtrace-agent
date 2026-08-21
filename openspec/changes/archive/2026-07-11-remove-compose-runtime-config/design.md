## 上下文

`infra/compose.yaml` 已只编排 etcd、MinIO、Milvus、Attu 和 Alertmanager。后端、Vue 前端和官方 CLS MCP Server 由本机启动器直接启动，并使用 `config/project.json`。但仓库仍保留 `config/project.compose.json`、`create_compose_app()` 与 `infra/app.Dockerfile`，它们来自已废弃的整套应用容器化路径，当前没有 Compose 服务或启动器使用它们。

## 目标与非目标

**目标：**

- 删除无消费者的 Compose 应用运行时配置、镜像和应用工厂。
- 使应用和工具的受跟踪配置唯一为 `config/project.json`。
- 保持 Compose 仅管理五个既有基础设施服务，并使文档、测试和 OpenSpec 规格反映这一边界。
- 在项目共享后，使运维指南的接收方替换清单精确且最小化，只标识必须由接收方提供的六个配置字段。

**非目标：**

- 不新增应用容器化、兼容别名、回退配置或本地环境变量读取。
- 不改变五个基础设施服务、应用 API、数据库迁移或提供方凭据值。
- 不将已归档的 OpenSpec 历史记录改写为当前状态。
- 不把 MCP、Milvus、MinIO、Prometheus/Alertmanager 来源、应用地址、Docker 字段或演示账户设置添加为接收方需替换的配置项。

## 决策

### 完整删除废弃运行时路径

删除 `config/project.compose.json`、`infra/app.Dockerfile` 及仅使用该配置的 `create_compose_app()`。不保留包装函数、空 Dockerfile 或配置副本，因为这些兼容物会继续暗示存在可用的 Compose 应用运行时，并可能再次产生配置漂移。

考虑过保留 `project.compose.json` 作为指向 `project.json` 的副本，但该方案仍会形成两份受跟踪配置，并使未来调用方无法暴露；因此采用完整删除。若需要恢复应用容器化，必须由新的 OpenSpec 变更重新定义镜像、配置和启动边界。

### 以单一项目配置作为应用运行时来源

所有保留的应用、MCP 与运维配置引用均指向 `config/project.json`。Compose 本身不消费应用配置，因此不再需要 Compose 配置变体；基础设施镜像和 Alertmanager 仍由各自现有的 Compose 或基础设施文件定义。

### 共享后的最小替换配置清单

`docs/operations-and-monitoring.md` 面向项目接收方的“需要替换”清单只能列出以下 `config/project.json` 字段：`llm.apiKey`、`clsMcpServer.secretId`、`clsMcpServer.secretKey`、`clsLogUpload.region`、`clsLogUpload.logsetId` 和 `clsLogUpload.topicId`。这些字段分别覆盖接收方自备的 LLM 密钥、CLS MCP 凭据和实际 CLS 日志上传目标。

MCP 服务来源、Milvus 或 MinIO 来源、Prometheus/Alertmanager 来源、应用访问地址、Docker 相关字段和演示账户设置可以在指南中作为既有运行说明出现，但不得被列入、暗示为或测试为接收方需要替换的配置项。这样可避免把共享环境中无需接收方修改的部署细节误导为前置配置。

### 通过边界测试和检索防止死引用回归

测试将断言废弃文件不存在、工厂函数不再存在，并确保运维文档只列出 `config/project.json`，且“需要替换”清单精确包含六个允许字段。最终检索排除 Git 元数据与历史归档，验证当前生产代码、测试和启动文档不再引用三个已删除标识。

## 风险与权衡

- [仍有未发现的使用方依赖旧文件或工厂函数] → 在删除前更新受影响测试，并对当前仓库执行精确检索。
- [开发者误以为 Compose 可启动应用] → 在 README、基础设施说明、运维指南和 OpenSpec 中明确 Compose 仅负责五个基础设施服务。
- [未来需要完整容器化应用] → 通过独立变更重新设计，而不是恢复未验证的旧入口。

## 迁移计划

1. 先增加或调整 Compose 基础设施测试，定义不存在 Compose 应用资产的运行时边界。
2. 删除旧配置、Dockerfile 和 `create_compose_app()`，随后运行受影响的运行时测试。
3. 在同一文档阶段内，增加或调整文档测试，并更新开发文档、运维指南和主 OpenSpec 规格：删除 `project.compose.json` 与应用镜像表述，并将共享后替换清单限制为六个允许字段。
4. 执行死引用检索、`openspec validate --all` 和后端质量检查。

回滚方式是在需要时恢复同一变更删除的三个资产及其调用方；这不影响现有 Compose 基础设施卷或服务定义。

## 开放问题

无。当前运行时边界和删除范围已由现有 Compose 拓扑确定。
