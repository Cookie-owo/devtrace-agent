## ADDED Requirements

### Requirement: Chat assembly configuration contracts
共享的 API 合同 SHALL 定义了对 user 聊天组装配置的经过身份验证的读取和更新操作，包括目录提示定义、技能定义和选定的ID。

#### Scenario: Frontend reads configuration
- **WHEN** 前端请求经过身份验证的聊天配置端点
- **THEN** 响应 MUST 使用统一的封装，并包含目录和当前 user 选择，而不会暴露另一个 user 的配置。

#### Scenario: Frontend updates configuration
- **WHEN** 前端提交选定的提示ID和技能ID列表
- **THEN** 输入的请求和响应 MUST 使用前端和后端共同消费的共享契约。

### Requirement: Reasoning SSE contract
共享的 SSE 合同 SHALL 支持有序的可选聊天推理增量事件，该事件与最终答案内容不同。

#### Scenario: Reasoning delta is received
- **WHEN** 后端会发出一个由模型提供的推理增量
- **THEN** 事件 MUST 将携带共享的聊天频道、增量文本和序列字段，以便前端可以在当前助手响应下聚合它。
