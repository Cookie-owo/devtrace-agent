## MODIFIED Requirements

### Requirement: OpenAI-compatible Qwen configuration
后端 SHALL 从跟踪的项目配置文件中加载 Qwen/OpenAI-compatible 模型设置和私有仓库开发密钥。

#### Scenario: 跟踪的配置定义了模型默认值
- **WHEN** 检查后端 Qwen 提供商配置文件
- **THEN** 它 MUST 定义聊天模型 `qwen3.7-max`、嵌入模型 `text-embedding-v4`、重新排序模型 `qwen3-vl-rerank`、OpenAI-compatible 基础 URL、温度、超时、重试参数以及内联开发 API 密钥。

#### Scenario: Required model credentials are loaded from configuration
- **WHEN** 后端 LLM 配置是从跟踪的文件构建的
- **THEN** 它 MUST 从跟踪的配置文件中 API 读取密钥，并 MUST NOT 读取本地机器环境变量。

#### Scenario: Runtime model options are configurable
- **WHEN** 后端 LLM 配置已构建
- **THEN** 基础 URL、模型名称、温度、超时和重试参数 MUST 可配置并具有安全默认值。

#### Scenario: Missing API key is reported as configuration error
- **WHEN** 内联 API 键缺失或为空
- **THEN** 配置创建 MUST 失败，且错误信息安全，不包含敏感内容。
