## 1. Embedding 批处理兼容

- [x] 1.1 将默认 Qwen `OpenAIEmbeddings` 客户端的单批文本数量限制为 10
- [x] 1.2 增加默认客户端批量配置的单元测试

## 2. 文档索引回归覆盖

- [x] 2.1 增加超过 10 个 chunk 时完整生成向量并写入向量库的回归测试
- [x] 2.2 运行 Ruff、Pyright、Pytest 和 OpenSpec 验证
