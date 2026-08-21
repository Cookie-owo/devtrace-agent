## ADDED Requirements

### Requirement: Character-granularity model content SSE
聊天流 SHALL 将模型最终回答拆分为每个 `content.delta` 只包含一个字符的有序 SSE 事件。

#### Scenario: Multi-character model content is streamed
- **WHEN** Agent runner 产生一个包含多个字符的 `ChatAgentContentDelta`
- **THEN** 后端 MUST 按原顺序发出逐字符 `content.delta`，sequence MUST 逐个递增，持久化 assistant 正文 MUST 与原内容一致

#### Scenario: Non-content events pass through unchanged
- **WHEN** Agent runner 产生 reasoning、tool call 或 reference 事件
- **THEN** 后端 MUST 保持该事件原有负载和粒度，不得按字符拆分
