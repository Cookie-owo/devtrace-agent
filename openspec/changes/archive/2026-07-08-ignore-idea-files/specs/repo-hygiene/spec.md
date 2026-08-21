## ADDED Requirements

### Requirement: Ignore local IDE metadata
仓库 SHALL 忽略 JetBrains IDE 项目元数据，因此不会显示为未跟踪或可提交的项目工件。

#### Scenario: Git status excludes JetBrains metadata
- **WHEN** 本地 `.idea/` 目录存在于仓库根目录中
- **THEN** Git 状态 MUST NOT 报告 `.idea/` 为未跟踪或已暂存的路径。
