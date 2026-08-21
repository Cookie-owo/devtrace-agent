## 1. 配置与 Provider

- [x] 1.1 将模型能力配置迁移到 `config/user.project.json`，并增加 rerank endpoint 配置与加载校验
- [x] 1.2 实现异步 `RerankModel` 协议和阿里云 `qwen3-vl-rerank` HTTP client，覆盖超时、重试、响应校验与安全错误
- [x] 1.3 将 rerank model 接入 Qwen provider 与应用依赖装配

## 2. 两阶段知识检索

- [x] 2.1 将 tenant 范围的 Milvus 粗召回结果交给 rerank，并返回最多 5 条精排降序命中
- [x] 2.2 在命中、引用、聊天和 AIOps 转换链路中保留 `vectorScore`、`rerankScore` 与兼容 `score`
- [x] 2.3 补充空结果、topK、权限过滤、排序和精排失败测试

## 3. 契约与前端

- [x] 3.1 更新 TypeScript、SSE 与 OpenAPI 共享契约中的双分数字段和 topK 上限
- [x] 3.2 将“本次回答引用”按精排分降序限制为 5 条，并在引用列表和详情展示精排及向量分数
- [x] 3.3 补充前端 store、组件和契约测试

## 4. 验证与交付

- [x] 4.1 使用真实阿里云 endpoint 验证 `qwen3-vl-rerank` 连通性和排序结果
- [x] 4.2 运行后端、前端、共享契约和 OpenSpec 全量检查
- [x] 4.3 归档变更、提交并通过 SSH 443 推送
