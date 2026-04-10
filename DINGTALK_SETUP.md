# 钉钉推送配置指南

## 为什么选择钉钉推送？

| 推送方式 | 每日限制 | 费用 | 推荐度 |
|---------|---------|------|--------|
| 钉钉Webhook | **无限制** | 免费 | ⭐⭐⭐⭐⭐ |
| Server酱免费版 | 5条 | 免费 | ⭐⭐ |
| Server酱付费版 | 500条+ | ¥9.9/月 | ⭐⭐⭐ |
| 邮件推送 | 无限制 | 免费 | ⭐⭐⭐⭐ |

## 配置步骤

### 步骤1：创建钉钉群

1. 打开钉钉客户端（PC或手机）
2. 创建一个新群聊，或选择现有群聊
3. 建议群名：`AI科技早报推送`

### 步骤2：添加群机器人

1. 进入群聊
2. 点击右上角 **群设置** 图标
3. 选择 **智能群助手**
4. 点击 **添加机器人**
5. 选择 **自定义** 机器人（通过Webhook接入）

### 步骤3：配置机器人

1. **机器人名称**：`AI科技早报`
2. **机器人头像**：选择默认或自定义
3. **安全设置**（必选）：
   - 选择 **自定义关键词**
   - 添加关键词：`早报`（必须包含在消息标题中）
   
   > ⚠️ 注意：钉钉要求消息必须包含关键词才能推送成功

### 步骤4：获取Webhook URL

1. 完成配置后，钉钉会生成Webhook URL
2. URL格式：`https://oapi.dingtalk.com/robot/send?access_token=xxxxxx`
3. **复制完整URL**（包含access_token参数）

### 步骤5：配置到项目

打开 `config.json` 文件，将Webhook URL填入：

```json
{
  "push": {
    "serverchan_key": "SCT325378T2knp9EXAJ2lNuqecF1nix7AE",
    "dingtalk_webhook": "https://oapi.dingtalk.com/robot/send?access_token=你的token",
    "pushplus_token": "b001a6b489f54757976e09570af0e488",
    "emails": ["liwei0@huawei.com"]
  }
}
```

### 步骤6：测试推送

运行测试：

```bash
python main.py --test
```

查看钉钉群是否收到消息。

## 常见问题

### Q1: 推送失败，提示"关键词不匹配"

**原因**：钉钉安全设置要求消息必须包含关键词

**解决**：确保消息标题包含关键词`早报`，或修改机器人关键词设置

### Q2: 推送失败，提示"token无效"

**原因**：Webhook URL不完整或错误

**解决**：重新复制完整的Webhook URL（包含`access_token`参数）

### Q3: 如何关闭Server酱推送？

**方法**：在 `config.json` 中删除或清空 `serverchan_key`：

```json
{
  "push": {
    "serverchan_key": "",
    "dingtalk_webhook": "https://oapi.dingtalk.com/robot/send?access_token=xxx",
    ...
  }
}
```

### Q4: 可以同时推送到多个钉钉群吗？

**方法**：创建多个机器人，获取多个Webhook URL

**代码修改**：在 `main.py` 中添加多个推送调用

```python
# 推送到多个钉钉群
push_dingtalk(config, title, content)  # 群1
push_dingtalk(config2, title, content)  # 群2
```

## 推送效果预览

钉钉推送采用Markdown格式，显示效果：

```
🤖 AI科技早报 - 2026年04月05日

📅 2026年04月05日 | 精选10条

1. AI 让英国学生"不会思考"，近 6000 名英格兰中学教师表示担忧
[阅读原文](https://www.ithome.com/...)

2. 微软 Win11 新版 Copilot 内置完整 Edge 浏览器，内存占用飙升
[阅读原文](https://www.ithome.com/...)

...
```

## 技术说明

- **推送方式**：钉钉Webhook API（POST请求）
- **消息格式**：Markdown
- **超时时间**：30秒
- **错误处理**：自动捕获并记录错误信息

---

**配置完成后，每日早报将自动推送到钉钉群，无次数限制！**