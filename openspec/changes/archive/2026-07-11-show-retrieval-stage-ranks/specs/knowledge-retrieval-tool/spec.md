## ADDED Requirements

### Requirement: Retrieval stage rank traceability
知识检索工具 SHALL 为最终命中和引用保留向量召回、BM25 召回和 rerank 三阶段的一基排名。

#### Scenario: 候选在两路粗召回中命中
- **WHEN** 最终结果同时来自向量和 BM25 候选列表
- **THEN** 结果 MUST 包含对应的 `vectorRank`、`bm25Rank` 和最终 `rerankRank`。

#### Scenario: 候选只在单路粗召回中命中
- **WHEN** 最终结果只在向量或 BM25 一路出现
- **THEN** 未命中阶段的排名和分数 MUST 为空，命中阶段与 rerank 排名 MUST 保留。

#### Scenario: rerank 改变融合候选顺序
- **WHEN** rerank provider 返回与 RRF 候选顺序不同的排序
- **THEN** `rerankRank` MUST 表示最终输出位置，而不是候选输入 index。
