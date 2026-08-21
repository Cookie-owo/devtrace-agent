## Why

当前的 `/health` 端点执行一个 Milvus 依赖调用，而实际的依赖检查位于非契约性的 `/readiness` 路由下，并且省略了 SQLite。这使得当依赖不可用时，容器编排和本地诊断变得模糊。

## 哪些更改

- 使 `/health` 成为一个严格的存活状态端点，不与 SQLite、Milvus、Qwen 或 MCP 进行通信即可返回。
- 用 `/ready` 替换公共的 readiness 路由，同时检查 SQLite、Milvus、Qwen 和本地的 MCP 服务器，并报告每个依赖项的安全诊断结果。
- 添加一个未经过身份验证的 `/config/check` 端点，用于报告配置有效性及依赖连接性，而不会暴露秘密。
- 更新共享的 API 合同、前端运行时状态使用情况以及自动化测试，以使用更正后的路由语义。

## 能力

### 新功能

无。

### 修改的功能

- `runtime-readiness-checks`：将活性、readiness 和安全配置诊断分离到稳定的 API 合约下。

## 影响

- 影响FastAPI health 路由、运行时配置加载、SQLAlchemy readiness 探测、Qwen 和 MCP 提供商检查、前端运行时状态、API 合同，以及后端/前端测试。
