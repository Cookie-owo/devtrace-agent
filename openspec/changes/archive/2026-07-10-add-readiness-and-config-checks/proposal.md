## Why

操作员需要在依赖聊天、索引或AIOps之前，获得关于本地应用程序是否可以使用Milvus、Qwen和CLS MCP服务器的可靠答案。现有的部分health路由不会汇总该readiness或公开类型的应用程序状态。

## 什么更改

- 添加一个类型化、安全的 readiness 端点，用于聚合 Milvus、LLM 和 MCP 检查。
- 为常规 UI 连接保留轻量级 health 行为，同时将完整的提供者检查设为显式。
- 添加共享的 readiness 合同和前端状态处理，以便工作区标题反映实时后端可访问性，而不是静态文本。

## 功能

### 新功能
- `runtime-readiness-checks`: 带有类型化前端可访问状态的密钥安全聚合 health 和提供者 readiness 检查。

### 修改的功能
- 无。

## 影响

- 影响后端 API 路由和测试，共享 API 合同，前端 health 传输/布局状态，以及文档。
