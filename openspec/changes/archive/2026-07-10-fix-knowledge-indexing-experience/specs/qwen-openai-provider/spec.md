## MODIFIED Requirements

### Requirement: OpenAI-compatible Qwen configuration
后端 SHALL 从跟踪的项目配置文件中加载 Qwen/OpenAI-compatible 模型设置和私有仓库开发密钥。

#### Scenario: 跟踪的配置定义了模型默认值
- **WHEN** 检查后端 Qwen 提供商配置文件
- **THEN** 它 MUST 定义聊天模型 `qwen3.7-max`、嵌入模型 `text-embedding-v4`、嵌入维度 `1024`、重新排序模型 `qwen3-vl-rerank`、OpenAI-compatible 基础 URL、温度、超时、重试参数以及内联开发 API 密钥。

#### Scenario: Required model credentials are loaded from configuration
- **WHEN** 后端 LLM 配置是从跟踪的文件构建的
- **THEN** 它 MUST 从跟踪的配置文件中读取 API 键，并 MUST NOT 读取本地机器环境变量。

#### Scenario: Runtime model options are configurable
- **WHEN** 后端 LLM 配置已构建
- **THEN** 基础 URL、模型名称、嵌入维度、温度、超时和重试参数 MUST 可配置并具有安全默认值。

#### Scenario: Missing API key is reported as configuration error
- **WHEN** 内联 API 键缺失或为空
- **THEN** 配置创建 MUST 时应失败，并显示不包含敏感信息的安全错误消息。

## ADDED Requirements

### Requirement: Qwen embedding compatibility
后端 SHALL 使用原始字符串输入和配置的维度创建 OpenAI-compatible 嵌入请求。

#### Scenario: Embedding model preserves raw text inputs
- **WHEN** 默认提供程序为 `text-embedding-v4` 创建一个嵌入模型
- **THEN** 它 MUST 保留原始字符串或字符串数组输入以用于提供程序请求，并 MUST NOT 发送标记 ID 数组。

#### Scenario: Embedding dimensions are explicit
- **WHEN** 默认提供者会创建一个嵌入模型
- **THEN** 它 MUST 会将配置的嵌入维度传递给 OpenAI-compatible 嵌入客户端。
