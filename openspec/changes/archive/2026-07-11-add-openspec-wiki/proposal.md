## Why

OpenSpec 已积累大量变更与归档，但缺少可浏览的文档站点，proposal、design、tasks 和 delta specs 只能从仓库目录逐个查找。需要建立由 OpenSpec 驱动的 VitePress WIKI，并通过仓库 Skill 保证新建和归档后的文档同步可重复执行。

## What Changes

- 在根 workspace 安装 VitePress，提供开发、构建和预览命令。
- 建立 `docs/openspec -> ../openspec` 符号链接、VitePress 配置、首页和变更索引。
- 在 `.codex/skills/wiki-sync` 添加仓库 Skill 与确定性同步/校验脚本。
- 为 active 与 archive 变更生成使用 `@include` 引用 OpenSpec 源文件的 WIKI 页面。
- 同步全部历史归档到 `docs/changes/archive/`，并让索引和 Sidebar 与文件系统保持一致。
- 归档同步强制检查 delta specs 存在、主规格同步状态、include 目标和 VitePress 构建。

## Capabilities

### New Capabilities

- `openspec-wiki`: 定义 OpenSpec 变更到 VitePress WIKI 的同步、校验、历史迁移和运行能力。

### Modified Capabilities

无。

## Impact

- 根 `package.json`、`package-lock.json` 和 VitePress 依赖。
- `docs/.vitepress`、`docs/changes`、`docs/index.md` 和 `docs/openspec` 符号链接。
- `.codex/skills/wiki-sync` 仓库 Skill。
- 不修改既有 OpenSpec 源文件内容。
