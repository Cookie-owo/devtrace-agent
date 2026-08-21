## ADDED Requirements

### Requirement: Non-negative BM25 lexical scoring
知识检索工具 SHALL 使用正 IDF 的 BM25 词法排序语义，并 SHALL NOT 为有关键词命中的候选返回负 `bm25Score`。

#### Scenario: 小语料精确词项保持正分
- **WHEN** tenant 语料只有一个或少量 chunks，查询精确命中错误码或专有词
- **THEN** 命中 chunk 的 `bm25Score` MUST 大于 0。

#### Scenario: 高频词项不产生负贡献
- **WHEN** 查询词项出现在超过一半的 tenant chunks 中
- **THEN** BM25 排序 MUST 为这些命中返回非负分，并 MUST NOT 因累积负 IDF 而惩罚包含更多查询词的文档。

#### Scenario: 未命中词项贡献为零
- **WHEN** 某个 chunk 不包含任何查询词项
- **THEN** 该 chunk MUST NOT 仅因 BM25 变体的常量或 delta 项进入关键词候选。
