# api-and-sse-contracts Specification

## Purpose

定义共享后端 API、HTTP 响应、错误、OpenAPI 和 SSE 事件契约，前端和后端实现必须将其作为共同的唯一真实来源。
## Requirements
### Requirement: Unified HTTP response envelope
系统 SHALL 定义一个共享的 HTTP 响应封装，该封装使用稳定的区分器来表示成功响应、业务错误、验证错误和系统错误。

#### Scenario: Successful API response
- **WHEN** 端点成功
- **THEN** 响应契约 MUST 使用成功区分器，包含类型化的 `data`，并包含请求元数据。

#### Scenario: Business error response
- **WHEN** 一个领域规则阻止了该操作  
- **THEN** 响应契约 MUST 使用错误区分器，包括业务错误代码、消息和可选的详细信息列表。

#### Scenario: Validation error response
- **WHEN** 请求参数无效
- **THEN** 响应契约 MUST 包含参数级验证详细信息，包括字段路径、消息和验证代码。

#### Scenario: System error response
- **WHEN** 发生意外的基础架构或服务器故障
- **THEN** 响应契约 MUST 应包含系统错误码和安全消息，而不会泄露秘密或内部堆栈跟踪。

### Requirement: Unified error code catalog
系统 SHALL 定义一个带有稳定代码标识符、分类、HTTP 状态映射和默认消息的共享错误代码目录。

#### Scenario: Error code has category and message
- **WHEN** 导出一个错误代码
- **THEN** 它 MUST 包含一个类别、HTTP 状态和前端和后端都可以使用的默认消息。

#### Scenario: SSE error reuses error structure
- **WHEN** 流操作会发出错误事件
- **THEN** SSE 有效负载 MUST 重用与 HTTP 错误响应相同的结构化错误消息格式。

### Requirement: OpenAPI contract coverage
系统 SHALL 定义一个机器可读的 OpenAPI 合同，涵盖 health 检查、聊天、知识库、知识文档、文档索引任务、索引任务以及 AIOps 诊断。

#### Scenario: Health path is described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它必须包含一个 health 检查端点，并具有成功的响应模式。

#### Scenario: Chat paths are described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它 MUST 包括聊天会话的创建、列出、历史记录、生命周期以及统一的聊天消息流端点。

#### Scenario: Knowledge base paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含知识库列表和文档上传、列出、详细信息及删除端点。

#### Scenario: Document upload policy is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 描述了文档上传的最大文件大小、允许的文件类型、重复哈希冲突行为以及显式覆盖行为。

#### Scenario: Document index task paths are described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它 MUST 应包含用于创建文档索引任务、读取索引任务和重试失败的文档索引任务的受保护操作。

#### Scenario: Index task paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 包含索引任务创建和状态端点。

#### Scenario: AIOps diagnostic paths are described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它应包含诊断创建、状态和流式传输端点。

### Requirement: SSE event contract
系统 SHALL 为聊天流和 AIOps 诊断进度定义了一个具有区分性的 SSE 事件契约。

#### Scenario: Required SSE event types exist
- **WHEN** 检查 SSE 事件类型目录
- **THEN** 它应包含内容差异、工具调用、参考源、任务状态、报告、完成和错误事件类型。

#### Scenario: Tool call lifecycle statuses exist
- **WHEN** 检查 SSE 工具调用事件契约
- **THEN** 它 MUST 表示工具调用的开始、增量、完成和失败状态。

#### Scenario: Chat stream uses shared events
- **WHEN** 聊天流式输出已实现
- **THEN** 它 MUST 仅发出符合共享 SSE 事件契约的事件负载。

#### Scenario: AIOps stream uses shared events
- **WHEN** AIOps 诊断过程输出已实现
- **THEN** 它 MUST 仅发出符合共享 SSE 事件契约的事件负载。

### Requirement: Single source contract consumption
前端和后端 SHALL 实现 API 响应和 SSE 事件来自 `packages/api-contracts` 和 MUST NOT 独立构建临时端点或事件结构。

