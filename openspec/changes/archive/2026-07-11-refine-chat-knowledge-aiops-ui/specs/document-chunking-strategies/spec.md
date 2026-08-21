## MODIFIED Requirements

### Requirement: Controlled document chunking strategy catalog
系统 SHALL 支持 `fixed-character`、`markdown-heading` 和 `paragraph` 文档 chunking 策略，具有类型化、验证的参数和确定性的默认配置。只有 `fixed-character` 策略 SHALL 接受 `maxCharacters` 和 `overlapCharacters` 参数；其他策略 SHALL 不要求也不展示这些参数。

#### Scenario: User selects fixed character chunking
- **WHEN** 一个 user 使用有效大小和重叠选择固定字符 chunking
- **THEN** 系统 MUST 使用有界字符分片实现拆分文本，同时保留相邻 chunk 之间的配置重叠。

#### Scenario: User selects Markdown heading chunking
- **WHEN** 一个 user 选择 Markdown 标题 chunking 用于带有 `#` 到 `######` 的标题文本
- **THEN** 系统 MUST 按标题上下文对内容进行分组，并且对于过大的部分，确定性地回退到有界字符 chunks。

#### Scenario: User selects paragraph chunking
- **WHEN** user 选择段落 chunking
- **THEN** 系统 MUST 根据段落边界对内容进行分组，并确定性地拆分过长的段落。

#### Scenario: Non-fixed strategy omits fixed-only parameters
- **WHEN** user 在前端选择 `markdown-heading` 或 `paragraph`
- **THEN** 前端 MUST 隐藏最大字符和 overlap 输入，并且后端 MUST 接受只包含 `strategy` 的配置。

#### Scenario: Invalid fixed strategy parameters are rejected
- **WHEN** user 为 `fixed-character` 提供缺失、过小、过大或 overlap 大于等于最大字符的参数
- **THEN** 后端 MUST 使用统一参数错误拒绝请求。

### Requirement: Markdown and PDF indexable text extraction
系统 SHALL 对允许上传的 Markdown 和 PDF 文档生成可索引文本。Markdown SHALL 以 UTF-8 文本读取；PDF SHALL 使用现成 PDF 文本提取库获取文本。

#### Scenario: Markdown text is extracted
- **WHEN** user 上传 UTF-8 Markdown 文件
- **THEN** 后端 MUST 将该 Markdown 正文保存为可索引文本。

#### Scenario: PDF text is extracted
- **WHEN** user 上传包含可选择文本的 PDF 文件
- **THEN** 后端 MUST 使用 PDF 文本提取库保存可索引文本，而不是把 PDF 字节当 UTF-8 文本解码。

#### Scenario: PDF has no extractable text
- **WHEN** user 上传无法提取文本的 PDF 文件
- **THEN** 后端 MUST 使用统一参数错误拒绝上传，并说明该 PDF 无可索引文本。

### Requirement: Bounded deterministic chunk preview
系统 SHALL 从用于索引的相同 chunking 实现中生成一个有限预览，并 SHALL 按保存的策略返回对应的配置字段。

#### Scenario: User previews an uploaded document
- **WHEN** 已认证的 user 请求其拥有文档的 chunk 预览
- **THEN** 系统 MUST 返回保存的配置、总 chunk 数量、截断指示符以及有限的有序 chunk 摘要，而不会暴露其他 user 的文档。

#### Scenario: Preview reflects non-fixed configuration shape
- **WHEN** 预览文档使用 `markdown-heading` 或 `paragraph`
- **THEN** 响应中的配置 MUST 只包含该策略需要的字段，MUST NOT 伪造用户未选择的 overlap 参数。
