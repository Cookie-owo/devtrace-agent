## ADDED Requirements

### Requirement: User-initiated document upload
系统 SHALL 仅在 user 明确选择文件并提交时，才允许经过身份验证的 user 上传知识库文档。

#### Scenario: 已认证的 user 上传允许的文档
- **WHEN** 已认证的 user 上传一个允许类型且大小在配置的最大值以内的文档
- **THEN** 系统 MUST 为当前 user 创建一个文档元数据记录，并在统一的成功响应包中返回它。

#### Scenario: Startup does not upload documents
- **WHEN** 应用程序启动时
- **THEN** 它会自动上传或导入内置知识文档。

### Requirement: Document metadata
系统 SHALL 记录文档元数据，包括文档 id、owner user id、知识库 id、原始文件名、字节大小、MIME 类型、内容哈希、上传时间、文档状态、索引状态和可选来源。

#### Scenario: 上传后返回元数据
- **WHEN** 文档上传成功
- **THEN** 响应 MUST 应包含文件名、大小、类型、哈希值、上传时间、文档状态和索引状态。

#### Scenario: 元数据在列表视图和详细视图中返回
- **WHEN** 已认证的 user 列出或读取文档
- **THEN** 的 API MUST 返回持久化的元数据，而不会暴露其他 user 拥有的文档。

### Requirement: Document listing and detail
系统 SHALL 为列出知识库中的文档和读取单个文档详情提供受保护的 API。

#### Scenario: User lists documents
- **WHEN** 已认证的 user 请求其知识库中的文档列表
- **THEN** 系统 MUST 仅返回该 user 拥有的文档，并按上传时间排序。

#### Scenario: User reads document detail
- **WHEN** 已认证的 user 请求属于他们的文档 ID
- **THEN** 系统 MUST 返回该文档的元数据。

#### Scenario: 用户阅读另一个 user 的文档
- **WHEN** 身份验证过的 user 请求另一个 user 拥有的文档 ID
- **THEN** 系统 MUST 以统一的授权错误拒绝该请求。

### Requirement: Document deletion and vector cleanup
系统 SHALL 允许经过身份验证的 user 删除其自己的文档，并使用当前 tenant 范围从 Milvus 中删除该文档的向量 chunk。

#### Scenario: User deletes own document
- **WHEN** 已认证的 user 删除其拥有的文档
- **THEN** 系统 MUST 删除或标记文档元数据，并按 tenant ID、知识库 ID 和文档 ID 范围调用向量删除操作。

#### Scenario: 用户删除另一个 user 的文档
- **WHEN** 已认证的 user 尝试删除由另一个 user 拥有的文档
- **THEN** 系统 MUST 以统一的授权错误拒绝请求，并 MUST NOT 删除 chunk 的向量。

### Requirement: Upload policy
系统 SHALL 在共享 API 合同中定义文件大小、文件类型、重复上传和覆盖策略。

#### Scenario: Oversized file is rejected
- **WHEN** 上传文件超过配置的最大文件大小
- **THEN** 当 API MUST 时，使用统一的验证错误响应拒绝它。

#### Scenario: 不支持的文件类型将被拒绝
- **WHEN** 上传的文件类型或扩展名不在允许的文档集合之外
- **THEN** 如果 API MUST 将使用统一的验证错误响应进行拒绝。

#### Scenario: Duplicate upload without overwrite is rejected
- **WHEN** 一个 user 上传了一个内容哈希值已在相同知识库中存在的文档，且 `overwrite` 不为真  
- **THEN** 的 API MUST 将其拒绝，并返回统一的业务冲突错误响应。

#### Scenario: Duplicate upload with overwrite replaces prior document
- **WHEN** 一个 user 上传了带有 `overwrite=true` 的重复文档
- **THEN** 系统 MUST 移除该哈希值的先前文档向量，将先前文档元数据标记为已删除，并为上传创建新的文档记录。

### Requirement: Frontend document management
前端 SHALL 为上传、列表、状态显示、详细元数据和删除提供经过身份验证的文档管理界面。

#### Scenario: Authenticated user views documents
- **WHEN** 加载已认证的工作区
- **THEN** 前端 MUST 使用存储的 bearer 令牌请求当前 user 的知识库文档，并显示文件名、状态、索引状态、大小和上传时间。

#### Scenario: User uploads selected file
- **WHEN** 一个 user 选择文件并提交上传表单
- **THEN** 前端 MUST 通过共享文档上传 API 发送文件，并在成功后刷新文档列表。

#### Scenario: User deletes a document
- **WHEN** 一个 user 从文档列表中删除文档
- **THEN** 前端 MUST 调用受保护的删除 API 并在成功后从可见列表中移除文档