#### Scenario: Frontend imports shared contracts
- **WHEN** 前端代码需要 HTTP 响应或 SSE 事件类型
- **THEN** 它 MUST 从 `packages/api-contracts` 导入它们。

#### Scenario: Backend aligns with shared contracts
- **WHEN** 后端端点模型或流式事件已实现
- **THEN** 它们 MUST 必须与导出的 `packages/api-contracts` 响应、错误、OpenAPI 和 SSE 合同形状匹配。

### Requirement: Auth API contracts
系统 SHALL 定义注册、登录、注销和当前user 查询的共享身份验证请求、响应和 OpenAPI 合同。

#### Scenario: Auth paths are described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含 `/auth/register`、`/auth/login`、`/auth/logout` 和 `/auth/me` 路径，并具有统一的响应模式。

#### Scenario: Auth DTOs are shared
- **WHEN** 前端或后端代码需要身份验证请求或响应的结构
- **THEN** 它 MUST 会使用身份验证 user、令牌响应、注册请求和登录请求的共享契约定义

### Requirement: Auth error code catalog
系统 SHALL 定义统一的认证错误代码，具有稳定的类别、HTTP 状态映射和默认消息。

#### Scenario: Unauthenticated error is reusable
- **WHEN** 端点会拒绝缺失、无效或被吊销的认证令牌
- **THEN** 它 MUST 会使用共享的认证错误代码和统一的错误响应封装。

#### Scenario: Invalid credentials error is safe
- **WHEN** 登录凭据无效
- **THEN** 共享错误目录 MUST 仅暴露一个无效凭据代码，无法揭示是邮箱还是密码错误。

### Requirement: Protected API contract security
系统 SHALL 将知识库、知识文档、文档索引、聊天和 AIOps API 合同标记为认证表面。

#### Scenario: Protected paths include unauthorized response
- **WHEN** 保护的聊天、知识库、知识文档、文档索引，或 AIOps OpenAPI 路径会被检查
- **THEN** 它们 MUST 应使用统一的错误响应模式返回 401 响应。

#### Scenario: Protected paths declare bearer auth
- **WHEN** 保护聊天、知识库、知识文档、文档索引，或 AIOps OpenAPI 操作被检查
- **THEN** 它们通过 OpenAPI 安全方案声明承载者身份验证。

### Requirement: Authorization error code catalog
系统 SHALL 为未获得访问资源权限的已认证调用者定义统一的授权错误代码。

#### Scenario: Forbidden error is reusable
- **WHEN** 一个受保护的端点会拒绝跨tenant访问
- **THEN** 它应与认证类别使用相同的错误代码，HTTP 403 状态，并且使用安全的默认消息。

### Requirement: Protected API contract authorization responses
系统 SHALL 在认证失败响应之外，对受保护的知识库、知识文档、文档索引、聊天和 AIOps 操作返回授权失败响应。

#### Scenario: Protected paths include forbidden response
- **WHEN** 受保护的聊天、知识库、知识文档、文档索引，或 AIOps OpenAPI 路径将被检查
- **THEN** 它们 MUST 将使用统一的错误响应模式返回 403 响应。

#### Scenario: Resource id paths are tenant scoped
- **WHEN** 受保护的路径针对特定的知识库、知识文档、文档索引任务、聊天会话或诊断ID
- **THEN** 其合同 MUST 要求持有者认证，并通过共享授权错误响应描述被禁止的访问。

### Requirement: Knowledge document contracts
系统 SHALL 导出共享知识文档 DTO、上传策略常量和前端及后端文档管理的响应类型。

#### Scenario: Document DTOs are shared
- **WHEN** 前端或后端代码需要文档元数据结构
- **THEN** 它 MUST 会使用共享的契约定义来表示文档摘要、文档详情、上传响应、列表响应、删除响应、文档状态和索引状态。

#### Scenario: Upload policy constants are shared
- **WHEN** 前端或后端代码验证文档上传策略
- **THEN** 它 MUST 使用共享的合同值来确定最大文件大小、允许的 MIME 类型、允许的扩展名以及覆盖行为。

