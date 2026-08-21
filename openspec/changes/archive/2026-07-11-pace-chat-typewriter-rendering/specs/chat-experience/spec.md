## ADDED Requirements

### Requirement: Perceptible model typewriter pacing
聊天工作区 SHALL 以稳定、可感知的时间间隔逐字显示模型最终回答，而不是在同一渲染帧批量显示多个字符。

#### Scenario: Network delivers content faster than rendering
- **WHEN** SSE 客户端快速收到多个正文字符或一个多字符正文增量
- **THEN** 前端 MUST 将正文拆为字符并在相邻字符之间等待显示节奏，MUST NOT 在一个同步更新中追加整段文本

#### Scenario: Content queue reaches completion
- **WHEN** 后端已经发出 `complete` 事件
- **THEN** 前端 MUST 先按顺序显示此前收到的全部正文字符，再用持久化 assistant 消息完成会话协调

#### Scenario: Non-content event is received
- **WHEN** 前端收到工具调用、知识引用、推理、状态或错误事件
- **THEN** 该事件 MUST 保持原有处理方式，不得进入正文打字机延迟队列
