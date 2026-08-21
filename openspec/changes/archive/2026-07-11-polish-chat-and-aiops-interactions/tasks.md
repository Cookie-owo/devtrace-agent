## 1. 聊天输入与消息尺寸

- [x] 1.1 实现 Enter 发送、Shift+Enter 换行和 IME 保护
- [x] 1.2 禁止聊天 textarea 缩放并稳定输入区域高度
- [x] 1.3 让用户消息气泡按内容收缩并覆盖长文本换行
- [x] 1.4 补充 composer 键盘行为和消息气泡测试

## 2. Skill 上传样例

- [x] 2.1 在 `docs/examples/skills/` 创建 5 个符合上传契约的 `*SKILL.md`
- [x] 2.2 添加样例 README 并自动校验文件数量、命名、编码、大小和内容

## 3. AIOps 执行链

- [x] 3.1 将右栏证据链改为 Planner、Executor、Replanner 的持久化步骤视图
- [x] 3.2 将工具调用改为默认收起的名称、状态和缩进输出
- [x] 3.3 实现 SearchLog、知识检索和通用工具结果的非 JSON 摘要格式
- [x] 3.4 从实时诊断时间线移除工具输出正文
- [x] 3.5 更新 AIOps 组件测试，确保原始 evidence、payload、ID 和 JSON 不可见

## 4. 验证与归档

- [x] 4.1 运行后端、前端、契约和 OpenSpec 全量检查
- [x] 4.2 在桌面与移动端验证聊天和 AIOps 交互并归档变更
