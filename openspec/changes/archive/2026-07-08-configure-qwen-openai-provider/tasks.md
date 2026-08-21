## 1. 后端配置测试

- [x] 1.1 为加载跟踪的 Qwen 配置默认值添加失败测试，包括聊天、嵌入和重新排序模型名称。
- [x] 1.2 为从配置的环境变量中读取 API 键添加失败测试，且在错误或 readiness 输出中不暴露它。
- [x] 1.3 为提供者构建添加失败测试，模拟 readiness 成功，模拟 readiness 失败，并且不存在 DashScope 导入。

## 2. 后端提供者实现

- [x] 2.1 添加 `langchain-openai` 后端依赖并刷新 `uv.lock`。
- [x] 2.2 添加带有非秘密 Qwen 提供者默认值的跟踪 `apps/backend/config/qwen-openai.json`。
- [x] 2.3 实现从文件和环境加载带类型的 LLM 配置。
- [x] 2.4 实现可替换的 LLM 提供者抽象及默认的 `ChatOpenAI` 提供者。
- [x] 2.5 实现异步 readiness/config 检查，并安全地返回成功和失败结果。

## 3. 文档和环境

- [x] 3.1 使用占位符密钥和OpenAI-compatible Qwen 设置更新后端`.env.example`。
- [x] 3.2 使用提供者使用情况和readiness 检查备注更新后端README。
- [x] 3.3 扫描跟踪的文件以确保实际的API 密钥不存在。

## 4. 验证

- [x] 4.1 运行后端测试、代码风格检查和类型检查。
- [x] 4.2 运行前端/包检查和OpenSpec验证。
- [x] 4.3 同步规范，归档更改，提交并通过SSH端口443推送。
