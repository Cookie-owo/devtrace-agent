## 1. Milvus 与 BM25 基础能力

- [x] 1.1 增加 `rank-bm25` 依赖并更新 `uv.lock`
- [x] 1.2 为 Milvus 增加 tenant-scoped chunk iterator 列举边界和测试
- [x] 1.3 实现中英文混合分词、内存 BM25 排序及边界条件测试

## 2. 混合召回与融合

- [x] 2.1 并行执行向量召回和 BM25 召回，并统一应用用户、知识库、文档和 metadata 过滤
- [x] 2.2 实现 `RRF(k=60)` 去重融合、确定性排序和最多 20 条 rerank 候选限制
- [x] 2.3 扩展检索命中与引用的 `bm25Score`、`rrfScore`，保持最终精排分语义
- [x] 2.4 覆盖关键词独占命中、双路共同命中、并发、权限隔离、空结果和失败路径测试

## 3. 契约与调用链

- [x] 3.1 更新 TypeScript、OpenAPI 和 SSE 引用契约及契约测试
- [x] 3.2 更新聊天与 AIOps 引用映射，确保阶段分数可持久化和返回

## 4. 验证

- [x] 4.1 运行后端 Ruff、Pyright 和全量 Pytest
- [x] 4.2 运行共享契约和前端 typecheck、测试、构建
- [x] 4.3 使用真实本地 Milvus 与配置的 rerank 模型验证混合检索
- [x] 4.4 运行 `openspec validate --all` 并核对实现与变更规格
