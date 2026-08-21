## MODIFIED Requirements

### Requirement: Document metadata
系统 SHALL 记录文档元数据，包括文档 id、owner user id、知识库 id、原始文件名、字节大小、MIME 类型、内容哈希、上传时间、文档状态、索引状态、可选来源以及可用的可索引上传文本。

#### Scenario: 上传后返回元数据
- **WHEN** 文档上传成功
- **THEN** 响应 MUST 应包含文件名、大小、类型、哈希值、上传时间、文档状态和索引状态。

#### Scenario: 元数据在列表和详细视图中返回
- **WHEN** 已认证的 user 列出或读取文档
- **THEN** 的 API MUST 返回持久化的元数据，而不会暴露其他 user 拥有的文档。

#### Scenario: Indexable text is available to indexing
- **WHEN** 文本兼容的文档上传成功
- **THEN** 后端 MUST 保留足够的可索引文本元数据，以便后续的手动索引任务重新构建 chunk 而无需重新上传文件。

### Requirement: Frontend document management
前端 SHALL 为上传、列表、状态显示、详细元数据、删除和手动索引重建提供经过身份验证的文档管理界面。

#### Scenario: Authenticated user views documents
- **WHEN** 加载已认证的工作区
- **THEN** 前端 MUST 使用存储的 bearer 令牌请求当前 user 的知识库文档，并显示文件名、状态、索引状态、大小和上传时间。

#### Scenario: User uploads selected file
- **WHEN** 一个 user 选择文件并提交上传表单
- **THEN** 前端 MUST 通过共享文档上传 API 发送文件，并在成功后刷新文档列表。

#### Scenario: User deletes a document
- **WHEN** 一个 user 从文档列表中删除文档
- **THEN** 前端 MUST 调用受保护的删除 API 并在成功后从可见列表中移除文档

#### Scenario: User rebuilds a document index
- **WHEN** 一个 user 触发已拥有文档的重新索引
- **THEN** 前端 MUST 调用受保护文档索引任务 API 并从经过身份验证的 API 响应中刷新可见文档/任务状态。
