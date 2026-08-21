## ADDED Requirements

### Requirement: VitePress documentation runtime
仓库 SHALL 在根 npm workspace 中提供以 `docs` 为源目录的 VitePress 开发、构建和预览命令，并 SHALL NOT 提交构建或缓存产物。

#### Scenario: 开发者启动 WIKI
- **WHEN** 执行 `npm run docs:dev`
- **THEN** VitePress MUST 启动并提供项目首页与变更 WIKI。

#### Scenario: 文档生产构建
- **WHEN** 执行 `npm run docs:build`
- **THEN** 构建 MUST 成功，且 `docs/.vitepress/dist` 与缓存目录 MUST 被 Git 忽略。

### Requirement: Active change WIKI synchronization
仓库 SHALL 为每个 active OpenSpec 变更在 `docs/changes/active/{name}/index.md` 提供同步页面。

#### Scenario: 新变更同步
- **WHEN** `openspec/changes/{name}` 存在并完成 WIKI 同步
- **THEN** active 页面 MUST 包含 active frontmatter、正确日期和指向 proposal、design、tasks 与 delta specs 的有效相对 `@include`。

### Requirement: Archived change WIKI synchronization
仓库 SHALL 为每个历史和未来归档在 `docs/changes/archive/{date}-{name}/index.md` 提供同步页面。

#### Scenario: 归档变更同步
- **WHEN** `openspec/changes/archive/{date}-{name}` 存在并通过 delta spec 校验
- **THEN** archive 页面 MUST 包含 archived frontmatter，并且所有 include MUST 指向归档后的 OpenSpec 路径。

#### Scenario: delta specs 缺失或未同步
- **WHEN** 归档缺少 delta specs，或 requirement 同步状态与 main spec 不一致
- **THEN** 同步 MUST 阻断，除非用户显性声明跳过。

### Requirement: WIKI navigation consistency
变更页面、`docs/changes/index.md` 与 VitePress Sidebar SHALL 与 OpenSpec active/archive 目录保持一致和相同顺序。

#### Scenario: 全量历史同步
- **WHEN** 执行全量 WIKI 同步
- **THEN** 每个 OpenSpec 变更 MUST 恰好对应一个正确状态的 WIKI 页面，索引与 Sidebar MUST 列出相同条目。

### Requirement: Repository wiki-sync Skill
仓库 SHALL 在 `.codex/skills/wiki-sync` 提供可发现的 Skill，指导 Agent 在 OpenSpec 创建或归档后执行同步和全部必需校验。

#### Scenario: Skill 被加载
- **WHEN** Agent 处理 OpenSpec 创建、归档或 WIKI 同步
- **THEN** Skill MUST 描述 active/archive 流程、frontmatter、include、delta spec、构建和一致性 Guardrails，并提供可重复执行的同步入口。
