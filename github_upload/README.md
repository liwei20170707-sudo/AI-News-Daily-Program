# AI科技新闻自动推送系统

## 📋 系统概述

每日自动抓取AI科技新闻，生成智能摘要，推送到微信和邮箱，并生成双人对话播客。

**GitHub仓库**：[liwei20170707-sudo/AI-News-Daily-Program](https://github.com/liwei20170707-sudo/AI-News-Daily-Program)

**播客订阅**：[点击订阅](https://liwei20170707-sudo.github.io/AI-News-Daily-Program/podcast.xml)

---

## 🎯 功能特性

### 阶段一：文字早报
- ✅ RSS自动抓取（IT之家、Hacker News、36氪）
- ✅ AI智能摘要（阿里云百炼qwen-turbo）
- ✅ 多渠道推送（Server酱微信 + SMTP邮箱）
- ✅ GitHub Actions定时执行（北京时间07:30）

### 阶段二：双人对话播客
- ✅ 对话脚本生成（大模型改写）
- ✅ 分角色音频生成（男声云希 + 女声晓晓）
- ✅ 音频合并导出（MP3格式）
- ✅ GitHub Pages托管（支持播客App订阅）

### 阶段三：AI短视频（待开发）
- 📋 竖屏字幕视频生成
- 📋 视频号/抖音发布

---

## 🚀 快速开始

### 本地测试

```bash
cd ai_news_daily

# 安装依赖
pip install feedparser requests openai edge-tts pydub

# 测试运行（仅抓取不推送）
python main.py --test

# 立即推送
python main.py

# 生成播客
python main.py --podcast
```

### GitHub Actions部署

1. Fork 或 Clone 本仓库
2. 在 Settings → Secrets 中添加：
   - `DASHSCOPE_API_KEY`：阿里云百炼API Key
3. 进入 Actions → "AI News Daily Push" → Run workflow

---

## 📁 文件结构

```
ai_news_daily/
├── .github/workflows/
│   └── daily.yml              # GitHub Actions工作流
├── config.json                # RSS源和推送配置
├── main.py                    # 主脚本
├── podcast_generator.py       # 播客生成器
├── dashscope_key.txt          # 阿里云百炼API Key（本地）
├── requirements.txt           # Python依赖
├── README.md                  # 本文件
├── PODCAST.md                 # 播客订阅说明
├── index.html                 # 播客首页
├── reports/                   # 生成的报告
└── podcasts/                  # 生成的播客音频
```

---

## 🔧 配置说明

### config.json

```json
{
  "feeds": [
    {"name": "IT之家", "url": "https://www.ithome.com/rss", "max_items": 8},
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "max_items": 6},
    {"name": "36氪", "url": "https://36kr.com/feed", "max_items": 5}
  ],
  "push": {
    "serverchan_key": "你的Server酱SendKey",
    "pushplus_token": "你的PushPlus Token",
    "emails": ["your@email.com"]
  }
}
```

---

## 📤 推送渠道

| 渠道 | 说明 | 状态 |
|------|------|------|
| Server酱 | 微信公众号推送 | ✅ |
| SMTP邮箱 | 126邮箱发送 | ✅ |
| GitHub Pages | 播客RSS托管 | ✅ |

---

## 🎙️ 播客订阅

### 订阅链接

```
https://liwei20170707-sudo.github.io/AI-program001/podcast.xml
```

### 支持的播客App

| App | 订阅方式 |
|-----|----------|
| Pocket Casts | 发现 → 粘贴链接 |
| Apple Podcasts | 资料库 → 通过URL关注 |
| 小宇宙 | 搜索「AI科技早报」或分享链接 |
| 其他泛用型App | 添加RSS链接 |

详见 [PODCAST.md](PODCAST.md)

---

## ⏰ 定时任务

- **执行时间**：北京时间每日07:30
- **执行方式**：GitHub Actions云端运行
- **无需本地开机**：完全自动化

---

## 💰 成本分析

| 服务 | 免费额度 | 实际成本 |
|------|----------|----------|
| GitHub Actions | 2000分钟/月 | 0元 |
| 阿里云百炼 | 新用户10万tokens | 0元 |
| Server酱 | 每日5条 | 0元 |
| GitHub Pages | 无限流量 | 0元 |
| edge-tts | 完全免费 | 0元 |

**总成本：0元/月**

---

## 📊 阶段规划

| 阶段 | 功能 | 状态 |
|------|------|------|
| 阶段一 | RSS抓取 + AI摘要 + 推送 | ✅ 完成 |
| 阶段二 | 双人对话播客 + GitHub Pages | ✅ 完成 |
| 阶段三 | AI短视频生成 | 📋 待开发 |

---

## 🔗 相关链接

- [GitHub仓库](https://github.com/liwei20170707-sudo/AI-News-Daily-Program)
- [播客订阅](https://liwei20170707-sudo.github.io/AI-News-Daily-Program/podcast.xml)
- [问题反馈](https://github.com/liwei20170707-sudo/AI-News-Daily-Program/issues)

---

## 📝 更新日志

### 2026-04-04
- ✅ 完成阶段一：文字早报推送
- ✅ 完成阶段二：双人对话播客
- ✅ GitHub Actions定时任务配置
- ✅ GitHub Pages播客托管
- ✅ Pocket Casts订阅成功

---

_由 AI科技新闻自动推送系统 生成_