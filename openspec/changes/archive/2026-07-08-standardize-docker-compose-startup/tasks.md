## 1. 合同和验证测试

- [x] 1.1 添加验证 Docker Compose 服务、共享应用镜像使用情况、端口、依赖项和排除项的基础架构测试。
- [x] 1.2 添加验证 `infra/app.Dockerfile` 包含后端、前端构建和官方 CLS MCP 运行时的基础架构测试。
- [x] 1.3 添加验证 Compose 启动和 CLS 占位符的文档和环境示例的基础架构测试。

## 2. 组合与图像实现

- [x] 2.1 为统一的应用镜像添加 `infra/app.Dockerfile`。
- [x] 2.2 添加带有后端、前端、cls-mcp-server、Milvus、etcd、MinIO 和 Attu 服务的 `infra/compose.yaml`。
- [x] 2.3 添加本地 Docker Compose 环境示例和被忽略的本地 CLS 凭据配置。

## 3. 文档

- [x] 3.1 使用 Compose 启动、端点、凭证和排除项更新 `infra/README.md`。
- [x] 3.2 更新根 README，使其完整堆栈启动指向 Docker Compose。

## 4. 验证和归档

- [x] 4.1 运行基础设施测试，后端/前端/合约检查，当可用时进行Docker Compose配置验证和OpenSpec验证。
- [x] 4.2 同步规范并归档更改。
- [x] 4.3 提交跟踪的更改并通过`main`到SSH端口443推送。
