## ADDED Requirements

### Requirement: Reranked citation presentation
聊天工作区 SHALL 将本次回答引用按精排分数降序展示，最多展示 5 条，并明确区分精排分数与向量召回分数。

#### Scenario: 本次回答包含引用
- **WHEN** 流式回答收到一个或多个带有精排分数的引用事件
- **THEN** “本次回答引用”列表 MUST 按 `rerankScore` 从高到低显示最多 5 条，并 MUST 将其标记为精排分数

#### Scenario: User opens citation detail
- **WHEN** user 查看某个知识引用详情
- **THEN** 前端 MUST 显示可用的精排分数和向量召回分数，并保持来源、文档及 metadata 可追溯