### Requirement: Document index task contracts
系统 SHALL 导出共享文档索引任务 DTO、状态、请求类型和响应类型，用于前端和后端索引工作流。

#### Scenario: Index task DTOs are shared
- **WHEN** 前端或后端代码需要文档索引任务数据
- **THEN** 它 MUST 使用共享的合同定义来指定索引任务 ID，owner user ID，知识库 ID，文档 ID，状态，失败原因，重试来源和时间戳。

#### Scenario: Index task status catalog is shared
- **WHEN** 前端或后端代码检查文档索引任务状态
- **THEN** 它 MUST 使用共享的 `pending`、`running`、`succeeded` 和 `failed` 状态目录。

### Requirement: Knowledge retrieval tool contracts
系统 SHALL 导出共享知识检索工具 DTO，用于输入、过滤器、命中结果、引用来源和输出，并 SHALL 区分向量召回分与最终精排分。

#### Scenario: Retrieval DTOs are shared
- **WHEN** 前端或后端代码需要知识检索工具的形状
- **THEN** 它 MUST 使用共享合同定义检索查询、最多为 5 的可选 topK、过滤器、结果命中、引用来源、`vectorScore`、`rerankScore` 和空结果输出

#### Scenario: Retrieval output can represent no matches
- **WHEN** 没有检索到文档
- **THEN** 共享输出契约 MUST 表示一个空的 `results` 数组，而不生成回退内容

### Requirement: Knowledge retrieval citation events
共享 SSE 引用源合约 SHALL 支持从精排知识检索结果生成的引用，并统一双分数字段语义。

#### Scenario: Reference source carries retrieval identity
- **WHEN** 聊天流为检索到的知识 chunk 提供引用源
- **THEN** 事件负载 MUST 包含 chunk、文档和知识库的稳定标识符、源文本或 URI、元数据、`vectorScore`、`rerankScore`，且兼容字段 `score` MUST 等于 `rerankScore`

### Requirement: Chat session management contracts
系统 SHALL 导出共享聊天会话和消息 DTO、请求类型、响应类型以及用于聊天会话管理和流式聊天发送的 OpenAPI 路径。

#### Scenario: Chat DTOs are shared
- **WHEN** 前端或后端代码需要聊天会话、聊天消息、消息元数据、列表响应、详细响应、创建请求、追加消息请求、流请求、清除响应或删除响应的结构
- **THEN** 它 MUST 会使用来自 `packages/api-contracts` 的共享契约定义

#### Scenario: Chat lifecycle paths are described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它应包含用于创建会话、列出会话、读取会话历史、追加消息以供持久化使用、流式传输 user 发送、清除消息和删除会话的受保护路径。

#### Scenario: Chat message metadata is described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 聊天消息模式 MUST 包含能够携带引用参考和工具调用标识符的结构化元数据。

#### Scenario: Chat streaming path is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它应包含一个受保护的 SSE 端点，用于流式传输聊天发送，请求体包含 user 内容和可选元数据。

#### Scenario: Chat protected responses are described
- **WHEN** 受保护的聊天会话管理路径将被检查
- **THEN** 它们 MUST 声明承载者身份验证并包含统一的 401 和 403 错误响应。

### Requirement: Tool call audit API contract
共享的 API-contract 包 SHALL 定义了经过身份验证的聊天会话工具调用审计集合及其响应结构，包括父级关联、工具名称、参数、状态、结果摘要、错误消息、时间戳和持续时间。

#### Scenario: Contract describes scoped audit collection
- **WHEN** 前端和后端实现聊天工具审计历史
- **THEN** 两者 MUST 使用相同的导出集合响应类型和 OpenAPI 路径用于 `GET /chat/sessions/{sessionId}/tool-call-audits`。

### Requirement: MCP tool lifecycle uses shared SSE contract
MCP 工具发现、调用、完成和失败 SHALL 应由现有的共享 `tool.call` SSE 生命周期形状表示。

