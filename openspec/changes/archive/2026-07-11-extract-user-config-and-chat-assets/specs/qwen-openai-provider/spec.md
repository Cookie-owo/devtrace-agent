## MODIFIED Requirements

### Requirement: OpenAI-compatible Qwen configuration
后端 SHALL 从 merged 项目配置中加载 Qwen/OpenAI-compatible 模型设置和私有仓库开发密钥，其中基础配置保留通用默认值，用户配置提供每个使用者不同的模型和 API key。

#### Scenario: 跟踪的配置定义了模型默认值
- **WHEN** 检查后端 Qwen 提供商配置文件
- **THEN** merged 配置 MUST 定义聊天模型 `qwen3.7-max`、嵌入模型 `text-embedding-v4`、嵌入维度 `1024`、重排序模型 `qwen3-vl-rerank`、OpenAI-compatible 基础 URL、温度、超时、重试参数以及开发 API 密钥。

#### Scenario: Base config leaves personal model credentials empty
- **WHEN** 检查 `config/project.json`
- **THEN** `llm.apiKey`、`llm.chatModel` 和 `llm.embeddingModel` MUST 为空字符串，并由用户配置文件覆盖。

#### Scenario: Required model credentials are loaded from configuration
- **WHEN** 后端 LLM 配置是从项目配置构建的
- **THEN** 它 MUST 从 merged 项目配置文件中读取 API 键，并 MUST NOT 读取本地机器的环境变量。

#### Scenario: Runtime model options are configurable
- **WHEN** 后端 LLM 配置已构建
- **THEN** 基础 URL、模型名称、嵌入维度、温度、超时和重试参数 MUST 可配置并具有安全默认值。

#### Scenario: Missing API key is reported as configuration error
- **WHEN** merged 配置中的 API 键缺失或为空
- **THEN** 配置创建 MUST 失败，并显示不包含敏感信息的安全错误消息。
