# repo-hygiene Specification

## Purpose

定义仓库卫生规则，以防止本地开发元数据进入版本控制。

## Requirements

### Requirement: Ignore local IDE metadata
仓库 SHALL 忽略 JetBrains IDE 项目元数据，因此不会显示为未跟踪或准备提交的项目工件。

#### Scenario: Git status excludes JetBrains metadata
- **WHEN** 本地 `.idea/` 目录存在于仓库根目录
- **THEN** Git 状态 MUST NOT 报告 `.idea/` 为未跟踪或已暂存的路径。

### Requirement: Project configuration is absent from Git
仓库 SHALL 将 `config/project.json` 和 `config/user.project.json` 作为仅本地配置，两个路径不得出现在当前索引或任何可达历史提交中。

#### Scenario: Developer checks Git tracking
- **WHEN** 本地配置文件存在并运行 Git 状态或 `git ls-files`
- **THEN** 两个配置路径 MUST 被忽略且 MUST NOT 被报告为已跟踪或未跟踪变更

#### Scenario: Repository history is inspected
- **WHEN** 检查任一本地或远端分支的完整历史 tree
- **THEN** 任何提交 MUST NOT 包含 `config/project.json` 或 `config/user.project.json`

### Requirement: Known sensitive values are absent from reachable history
仓库 SHALL 从所有可达历史中删除本地配置曾包含的已知模型密钥、云凭据和私有服务地址，即使这些值曾被复制到其他文件。

#### Scenario: Repository history is scanned for known sensitive values
- **WHEN** 对本地和远端所有分支执行已知凭据值、凭据模式和私有服务地址扫描
- **THEN** 任何提交中的任何路径 MUST NOT 包含这些敏感值

### Requirement: Sanitized configuration templates
仓库 SHALL 提供可跟踪的无敏感值配置模板，供新克隆创建本地配置。

#### Scenario: Developer initializes local configuration
- **WHEN** 新克隆缺少本地配置文件
- **THEN** 文档 MUST 指导从模板复制文件，模板 MUST NOT 包含 API key、云凭据、密码或真实资源 ID
