## ADDED Requirements

### Requirement: Uploadable Skill verification samples
仓库 SHALL 提供 5 个可供开发人员手动上传验证的独立 Skill Markdown 样例，且每个文件 MUST 满足当前上传契约。

#### Scenario: Developer inspects Skill samples
- **WHEN** developer 查看仓库中的 Skill 示例目录
- **THEN** 目录 MUST 包含恰好 5 个以 `SKILL.md` 结尾、UTF-8 编码、非空且小于 64KB 的 Markdown 文件

#### Scenario: Developer uploads a sample
- **WHEN** developer 在“skill设置”中选择任一示例文件
- **THEN** 前端和后端校验 MUST 接受该文件，并允许 user 后续多选启用

#### Scenario: Samples remain opt-in
- **WHEN** 项目启动或 user 尚未上传示例
- **THEN** 系统 MUST NOT 自动创建、上传或启用任何示例 Skill
