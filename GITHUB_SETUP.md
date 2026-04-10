# GitHub Actions 配置指南

## 📋 上传步骤

### 方式一：GitHub网页上传（推荐，无需安装git）

1. **创建仓库**
   - 登录 https://github.com
   - 点击右上角 "+" → "New repository"
   - 仓库名：`AI-program001`
   - 选择 "Public" 或 "Private"
   - 点击 "Create repository"

2. **上传文件**
   - 进入仓库页面
   - 点击 "Add file" → "Upload files"
   - 将 `ai_news_daily` 文件夹中的所有文件拖拽上传
   - **注意**：不要上传 `dashscope_key.txt`（已在.gitignore中）

3. **文件结构**
   ```
   AI-program001/
   ├── .github/
   │   └── workflows/
   │       └── daily.yml
   ├── .gitignore
   ├── config.json
   ├── main.py
   ├── requirements.txt
   ├── README.md
   └── reports/ (可选，GitHub会自动创建)
   ```

---

## 🔐 配置 Secrets

1. 进入仓库页面
2. 点击 "Settings" → "Secrets and variables" → "Actions"
3. 点击 "New repository secret"
4. 添加以下Secret：

| Name | Value |
|------|-------|
| `DASHSCOPE_API_KEY` | `sk-7ee6ec7a4b6b4ea48d76ede32afbf418` |

---

## 🚀 测试运行

1. 进入仓库页面
2. 点击 "Actions" 标签
3. 选择 "AI News Daily Push" 工作流
4. 点击 "Run workflow" → "Run workflow"
5. 等待执行完成，查看日志

---

## ⏰ 定时任务

工作流会自动在以下时间执行：
- **北京时间 07:30**（UTC 23:30）

---

## 📧 推送渠道

| 渠道 | 状态 |
|------|------|
| Server酱微信 | ✅ 已配置 |
| SMTP邮箱 | ✅ 已配置 |
| PushPlus | ⏳ 可选 |

---

## ⚠️ 注意事项

1. **敏感信息**：API Key 通过 GitHub Secrets 配置，不会暴露在代码中
2. **报告存储**：每次运行的报告会保存7天，可在 Actions → Artifacts 中下载
3. **频率限制**：Server酱免费版每天5条，GitHub Actions每天只运行1次，足够使用

---

## 🔧 故障排查

如果推送失败：
1. 检查 Actions 日志中的错误信息
2. 确认 Secrets 配置正确
3. 确认 Server酱/PushPlus 账号状态正常