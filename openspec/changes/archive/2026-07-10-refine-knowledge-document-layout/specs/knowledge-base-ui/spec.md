## MODIFIED Requirements

### Requirement: Authenticated knowledge document workspace
前端 SHALL 提供一个经过身份验证的 `/knowledge` 工作区，该工作区仅使用共享 API 合同列出已登录 user 的后端服务器知识库和文档。当 user 可以从多个可访问的知识库中进行选择时，它 MUST 仅显示知识库选择控件。

#### Scenario: User opens their knowledge workspace
- **WHEN** 已认证的 user 打开 `/knowledge`
- **THEN** 前端 MUST 从后端加载 user 可访问的知识库和选定基础的文档，而不将浏览器存储视为文档目录。

#### Scenario: User changes the knowledge base selection
- **WHEN** 一个 user 从显示的多库控件中选择一个可访问的知识库
- **THEN** 前端 MUST 仅加载并显示为该选定库返回的文档

#### Scenario: Workspace has one knowledge base
- **WHEN** 该 user 拥有且仅有一个可访问的知识库
- **THEN** 该工作区 MUST 忽略非可操作的知识库选择控件。

#### Scenario: Workspace has no documents
- **WHEN** 选定的知识库没有文档
- **THEN** 工作区 MUST 显示一个清晰的空白状态和可用的上传操作

### Requirement: Document inspection and deletion
前端 SHALL 应在相应文档行下方以折叠优先的内联披露方式显示持久化文档元数据，并允许 user 通过显式的中文确认删除可访问的文档。

#### Scenario: User opens a document detail
- **WHEN** 一个 user 会从工作区展开文档的内联披露
- **THEN** 前端 MUST 使用服务器支持的元数据在该文档行下方显示其文件名、源类型、哈希值、大小、上传时间、文档状态、索引状态、保存的 chunk 策略以及 chunk 预览

#### Scenario: Document detail starts collapsed
- **WHEN** 工作区初始时显示一个文档行
- **THEN** 其元数据和 chunk 预览展开 MUST 应该被折叠，直到 user 展开它。

#### Scenario: User deletes a document
- **WHEN** 一个 user 确认可访问文档的删除
- **THEN** 前端 MUST 调用文档删除端点，并在后端确认删除后，仅删除文档及其显示的任务状态。

#### Scenario: A document request is rejected
- **WHEN** 后端在上传、索引或删除操作中返回规范化的授权、验证或系统错误
- **THEN** 前端 MUST 显示规范化的安全错误，MUST NOT 为该失败操作显示成功本地状态

### Requirement: Chunking selection and preview UI
经过身份验证的知识工作区 SHALL 提供中文控件，用于在上传时选择文档 chunking 策略，并用于在文档的内联披露中查看已保存文档的 chunk 预览。

#### Scenario: User selects a strategy before upload
- **WHEN** 一个 user 选择要上传的文件
- **THEN** 前端 MUST 以固定的字符、Markdown 标题和段落策略及其相关参数，以及可见的选中状态进行展示。

#### Scenario: User reviews uploaded chunks
- **WHEN** 一个 user 在上传后或从文档列表中展开所有文档的内联披露
- **THEN** 前端 MUST 请求并显示保存的策略、总 chunk 数量以及该文档行下方绑定的 chunk 摘录中文内容