#### Scenario: MCP result is visible to the client
- **WHEN** 一个聊天 MCP 工具完成
- **THEN** 客户端 MUST 接收开始和完成的工具调用事件，然后接收最终响应。

### Requirement: AIOps execution API contract
共享的 API-contract 包 SHALL 为 AIOps 诊断任务定义了经过身份验证的创建、状态、报告和 SSE 流式传输合约。

#### Scenario: Diagnostic stream path is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 描述受保护的 `POST /aiops/diagnostics/{diagnosticId}:stream` 操作及其共享的 SSE 响应结构。

#### Scenario: Diagnostic result has evidence state
- **WHEN** 诊断任务的响应将被序列化
- **THEN** 它 MUST 包含任务状态、查询、输入、结果负载、时间戳和报告数据，足以区分 SOP 支持的计划与通用计划。

### Requirement: AIOps graph stages use shared SSE events
API-contract 包 SHALL 记录了用于 Planner、Executor、Replanner 和 Report 诊断阶段的共享 SSE 事件有效载荷。

#### Scenario: Graph progress is representable
- **WHEN** 诊断节点进行进展或重新规划  
- **THEN** 共享的 `task.status` 事件 MUST 表示图阶段和安全进展细节。

### Requirement: Diagnostic history and evidence-chain API contracts
共享的 API-contract 包 SHALL 定义了经过身份验证的响应类型和 OpenAPI 路径，用于列出 AIOps 诊断历史记录并读取完整的诊断证据链。

#### Scenario: History and evidence-chain paths are described
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它 MUST 使用统一的成功和授权错误响应来描述受保护的 `GET /aiops/diagnostics` 和 `GET /aiops/diagnostics/{diagnosticId}/evidence-chain` 操作。

#### Scenario: Evidence-chain response is typed
- **WHEN** 前端或后端代码使用诊断证据链
- **THEN** 它 MUST 为任务输入、步骤、工具调用、类型化证据、报告、报告证据链接以及 checkpoint 使用共享类型。

### Requirement: Chat assembly configuration contracts
共享的 API 合同 SHALL 定义了对 user 聊天组装配置的经过身份验证的读取和更新操作，包括目录提示定义、技能定义和选定的 ID。

#### Scenario: Frontend reads configuration
- **WHEN** 前端请求经过身份验证的聊天配置端点
- **THEN** 响应 MUST 使用统一的信封，并包含目录和当前 user 选择，而不会暴露另一个 user 的配置。

#### Scenario: Frontend updates configuration
- **WHEN** 前端提交选定的提示ID和技能ID列表
- **THEN** 输入的请求和响应 MUST 使用前端和后端共同消费的共享契约。

### Requirement: Reasoning SSE contract
共享的 SSE 合同 SHALL 支持与最终答案内容不同的有序可选聊天推理增量事件。

#### Scenario: Reasoning delta is received
- **WHEN** 后端会发出一个由模型提供的推理增量
- **THEN** 事件 MUST 会携带共享聊天频道、增量文本和序列字段，以便前端可以在活动助手响应下聚合它。

### Requirement: Document chunking HTTP contracts
共享的 API 合同 SHALL 定义了在文档上传时支持的 chunking 配置，以及对已保存文档的受保护 chunk 预览响应。

#### Scenario: Upload includes chunking configuration
- **WHEN** 前端上传一个带有选定的 chunking 配置的知识文档
- **THEN** 类型的 multipart 请求 MUST 携带配置和响应文档元数据 MUST 会暴露接受的策略。

#### Scenario: Detail preview is requested
- **WHEN** 前端请求其拥有文档的 chunk 预览
- **THEN** 合同 MUST 仅通过统一的 HTTP 响应封装返回一个有界类型预览。

### Requirement: Chat prompt and Skill asset contracts
系统 SHALL 在共享 API 契约中定义用户系统提示词、用户 Skill 文件、聊天装配选择以及对应的受保护 HTTP 路径。

#### Scenario: Prompt CRUD contracts are shared
- **WHEN** 前端或后端实现系统提示词创建、修改、删除和配置读取
- **THEN** 两者 MUST 使用 `packages/api-contracts` 中导出的提示词 DTO、创建请求、更新请求和响应类型。

