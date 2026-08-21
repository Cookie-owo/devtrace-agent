## Why

身份验证目前仅能证明调用者的身份，但持久化的业务数据仍类似于全局数据。知识库、向量、聊天历史、工具审计和 AIOps 工件在连接真正的 user 数据之前需要明确的授权和 tenant 边界。

## 什么更改

- 根据经过身份验证的 user ID 添加一个 tenant 范围模型。
- 要求知识库、向量、聊天、消息、诊断、证据、报告、工具审计和 checkpoint 数据必须属于一个 tenant 范围。
- 要求仓库方法接收tenant/user范围以进行作用域内的读写操作。
- 为禁止的跨tenant访问添加统一的授权错误。
- 需要 Milvus chunk 元数据来携带 owner/user/tenant 信息和检索过滤器以应用该作用域。
- 确保前端数据视图仅通过经过身份验证的、有作用域的 API 调用进行填充。
- **BREAKING**: 有作用域数据的记忆库方法签名包括 tenant/user 作用域，而不是全局访问。

## 功能

### 新功能

- `authorization-and-tenant-isolation`: 权限检查，tenant 范围传播，跨tenant拒绝，向量元数据ownership，以及前端作用域数据行为。

### 修改后的功能

- `api-and-sse-contracts`: 添加授权错误合约、403 响应以及作用域保护的 API 语义。
- `memory-repositories`: 添加 owner/tenant 列、作用域仓库签名、作用域查询行为和向量元数据约束。
- `user-authentication`: 要求经过身份验证的端点将用户作用域传播到下游仓库并拒绝未经授权的访问。

## 影响

- 后端 API 身份验证依赖和受保护的端点处理程序。
- SQLAlchemy 模型，Alembic 迁移，仓库协议，以及 SQLite 仓库实现。
- 共享的 TypeScript API 合同和 OpenAPI 合同测试。
- 前端身份验证状态和经过身份验证的数据客户端行为。
- OpenSpec 主要规范和已归档的变更工件。
