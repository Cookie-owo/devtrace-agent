## Context

多个产品表面都需要反馈，分别建表会造成权限和分析口径分裂。反馈应保留目标类型和目标标识，同时由服务验证目标确实属于当前用户。

## Goals / Non-Goals

**Goals:** 统一存储、可更新、可删除、用户隔离、聊天和 AIOps 端上可用。

**Non-Goals:** 本次不自动训练模型、不提供跨用户运营分析后台。

## Decisions

### 统一反馈记录

`user_feedback` 包含 owner、targetType、targetId、subjectId、rating、reason、comment、correction 和时间。`subjectId` 用于消息中的 citation 等子对象。owner + targetType + targetId + subjectId 唯一，重复提交执行更新。

### 目标归属验证

服务按 targetType 查询消息、诊断步骤或报告，并校验 owner。citation 还必须存在于目标消息 metadata 中。不存在和越权统一返回权限错误。

### 渐进式反馈控件

默认只显示赞同/反对图标。选择后再显示原因、评论和纠正输入，避免干扰主要阅读流程；已提交状态可编辑和删除。

## Risks / Trade-offs

- 多态目标无法完全依赖数据库外键，因此必须用服务层归属校验和测试保证完整性。
