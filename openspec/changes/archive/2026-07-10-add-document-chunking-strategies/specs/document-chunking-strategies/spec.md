## ADDED Requirements

### Requirement: Controlled document chunking strategy catalog
系统 SHALL 支持 `fixed-character`、`markdown-heading` 和 `paragraph` 文档 chunking 策略，具有类型化、验证过的参数和确定性的默认配置。

#### Scenario: User selects fixed character chunking
- **WHEN** 一个 user 使用有效大小和重叠选择固定字符 chunking
- **THEN** 系统在保留相邻 chunk 之间配置的重叠的同时，在确定性字符边界处拆分文本。

#### Scenario: User selects Markdown heading chunking
- **WHEN** 一个 user 选择 Markdown 标题 chunking 用于带有 `#` 到 `######` 的标题文本
- **THEN** 系统 MUST 按标题上下文对内容进行分组，并且对于过长的章节，确定性地回退到有限字符 chunks。

#### Scenario: User selects paragraph chunking
- **WHEN** 一个 user 选择段落 chunking
- **THEN** 系统根据段落边界对组内容进行分组，并确定性地拆分过长的段落。

### Requirement: Bounded deterministic chunk preview
系统 SHALL 从与索引使用的相同 chunking 实现中生成一个有限预览。

#### Scenario: User previews an uploaded document
- **WHEN** 已认证的 user 请求其拥有文档的 chunk 预览
- **THEN** 系统 MUST 返回保存的配置、总 chunk 数量、截断指示符以及有限顺序的 chunk 摘录，而不会暴露其他 user 的文档。
