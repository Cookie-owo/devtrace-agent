## 1. VitePress 与 Skill

- [x] 1.1 安装 VitePress 并增加 docs 开发、构建和预览命令
- [x] 1.2 创建 `docs/openspec` 符号链接、首页与 VitePress 配置
- [x] 1.3 创建 `.codex/skills/wiki-sync` Skill 和确定性同步脚本
- [x] 1.4 验证 Skill frontmatter 和脚本命令

## 2. 历史同步

- [x] 2.1 校验全部历史归档的 delta specs 与 main specs 同步状态
- [x] 2.2 生成全部 active/archive WIKI 页面
- [x] 2.3 生成并核对变更索引与 Sidebar 顺序
- [x] 2.4 逐项验证所有 `@include` 目标存在且归档路径正确

## 3. 验证与运行

- [x] 3.1 运行 `npm run docs:build` 和 OpenSpec 全量校验
- [x] 3.2 归档本变更并重新同步 WIKI
- [x] 3.3 启动 VitePress 并通过浏览器验证首页、索引和归档页面
- [x] 3.4 检查运行生成物并更新 `.gitignore`
