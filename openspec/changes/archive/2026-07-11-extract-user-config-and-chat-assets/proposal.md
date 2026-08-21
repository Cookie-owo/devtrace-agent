## Why

当前 `config/project.json` 同时承担项目默认配置和个人凭据配置职责，其他开发者拿到仓库后需要修改较多位置才能启动。聊天装配也仍然依赖项目内固定 catalog，用户无法创建、保存、修改自己的系统提示词，也无法上传并选择自己的 `SKILL.md` 文件，导致实际传给 Agent 的 system prompt 与产品要求不一致。

## What Changes

- 将每人不同的 LLM、CLS MCP、CLS 日志上传目标字段抽到单独的用户配置文件，基础配置保留结构但对应值置空。
- 后端与前端读取项目配置时对基础配置和用户配置执行深度 merge，业务代码继续只通过配置加载器读取项目配置。
- 将系统提示词从项目固定 catalog 改为当前用户可创建、编辑、保存和选择的持久化资产。
- 将 Skill 从项目固定 catalog 改为当前用户可上传、展示、删除和选择的 `*SKILL.md` 持久化资产。
- 流式聊天 Agent 每次执行时通过 Repository 加载当前用户选择的系统提示词和 Skill 内容，并把这些内容装配进传给 LangChain Agent 的 `system_prompt`。
- 更新共享 API 契约、OpenAPI、前端设置面板和验证覆盖。

## Capabilities

### New Capabilities

- `shared-user-project-configuration`: 定义基础项目配置和用户覆盖配置的 merge 行为，以及需要留给每个使用者修改的个人字段。

### Modified Capabilities

- `chat-prompt-skill-configuration`: 从项目控制的静态提示词和 Skill 目录改为用户范围的提示词与 `SKILL.md` 资产管理。
- `stream-rag-chat`: Agent system prompt 必须使用当前用户选择的提示词和 Skill 内容装配。
- `api-and-sse-contracts`: 增加聊天提示词 CRUD、Skill 上传/删除和配置选择的共享 API 契约。
- `qwen-openai-provider`: Qwen API key、聊天模型和嵌入模型从 merged 项目配置读取，基础配置中的个人字段允许为空。
- `project-foundation`: 项目配置文档和基础配置文件需要表达基础默认值与用户覆盖文件的职责边界。
- `cls-log-generation`: CLS 上传地域、日志集和主题从 merged 项目配置读取，基础配置中的个人字段允许为空。
- `real-mcp-tools`: CLS MCP 凭据从 merged 项目配置读取，基础配置中的个人字段允许为空。

## Impact

- 后端：`project_config`、LLM/CLS 配置消费者、聊天配置 API、SQLite 模型/迁移/Repository、流式聊天服务。
- 前端：聊天装配设置面板、Chat store/client、共享配置读取。
- 契约：`packages/api-contracts` 的聊天配置 DTO 和 OpenAPI 路径。
- 测试：后端配置 merge、用户聊天资产 API、Agent system prompt 生效、前端提示词/Skill 操作。
