## 上下文

文档上传已把可索引文本与 metadata 保存到 SQLite，异步索引服务使用一个固定的词边界切分函数写入 Milvus。前端可上传、重建和查看文档，但无法选择切分方式或确认 chunk 的边界。

## Goals / Non-Goals

**目标：**
- 提供固定字符加 overlap、Markdown 标题/章节、段落边界三种确定性策略。
- 在上传请求中保存选择与参数；文档详情通过后端返回有界预览。
- 让预览和异步索引调用同一分片服务，并将策略写入 Milvus chunk metadata。

**非目标：**
- 不引入 LLM 语义分片、外部队列或上传前把文件保存两次。
- 不改变文档所有权、检索过滤、向量维度、Embedding 模型或已有索引任务生命周期。

## 决策

### 使用结构化策略配置保存到文档的 metadata

上传 multipart 增加 `chunking` JSON 字段，服务端验证后将其与 `indexableText` 一起放入现有 document metadata JSON；这避免为首期策略增加冗余列和迁移。默认配置是 `fixed-character`、1200 字符、200 overlap，因此旧文档也可回退到可预测行为。

### 一个切分器服务同时供预览和索引使用

`DocumentChunkingService` 接受文本和配置，产出稳定的 `DocumentChunk` 序列。`fixed-character` 在自然边界截断并保留字符 overlap；`markdown-heading` 在 `#` 至 `######` 标题段落间聚合，过长章节再使用固定字符；`paragraph` 在空行边界聚合，过长段落同样回退。预览仅返回前 12 个 chunk 的索引、字符数、标题（若有）和有界摘录，索引消费完整序列。

### 通过受保护的文档详情预览端点读取

新增文档 chunk 预览端点，先按 user 和 knowledge base scope 读取文档，再用持久化策略生成预览。前端上传成功后自动读取该端点，文档详情也复用它；不会把大文本或所有 chunks 塞进列表响应。

### 保留向量 metadata 中的策略可追溯性

每个 Milvus chunk metadata 额外包含 `chunkingStrategy`、`chunkingParameters`、`chunkIndex` 与可选 `headingPath`，并保留既有 owner/user/tenant 信息。索引失败仍走已有任务状态和重试机制。

## Risks / Trade-offs

- [Markdown 格式不规范] → 标题策略把无标题文本作为一个章节并回退固定字符切分。
- [大文档预览过大] → 预览最多 12 个、每段最多 400 字符，并返回总数与截断标志。
- [旧文档没有配置] → 读取时使用默认固定字符配置，不需要数据迁移。
- [策略参数非法] → API 在保存前返回统一参数错误，不创建文档或任务。

## 迁移计划

1. 发布共享策略和预览契约，后端以默认策略兼容历史文档。
2. 更新上传路由、切分器和索引写入，再部署前端选择与预览。
3. 回滚时可以忽略 metadata 中的 `chunking` 字段，索引服务继续默认固定策略。

## 开放问题

无。首期不实现由模型决定边界的语义分片。
