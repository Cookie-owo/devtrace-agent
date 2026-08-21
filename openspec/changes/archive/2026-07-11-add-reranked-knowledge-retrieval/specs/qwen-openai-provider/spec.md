## ADDED Requirements

### Requirement: Configured Qwen rerank provider
LLM provider SHALL 通过项目配置创建异步文本排序能力，并使用真实阿里云百炼 `qwen3-vl-rerank` HTTP API，而不引入 DashScope SDK。

#### Scenario: Provider creates rerank client
- **WHEN** 应用装配知识检索工具
- **THEN** provider MUST 使用配置中的 API key、rerank endpoint、模型、timeout 和 retry 创建只暴露稳定 `RerankModel` 协议的客户端

#### Scenario: Rerank response is validated
- **WHEN** 阿里云返回排序结果
- **THEN** provider MUST 校验索引和 `relevance_score`，并返回按分数降序排列且索引对应输入文档的结果

#### Scenario: Provider failure is safe
- **WHEN** rerank 请求失败、超时、限流或响应无效
- **THEN** provider MUST 在有限重试后返回不包含 API key 或上游响应敏感内容的明确错误

### Requirement: User project model capability configuration
项目 SHALL 从 `config/user.project.json` 加载 `llm.modelCapabilities`，公共 `config/project.json` SHALL NOT 重复维护该配置。

#### Scenario: Merged configuration is loaded
- **WHEN** 应用加载项目配置
- **THEN** 当前聊天模型的上下文窗口能力和 rerank endpoint MUST 来自追踪的项目配置文件合并结果，而不是本机环境变量