#### Scenario: Skill upload and delete contracts are shared
- **WHEN** 前端或后端实现 `*SKILL.md` 上传、展示、选择和删除
- **THEN** 两者 MUST 使用共享契约描述 Skill DTO、上传响应、删除响应和配置响应中的 Skill 集合。

#### Scenario: OpenAPI describes chat asset paths
- **WHEN** 检查 OpenAPI 合约
- **THEN** 它 MUST 包含受保护的 `/chat/prompts`、`/chat/prompts/{promptId}`、`/chat/skills` 和 `/chat/skills/{skillId}` 路径，并声明统一的 401、403 和验证错误响应。

#### Scenario: Chat configuration response includes editable assets
- **WHEN** 已认证的 user 读取 `/chat/configuration`
- **THEN** 响应契约 MUST 包含该 user 可编辑的系统提示词内容、上传 Skill 文件名、Skill 内容摘要和当前选择。

### Requirement: Chat memory API contracts
系统 SHALL 在共享契约中定义会话记忆状态、记忆模式更新请求、显式压缩响应和对应的受保护 OpenAPI 路径。

#### Scenario: Memory mode is updated
- **WHEN** 客户端对 `/chat/sessions/{sessionId}/memory` 提交受支持的记忆模式
- **THEN** 后端 MUST 返回包含刷新后记忆状态的会话 DTO

#### Scenario: Manual compression is requested
- **WHEN** 客户端调用 `/chat/sessions/{sessionId}/memory:compact`
- **THEN** 后端 MUST 执行当前 user 会话的手动压缩并返回统一成功响应

### Requirement: Context limit error contract
统一错误目录 SHALL 定义稳定的 `CHAT_CONTEXT_LIMIT_REACHED` 业务错误，供 HTTP 和聊天 SSE 错误事件共同使用。

#### Scenario: Context limit rejects chat stream
- **WHEN** 聊天流因为 95% 上下文硬上限拒绝消息
- **THEN** SSE `error` 事件 MUST 使用 `CHAT_CONTEXT_LIMIT_REACHED` 并提供执行手动压缩的安全中文消息

### Requirement: Retrieval stage rank contracts
共享 HTTP 与 SSE 引用契约 SHALL 支持向量、BM25 和 rerank 阶段排名，并与对应分数字段一起传递。

#### Scenario: 新引用通过 SSE 到达
- **WHEN** 聊天或 AIOps 发出知识库 `reference.source`
- **THEN** 引用 MUST 能够包含 `vectorRank`、`bm25Rank`、`rerankRank` 及对应阶段分数。

#### Scenario: 单路未召回
- **WHEN** 引用只来自一个粗召回阶段
- **THEN** 契约 MUST 允许另一个粗召回阶段的排名和分数为空，且 MUST 保留最终 rerank 排名和分数。

### Requirement: Background job API contracts
共享契约 SHALL 定义后台任务列表、详情、取消、重试和事件订阅结构，包含 kind、resource、status、attempt、时间和安全错误。

#### Scenario: 前端观察后台任务
- **WHEN** 前端查询当前用户任务
- **THEN** 前后端 MUST 使用同一 `BackgroundJob` 契约且状态 MUST 限定为 queued、running、succeeded、failed、cancelled。

### Requirement: User feedback API contracts
共享契约 SHALL 定义反馈 upsert、列表和删除 API，以及 targetType、rating、reason、comment、correction 和时间字段。

#### Scenario: 客户端提交反馈
- **WHEN** 前端提交反馈
- **THEN** 后端 MUST 返回统一 envelope 中的规范化反馈对象。

### Requirement: MCP connection management contracts
共享契约 SHALL 定义 MCP connection CRUD、check 和 discovered tools 响应，并使用统一错误 envelope。

#### Scenario: 前端保存 MCP 连接
- **WHEN** 前端创建或更新连接
- **THEN** 前后端 MUST 使用同一 transport、URL、timeout、retries 和 enabled 字段定义。
