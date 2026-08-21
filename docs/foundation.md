# 项目基础

基础架构仅建立仓库结构和验证入口点。产品行为，如身份验证、聊天、知识库、AIOps 工作流、MCP 集成、向量存储和 LLM 提供商连接，必须通过后续的针对性 OpenSpec 变更来实现。

## 边界

- 后端代码通过`super_ai`从`apps/backend/src`导入。
- 前端代码从`apps/frontend`中使用了Vue 3、Vite 和 TypeScript。
- 共享的前端合约类型位于`packages/api-contracts`。
- 项目配置位于 JSON 文件中，这些文件受跟踪；本地 `.env` 文件不属于工作流程。
- 不支持历史实现目录。
