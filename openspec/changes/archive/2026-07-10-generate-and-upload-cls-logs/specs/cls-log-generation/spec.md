## ADDED Requirements

### Requirement: Standalone safe CLS log seeding script
仓库 SHALL 提供了一个独立的 Python 脚本，用于生成随机的合成日志，包括错误、超时、服务不可用、CPU 或内存压力、请求失败、重试和恢复场景，无需凭据、令牌、user 数据或调用者提供的原始日志内容。

#### Scenario: Script uploads a generated batch
- **WHEN** 开发者使用有效的有界计数调用脚本
- **THEN** 它 MUST 将使用腾讯云官方 Python CLS SDK 将生成的批次上传到跟踪配置的主题。

#### Scenario: Script reads tracked target configuration
- **WHEN** 脚本运行时
- **THEN** 它会从跟踪的项目配置中读取配置的广州区域、端点、日志集 ID、主题 ID 和 CLS 凭据，而不会读取本地环境变量。

#### Scenario: Batch size is bounded
- **WHEN** 提供的计数超出配置范围
- **THEN** 脚本 MUST 在联系 CLS 之前停止
