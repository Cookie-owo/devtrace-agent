## 1. 标准 Skill 资产

- [x] 1.1 将 5 个示例重写为 `<name>/SKILL.md` 目录结构并补齐合法 frontmatter
- [x] 1.2 更新示例 README、上传校验和单元测试，要求标准 name 与 description

## 2. 持久化与契约

- [x] 2.1 为 Skill name/description 增加 SQLAlchemy 字段、Alembic 迁移和 Repository 映射
- [x] 2.2 更新后端 API、OpenAPI、TypeScript 契约和前端 Skill 展示

## 3. LangChain Skill 运行时

- [x] 3.1 实现请求级 `load_skill` LangChain Tool 和轻量 name/description catalog
- [x] 3.2 保持 `create_agent` 并移除完整 Skill system prompt 注入
- [x] 3.3 覆盖渐进式加载、user scope、工具事件和现有聊天行为测试

## 4. 验证与交付

- [x] 4.1 运行后端、前端、OpenSpec 全量检查并修复问题
- [x] 4.2 本地迁移并启动后端、前端及必要基础设施
- [x] 4.3 从前端上传、选择标准 Skill 并通过真实对话验证模型按需加载
- [x] 4.4 同步主规格、归档变更、提交并通过 443 端口推送
