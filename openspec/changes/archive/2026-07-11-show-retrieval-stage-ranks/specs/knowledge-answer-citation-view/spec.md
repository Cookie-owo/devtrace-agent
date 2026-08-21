## ADDED Requirements

### Requirement: Visible retrieval stage trace
聊天工作区 SHALL 在知识库引用摘要和详情中展示向量、BM25 和 rerank 三阶段的排名与分数。

#### Scenario: 引用命中三个阶段
- **WHEN** 可见引用包含三个阶段的排名和分数
- **THEN** 前端 MUST 展示向量名次与相似度、BM25 名次与原始分、rerank 名次与相关度。

#### Scenario: 粗召回阶段未命中
- **WHEN** 引用的向量或 BM25 排名为空
- **THEN** 前端 MUST 对该阶段显示“未召回”，并 MUST NOT 伪造排名或分数。

#### Scenario: 移动端展示阶段轨迹
- **WHEN** 三阶段引用摘要位于窄视口
- **THEN** 阶段标签 MUST 自动换行且不得产生水平页面溢出。
