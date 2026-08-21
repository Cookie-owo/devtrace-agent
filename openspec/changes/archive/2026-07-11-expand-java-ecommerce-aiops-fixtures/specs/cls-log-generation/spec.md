## ADDED Requirements

### Requirement: Java e-commerce incident log batch
CLS 辅助脚本 SHALL 从共享场景目录生成并上传 10 条 Java 电商微服务结构化关键日志。

#### Scenario: Ten logs are generated
- **WHEN** 执行 Java 电商日志生成流程
- **THEN** 输出 MUST 恰好包含 10 条不同 incident 和 trace ID 的日志，并包含 service、alertname、sop、异常类型、耗时或资源指标

#### Scenario: Logs remain safe
- **WHEN** 日志批次被上传到 CLS
- **THEN** 任何日志 MUST NOT 包含 API key、SecretId、SecretKey、密码、token 或真实用户数据
