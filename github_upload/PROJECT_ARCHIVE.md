# AI科技新闻自动推送系统 - 项目归档文档

**项目名称**：AI科技新闻自动推送系统  
**项目位置**：`ai_news_daily/`  
**完成日期**：2026-04-04  
**项目状态**：阶段一+阶段二已完成 ✅

---

## 📋 项目概述

### 项目目标
每日自动抓取AI科技新闻，生成智能摘要，推送到微信和邮箱，并生成双人对话播客。

### 核心功能
1. **文字早报**：RSS抓取 + AI摘要 + 多渠道推送
2. **双人播客**：对话脚本生成 + 分角色音频 + 播客托管

---

## 🏗️ 技术架构

### 技术栈
| 模块 | 技术 | 说明 |
|------|------|------|
| RSS抓取 | feedparser | Python RSS解析库 |
| AI摘要 | 阿里云百炼 qwen-turbo | 北京地域 |
| 推送-微信 | Server酱 | 公众号推送 |
| 推送-邮箱 | SMTP | 126邮箱 |
| 播客-脚本 | 阿里云百炼 | 对话改写 |
| 播客-音频 | edge-tts | 微软TTS |
| 播客-合并 | pydub + FFmpeg | 音频处理 |
| 定时任务 | GitHub Actions | 云端运行 |
| 播客托管 | GitHub Pages | RSS托管 |

### 信息源
| 类型 | 平台 | RSS地址 |
|------|------|---------|
| 主源 | IT之家 | https://www.ithome.com/rss |
| 主源 | Hacker News | https://hnrss.org/frontpage |
| 主源 | 36氪 | https://36kr.com/feed |
| 备用 | 新智元 | https://rsshub.app/xinzhiyuan |
| 备用 | 量子位 | https://rsshub.app/qbitai |

---

## 🔧 配置信息

### 推送配置
| 配置项 | 值 |
|--------|-----|
| 收件邮箱 | liwei0@huawei.com |
| Server酱SendKey | SCT325378T2knp9EXAJ2lNuqecF1nix7AE |
| PushPlus Token | b001a6b489f54757976e09570af0e488 |
| 阿里云百炼API Key | sk-7ee6ec7a4b6b4ea48d76ede32afbf418 |
| 126邮箱授权码 | YYVBJ4F8cGBrGCXQ |

### GitHub配置
| 配置项 | 值 |
|--------|-----|
| 仓库 | liwei20170707-sudo/AI-News-Daily-Program |
| 播客订阅 | https://liwei20170707-sudo.github.io/AI-News-Daily-Program/podcast.xml |
| 工作流权限 | Read and write permissions |

### 播客音色
| 角色 | 音色代码 | 特点 |
|------|----------|------|
| 男声（云希） | zh-CN-YunxiNeural | 幽默风趣 |
| 女声（晓晓） | zh-CN-XiaoxiaoNeural | 技术严谨 |

---

## 📁 文件清单

### 核心文件
```
ai_news_daily/
├── .github/workflows/daily.yml    # GitHub Actions工作流
├── config.json                    # 配置文件
├── main.py                        # 主脚本（阶段一+阶段二）
├── podcast_generator.py           # 播客生成器
├── dashscope_key.txt              # 阿里云百炼API Key
├── requirements.txt               # Python依赖
├── README.md                      # 使用说明
├── PODCAST.md                     # 播客订阅说明
├── index.html                     # 播客首页
└── GITHUB_SETUP.md                # GitHub配置指南
```

### 辅助脚本
```
├── test_local.bat                 # 本地测试
├── run_push.bat                   # 立即推送
├── run_push_no_summary.bat        # 快速推送（无摘要）
├── test_email.py                  # 邮件测试
├── test_podcast_simple.py          # 播客测试
```

### 输出目录
```
├── reports/                       # 生成的报告
│   └── AI早报_YYYYMMDD.md
└── podcasts/                      # 生成的播客
    ├── AI科技早报_YYYYMMDD.mp3
    └── 脚本_YYYYMMDD.txt
```

---

## 📊 项目成果

### 功能完成度
| 阶段 | 功能 | 完成度 |
|------|------|--------|
| 阶段一 | RSS抓取 | ✅ 100% |
| 阶段一 | AI摘要 | ✅ 100% |
| 阶段一 | 微信推送 | ✅ 100% |
| 阶段一 | 邮箱推送 | ✅ 100% |
| 阶段一 | GitHub Actions | ✅ 100% |
| 阶段二 | 对话脚本 | ✅ 100% |
| 阶段二 | 音频生成 | ✅ 100% |
| 阶段二 | 音频合并 | ✅ 100% |
| 阶段二 | 播客托管 | ✅ 100% |
| 阶段二 | 播客订阅 | ✅ 100% |

### 运行数据
| 指标 | 数值 |
|------|------|
| 信息源 | 3个主源 + 3个备用 |
| 每日新闻 | 约20条精选 |
| 播客时长 | 3-5分钟 |
| 推送渠道 | 3个 |
| 运行成本 | 0元/月 |
| 维护频率 | 无需日常维护 |

---

## ⚠️ 踩坑记录

### 技术问题
1. **Python 3.13兼容性**：audioop模块已移除，需安装audioop-lts
2. **GitHub Actions权限**：需启用"Read and write permissions"
3. **Server酱频率限制**：免费版每日5条
4. **阿里云百炼地域**：北京地域sk-xxx，新加坡地域sk-sp-xxx
5. **GitHub Pages音频路径**：RSS中需包含podcasts/目录前缀

### 解决方案
| 问题 | 解决方案 |
|------|----------|
| audioop缺失 | pip install audioop-lts |
| Actions权限不足 | Settings → Actions → Read and write |
| Server酱超限 | 每日只推送1次，足够使用 |
| API Key格式错误 | 确认地域，使用正确的base_url |
| 音频404 | RSS中音频URL添加podcasts/前缀 |

---

## 🚀 后续规划

### 阶段三：AI短视频
- 📋 竖屏字幕视频生成
- 📋 FFmpeg视频合成
- 📋 视频号/抖音发布

### 优化方向
- 📋 首页index.html部署
- 📋 数据统计模块
- 📋 用户反馈机制
- 📋 关键词过滤
- 📋 多语言支持

---

## 📝 更新记录

### 2026-04-04
- ✅ 项目启动
- ✅ 阶段一开发完成
- ✅ 阶段二开发完成
- ✅ GitHub Actions配置
- ✅ GitHub Pages部署
- ✅ Pocket Casts订阅成功
- ✅ 项目文档归档

---

## 🔗 相关链接

- **GitHub仓库**：https://github.com/liwei20170707-sudo/AI-News-Daily-Program
- **播客订阅**：https://liwei20170707-sudo.github.io/AI-News-Daily-Program/podcast.xml
- **问题反馈**：https://github.com/liwei20170707-sudo/AI-News-Daily-Program/issues

---

_归档日期：2026-04-04_  
_项目状态：阶段一+阶段二已完成 ✅_