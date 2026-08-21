## Why

项目已具有经过身份验证的聊天会话存储、共享的 SSE 合同、Qwen 提供商配置，以及一个 tenant 范围的知识检索工具，但聊天请求仍然缺乏统一的流式 RAG 执行路径。此更改将聊天转变为单一的流式产品功能，其中模型可以决定是否调用工具，每个发出的事件和持久化消息都遵循共享合同。

## 什么更改

- 添加一个基于 LangChain `create_agent` 构建的后端流式聊天 Agent 功能，配置的 Qwen `ChatOpenAI` 提供商以及 LangChain 工具。
- 将产品聊天通过一个 SSE 端点进行路由，并移除单独的快速 /non-streaming 聊天行为。
- 为令牌差异、工具调用开始/结束/失败、知识引用、完成和错误发出共享的 SSE 事件。
- 将 user 消息、最终助理消息、工具调用标识符、引用元数据和聊天历史记录通过仓库边界持久化到 SQLite。
- 让模型决定是否调用知识检索工具；检索不得作为固定预步骤运行。
- 更新前端聊天状态和 UI 以使用统一的流式端点，同时继续将后端 SQLite 作为主要会话存储。

## 功能

### 新功能
- `stream-rag-chat`: Agent 驱动的流式聊天编排，SSE 发射，工具集成和消息持久化。

### 修改的功能
- `api-and-sse-contracts`: 添加流式聊天请求/响应契约，明确工具调用开始/结束事件语义，并移除快速/非流式聊天作为产品模式。
- `chat-sessions`: 要求流式聊天在 SQLite 中保留用户和助手消息以及引用/工具元数据。
- `knowledge-retrieval-tool`: 要求检索工具作为 LangChain 工具暴露，供流式聊天代理使用。
- `qwen-openai-provider`：要求提供者抽象必须提供一个适用于`create_agent`的LangChain聊天模型。

## 影响

- 后端：FastAPI 聊天流式处理端点，LangChain Agent 服务，SSE 序列化，提供者/工具连接，聊天仓库使用情况，测试。
- 前端：聊天客户端流式处理解析器，聊天状态操作，聊天面板交互，测试。
- 共享契约：TypeScript DTO，SSE 事件契约细化，OpenAPI 路径定义和测试。
- 依赖项：使用现有的 `langchain-openai` 提供者，并可能添加 LangChain 包，如果 `uv` 元数据中缺少这些包，则根据提供者/工具需求已隐含。
