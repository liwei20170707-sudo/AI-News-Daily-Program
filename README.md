# AI科技新闻自动推送系统

## 📋 系统概述

每日自动抓取AI科技新闻，生成智能摘要，推送到微信和邮箱。

## 🚀 快速开始

### 1. 配置阿里云百炼API Key

编辑 `dashscope_key.txt`，填入你的API Key：
```
sk-xxxxxxxxxxxxxx
```

或在环境变量中设置：
```bash
export DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxx
```

### 2. 本地测试

```bash
# Windows
test_local.bat

# 或命令行
python main.py --test
```

### 3. 立即推送

```bash
# Windows
run_push.bat

# 或命令行
python main.py
```

## 📁 文件结构

```
ai_news_daily/
├── config.json              # RSS源和推送配置
├── main.py                  # 主脚本
├── dashscope_key.txt        # 阿里云百炼API Key（本地）
├── requirements.txt         # Python依赖
├── test_local.bat           # 本地测试脚本
├── run_push.bat             # 立即推送脚本
├── run_push_no_summary.bat  # 快速推送（无摘要）
├── setup_windows_task.bat   # Windows定时任务配置
├── .github/workflows/
│   └── daily.yml            # GitHub Actions工作流
└── reports/                 # 生成的报告目录
```

## 🔧 配置说明

### config.json

```json
{
  "feeds": [
    {"name": "机器之心", "url": "...", "max_items": 6},
    {"name": "GitHub Trending", "url": "...", "max_items": 5},
    {"name": "IT之家", "url": "...", "max_items": 8},
    {"name": "Hacker News", "url": "...", "max_items": 6}
  ],
  "push": {
    "serverchan_key": "SCT...",
    "pushplus_token": "...",
    "emails": ["xxx@xxx.com"]
  }
}
```

## 📤 推送渠道

| 渠道 | 说明 |
|------|------|
| Server酱 | 微信公众号推送 |
| PushPlus | 邮箱推送 |
| SMTP | 126邮箱直接发送 |
| WorkBuddy | 本地推送接口 |

## ⏰ 定时任务

### Windows定时任务

运行 `setup_windows_task.bat`，自动创建：
- AI_News_Fetch：每日04:00抓取
- AI_News_Push：每日07:30推送

### GitHub Actions

将代码推送到GitHub仓库，在 Settings → Secrets 中添加：
- `DASHSCOPE_API_KEY`

工作流会自动在每日07:30（北京时间）执行。

## 📊 阶段规划

| 阶段 | 功能 | 状态 |
|------|------|------|
| 阶段一 | 文字早报推送 | ✅ 已完成 |
| 阶段二 | 双人对话播客 | 📋 待开发 |
| 阶段三 | AI短视频生成 | 📋 待开发 |

---

🤖 AI科技新闻自动推送系统 | 阿里云百炼智能摘要