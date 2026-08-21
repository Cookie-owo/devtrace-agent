## 1. 就绪契约和探针

- [x] 1.1 为无依赖的 `/health`、聚合 `/ready`、安全降级结果以及 `/config/check` 保留添加失败的后端/合约测试。
- [x] 1.2 添加带类型的 SQLite、依赖项和配置探测帮助程序，不记录或返回密钥。
- [x] 1.3 将 `/readiness` 替换为 `/ready`，实现 `/config/check`，并更新共享的 OpenAPI 合约。

## 2. 客户端集成和验证

- [x] 2.1 更新前端运行时 health type/client/tests 以进行严格的轻量级存活检查。
- [x] 2.2 运行后端检查、前端类型检查/测试/构建、API-contract 检查以及 OpenSpec 验证。
- [x] 2.3 重启本地应用程序，并将 `/health`、`/ready` 和 `/config/check` 与真实的 SQLite、Milvus、Qwen 和 MCP 服务进行验证。
- [x] 2.4 同步规范，归档 OpenSpec 的更改，提交并推送到 `main` 通过 SSH 端口 443。
