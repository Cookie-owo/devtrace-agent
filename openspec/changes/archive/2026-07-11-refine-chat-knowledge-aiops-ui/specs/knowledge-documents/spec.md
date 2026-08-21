## MODIFIED Requirements

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
- **THEN** API MUST 使用统一的业务冲突错误响应拒绝它。

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
