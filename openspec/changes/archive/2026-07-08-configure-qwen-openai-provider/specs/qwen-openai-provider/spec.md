## ADDED Requirements

### Requirement: OpenAI-compatible Qwen configuration
后端 SHALL 从跟踪的配置文件和环境变量中加载 Qwen/OpenAI-compatible 模型设置，而不是硬编码的业务代码值。

#### Scenario: 跟踪的配置定义了模型默认值
- **WHEN** 检查后端 Qwen 提供商配置文件
- **THEN** 它 MUST 定义聊天模型 `qwen3.7-max`、嵌入模型 `text-embedding-v4`、重新排序模型 `qwen3-vl-rerank`、OpenAI-compatible 基础 URL、温度、超时、重试参数，以及一个 `api_key_env` 参考。

#### Scenario: Required model credentials are loaded from environment
- **WHEN** 后端 LLM 配置是从跟踪的文件中构建的
- **THEN** 它 MUST 从配置的环境变量中读取密钥值，而不会记录或提交 API 密钥。

#### Scenario: Runtime model options are configurable
- **WHEN** 后端 LLM 配置已构建
- **THEN** 基础 URL、模型名称、温度、超时和重试参数 MUST 可配置并具有安全默认值。

#### Scenario: Missing API key is reported as configuration error
- **WHEN** 配置的 API 环境变量缺失或为空
- **THEN** 配置创建 MUST 失败，并显示一个安全的错误信息，该信息不包含敏感内容。

### Requirement: ### 需求：LangChain ChatOpenAI 提供者
后端 SHALL 使用 `langchain-openai` `ChatOpenAI` 通过 OpenAI-compatible 协议访问 Qwen 。

#### Scenario: 提供者使用配置的值创建 ChatOpenAI
- **WHEN** 默认的 LLM 提供者创建一个聊天模型
- **THEN** 它将配置的模型、API 密钥、基础 URL、温度、超时和重试值传递给 `ChatOpenAI`。

#### Scenario: No DashScope SDK dependency
- **WHEN** 后端业务代码导入 LLM 提供商
- **THEN** 它 MUST NOT 导入 DashScope SDK 或阿里厂商私有 API。

### Requirement: ### 需求：可替换的 LLM 提供者抽象
后端 SHALL 暴露一个提供者抽象，以便以后的 OpenAI-compatible 模型提供者可以替换 Qwen 而不更改业务代码。

#### Scenario: Business code depends on abstraction
- **WHEN** 应用服务需要聊天模型访问权限
- **THEN** 它们 MUST 依赖于 LLM 提供商抽象，而不是直接构建特定提供商的客户端。

#### Scenario: 测试中可以提供提供者
- **WHEN** 测试验证模型相关的行为
- **THEN** 它们 MUST 能够在不进行网络调用的情况下提供假的提供者或假的聊天模型。

### Requirement: LLM readiness check
后端 SHALL 提供一个模型 readiness/config 检查，用于验证配置的提供者是否可以访问该模型。

#### Scenario: Readiness succeeds
- **WHEN** 配置的聊天模型对最小的 health 提示做出响应
- **THEN** readiness MUST 报告成功，包含提供者、模型、基础 URL 和延迟元数据，但不包含敏感信息。

#### Scenario: Readiness fails safely
- **WHEN** 模型初始化或调用失败
- **THEN** readiness MUST 报告失败时使用安全的错误信息，并且 MUST NOT 暴露 API 键。
