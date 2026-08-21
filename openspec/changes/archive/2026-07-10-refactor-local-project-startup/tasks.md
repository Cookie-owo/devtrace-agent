## 1. 仅基础设施的 Compose

- [x] 1.1 添加需要仅基础设施 Compose 服务的失败测试，并更新启动器依赖命令。
- [x] 1.2 从 Compose 中移除 backend、frontend 和 CLS MCP 服务，同时保留 Milvus 依赖项、Attu 和 Alertmanager。
- [x] 1.3 更新 macOS/Linux 和 Windows 启动器，在主机本地 MCP、backend 和 frontend 进程之前启动完整的容器基础设施集。

## 2. 文档

- [x] 2.1 为根特性库存、平台安装指南和日志/警报教程添加失败的文档测试。
- [x] 2.2 添加完整的中文 macOS、Linux 和 Windows 安装指南。
- [x] 2.3 添加真实的 CLS 日志和 Alertmanager 警报教程，并使用特性库存和新的启动边界更新 root/infra README。

## 3. 浏览器接受和验证

- [x] 3.1 使用更新的启动器启动基础设施 Compose 并直接托管服务，然后验证 readiness。
- [x] 3.2 使用实时前端验证已认证的聊天、知识文档、活动警报、AIOps 证据/报告、历史记录和导航工作流。
- [x] 3.3 运行后端、前端、Compose、OpenSpec 和文档验证；通过 SSH 端口 443 归档、提交并推送。
