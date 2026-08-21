# 后端

后端使用 Python、`uv` 和 src 布局。应用代码位于 `src/super_ai` 下，并通过包名称进行导入：

```python
from super_ai.foundation import get_foundation_info
```

## 命令

```bash
uv sync
uv run ruff check .
uv run pyright
uv run pytest
```

在应用迁移后运行本地 API：

```bash
mkdir -p var
uv run alembic upgrade head
uv run uvicorn super_ai.api:create_app --factory --reload
```

## LLM 提供者

后端在 `src/super_ai/llm` 下使用可替换的 LLM 提供商抽象。
默认提供程序是 `QwenOpenAIProvider`，由 LangChain 的 OpenAI-compatible 支持
`ChatOpenAI`。

跟踪的 Qwen 默认值位于 `config/project.json` 的 `llm` 部分下：

- `baseUrl`: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- `chatModel`: `qwen3.7-max`
- `embeddingModel`: `text-embedding-v4`
- `embeddingDimensions`: `1024`
- `rerankModel`: `qwen3-vl-rerank`
- `temperature`: `0.2`
- `timeoutSeconds`: `30`
- `maxRetries`: `2`
- `apiKey`: 私有仓库开发密钥

后端不会读取本地环境变量中的提供者设置。

就绪检查返回提供者、模型、端点、延迟和安全错误字符串
不包含凭据：

```python
from super_ai.llm import build_default_llm_provider

provider = build_default_llm_provider()
result = await provider.check_readiness()
```

## 内存存储

后端内存层存储聊天会话、消息、AIOps 诊断任务，
报告、工具调用审计以及 LangGraph checkpoints 的仓库背后
`src/super_ai/memory` 中的接口

默认的本地数据库 URL 是：

```json
"memoryDatabaseUrl": "sqlite+aiosqlite:///./var/memory.sqlite3"
```

使用 Alembic 初始化或升级本地 SQLite 模式：

```bash
mkdir -p var
uv run alembic upgrade head
```

业务服务应依赖 `MemoryRepositories`，
`ChatMemoryRepository`，或 `DiagnosticMemoryRepository` 从
`super_ai.memory.repositories`。SQLite 特定的代码位于
`super_ai.memory.sqlite`。

## Milvus 向量存储

Milvus 向量存储位于 `src/super_ai/vector_store` 下。导入 Milvus
包仅定义了设置、模式帮助程序和仓库风格的边界；
它不会创建 Milvus 客户端或连接到 Milvus。请
从显式的启动流程或
维护流程中调用 Milvus，当由 Compose 管理的 Milvus 服务就绪时。

默认本地设置：

```json
{
  "uri": "http://localhost:19530",
  "collectionName": "knowledge_chunks",
  "vectorDimension": 1024,
  "indexType": "HNSW",
  "metricType": "COSINE",
  "indexParams": {"M": 16, "efConstruction": 200},
  "searchParams": {"ef": 64}
}
```

chunk 集合将 tenant ownership 存储为标量字段
(`ownerUserId`, `tenantId`, `knowledgeBaseId`, `documentId`, `chunkId`) 以及在
chunk 元数据中，以便检索时可以根据经过身份验证的 tenant 范围进行过滤。

## 身份验证

API 暴露了：

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/logout`
- `GET /auth/me`

密码通过 `pwdlib` 使用 Argon2 进行哈希处理；明文密码不会被存储。
身份验证会话使用不透明的 bearer 令牌，该令牌一旦返回给前端就会被使用。
仅在 SQLite 中存储 SHA-256 令牌哈希，因此注销可以撤销当前会话。
。

知识库、聊天和 AIOps API 路由需要：

```text
Authorization: Bearer <token>
```
