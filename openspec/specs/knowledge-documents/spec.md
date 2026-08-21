# knowledge-documents Specification

## Purpose

为 tenant-作用域的知识库文档管理定义经过身份验证的上传、文档元数据、状态可见性、删除、向量清理和前端文档工作流，适用于 user-选择的上传。
## Requirements
### Requirement: User-initiated document upload
系统 SHALL 仅在 user 明确选择文件并提交时，才允许经过身份验证的 user 上传知识库文档。

#### Scenario: 已认证的 user 上传允许的文档
- **WHEN** 已认证的 user 上传一个允许类型且大小不超过配置最大值的文档
- **THEN** 系统 MUST 创建由当前 user 拥有的文档元数据记录，并在统一的成功响应封装中返回它。

#### Scenario: Startup does not upload documents
- **WHEN** 应用程序启动时
- **THEN** 它会自动上传或导入内置知识文档。

### Requirement: Document metadata
系统 SHALL 记录文档元数据，包括文档ID、owner user ID、知识库ID、原始文件名、字节大小、MIME 类型、内容哈希、上传时间、文档状态、索引状态、可选来源以及可用的可索引上传文本。

#### Scenario: 上传后返回元数据
- **WHEN** 文档上传成功
- **THEN** 响应 MUST 应包含文件名、大小、类型、哈希、上传时间、文档状态和索引状态。

#### Scenario: 元数据在列表视图和详细视图中返回
- **WHEN** 一个经过身份验证的 user 列出或读取文档
- **THEN** 的 API MUST 返回持久化的元数据，而不会暴露其他 user 拥有的文档。

#### Scenario: Indexable text is available to indexing
- **WHEN** 文本兼容的文档上传成功
- **THEN** 后端 MUST 保留足够的可索引文本元数据，以便后续手动索引任务重新构建 chunk 而无需重新上传文件。

### Requirement: Document listing and detail
系统 SHALL 为列出知识库中的文档和读取单个文档详细信息提供受保护的 API。

#### Scenario: User lists documents
- **WHEN** 身份验证的 user 请求其知识库中的文档列表
- **THEN** 系统 MUST 仅返回该 user 拥有的文档，并按上传时间排序。

#### Scenario: User reads document detail
- **WHEN** 已认证的 user 请求属于自己的文档 ID  
- **THEN** 系统 MUST 返回该文档的元数据。

#### Scenario: 用户阅读另一个 user 的文档
- **WHEN** 身为已认证的 user 请求另一个 user 拥有的文档 ID
- **THEN** 系统 MUST 以统一的授权错误拒绝该请求。

### Requirement: Document deletion and vector cleanup
系统 SHALL 允许经过身份验证的 user 删除其自己的文档，并使用当前 tenant 范围从 Milvus 中删除该文档的向量 chunk。

#### Scenario: User deletes own document
- **WHEN** 已认证的 user 删除其拥有的文档
- **THEN** 系统 MUST 删除或标记为已删除文档元数据，并按 tenant ID、知识库 ID 和文档 ID 范围调用向量删除操作。

#### Scenario: 用户删除另一个 user 的文档
- **WHEN** 一个已认证的 user 尝试删除另一个 user 拥有的文档
- **THEN** 系统 MUST 以统一的授权错误拒绝请求，并 MUST NOT 删除向量 chunk 的。

### Requirement: Upload policy
系统 SHALL 在共享 API 合同中定义文件大小、文件类型、重复上传和覆盖策略。上传文件 SHALL 仅支持 Markdown `.md` 与 PDF `.pdf` 文档。

#### Scenario: Oversized file is rejected
- **WHEN** 上传文件超过配置的最大文件大小
- **THEN** API MUST 使用统一的验证错误响应拒绝它，并提供明确的大小限制说明。

#### Scenario: 不支持的文件类型被拒绝
- **WHEN** 上传的文件扩展名不是 `.md` 或 `.pdf`，或 PDF 的 MIME 类型明显不是 PDF
- **THEN** API MUST 使用统一的验证错误响应拒绝它，并说明只支持 Markdown 与 PDF。

#### Scenario: Markdown browser MIME variants are accepted
- **WHEN** user 上传 `.md` 文件且浏览器提供 `text/markdown`、`text/plain`、空 MIME 或 `application/octet-stream`
- **THEN** API MUST 接受该文件并按 Markdown 文档保存。

#### Scenario: Duplicate upload without overwrite is rejected
- **WHEN** 一个 user 上传了一个内容哈希已在相同知识库中存在的文档，且 `overwrite` 不为真
- **THEN** 的 API MUST 应使用统一的业务冲突错误响应拒绝它。

#### Scenario: Duplicate upload with overwrite replaces prior document
- **WHEN** 一个 user 上传了带有 `overwrite=true` 的重复文档  
- **THEN** 系统 MUST 移除该哈希值的先前文档向量，将先前文档元数据标记为已删除，并为上传创建一个新的文档记录。

### Requirement: Frontend document management
前端 SHALL 为上传、列表、状态显示、详细元数据、删除、上传后自动首次索引以及手动索引重建提供经过身份验证的文档管理界面。前端上传入口 SHALL 只展示 Markdown 与 PDF 限制，并在失败时显示具体恢复方式。

#### Scenario: Authenticated user views documents
- **WHEN** 已认证的工作区加载
- **THEN** 前端 MUST 使用存储的 bearer 令牌请求当前 user 的知识库文档，并显示文件名、状态、索引状态、大小和上传时间。

#### Scenario: User uploads selected file
- **WHEN** 一个 user 选择 Markdown 或 PDF 文件并提交上传表单
- **THEN** 前端 MUST 通过共享文档上传 API 发送文件，为上传的文档创建索引任务，在任务运行时显示文档正在索引，并在成功后刷新文档列表。

#### Scenario: User selects unsupported file locally
- **WHEN** user 在前端选择 `.csv`、`.json`、`.txt` 或其他不支持格式
- **THEN** 前端 MUST 阻止上传并在上传控件附近显示“仅支持 Markdown(.md) 与 PDF(.pdf)”的中文提示。

#### Scenario: User deletes a document
- **WHEN** 一个 user 从文档列表中删除文档
- **THEN** 前端 MUST 调用受保护的删除 API 并在成功后从可见列表中移除文档。

#### Scenario: User rebuilds a document index
- **WHEN** 一个 user 触发所拥有文档的索引或重新索引
- **THEN** 前端 MUST 调用受保护的文档索引任务 API 并从经过身份验证的 API 响应中刷新可见文档/任务状态。

### Requirement: Document upload chunking selection and preview
知识文档工作流 SHALL 接受一个由 user 选择的有效 chunk 配置，将其与所拥有的文档一起保存，并在上传后公开一个受保护的预览。

#### Scenario: Upload persists selected configuration
- **WHEN** 已认证的 user 上传一个允许的文档，并带有有效的 chunking 配置
- **THEN** 系统在创建或运行索引任务之前，将该配置与文档元数据一起存储。

#### Scenario: User reads chunk preview
- **WHEN** 该文档对当前 user 可用
- **THEN** 的 API MUST 使用共享的 chunking 服务，从持久化配置和可索引文本生成其预览。
