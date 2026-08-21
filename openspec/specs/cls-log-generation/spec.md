# cls-log-generation Specification

## Purpose

为使用安全的合成操作日志对真实的腾讯云 CLS 进行初始化，定义一个独立的脚本。
## Requirements
### Requirement: Standalone safe CLS log seeding script
仓库 SHALL 提供了一个独立的 Python 脚本，该脚本生成安全的结构化 Java 电子商务量化服务事件日志，涵盖错误、超时、服务不可用、CPU 或内存压力、请求失败、重试和恢复场景，不包含凭据、令牌、个人 user 数据或调用者提供的原始日志内容。生成的字段 MUST 与记录的本地 Alertmanager fixture 和 SOP 相关联。

#### Scenario: Script uploads a generated batch
- **WHEN** 开发者使用有效的有界计数调用脚本
- **THEN** 它 MUST 使用腾讯云官方的 Python CLS SDK 将生成的批次上传到 merged 项目配置的主题。

#### Scenario: Script reads tracked target configuration
- **WHEN** 脚本运行时
- **THEN** 它 MUST 从 merged 项目配置中读取已配置的广州区域、端点、日志集 ID、主题 ID 和 CLS 凭据，而不读取本地环境变量。

#### Scenario: Base config leaves personal CLS target fields empty
- **WHEN** 检查 `config/project.json`
- **THEN** `clsLogUpload.region`、`clsLogUpload.logsetId` 和 `clsLogUpload.topicId` MUST 为空字符串，并由用户配置文件覆盖。

#### Scenario: Batch size is bounded
- **WHEN** 提供的计数超出配置范围
- **THEN** 脚本 MUST 在联系 CLS 之前停止。

### Requirement: Java e-commerce incident log batch
CLS 辅助脚本 SHALL 从共享场景目录生成并上传 10 条 Java 电商微服务结构化关键日志。

#### Scenario: Ten logs are generated
- **WHEN** 执行 Java 电商日志生成流程
- **THEN** 输出 MUST 恰好包含 10 条不同 incident 和 trace ID 的日志，并包含 service、alertname、sop、异常类型、耗时或资源指标

#### Scenario: Logs remain safe
- **WHEN** 日志批次被上传到 CLS
- **THEN** 任何日志 MUST NOT 包含 API key、SecretId、SecretKey、密码、token 或真实用户数据
