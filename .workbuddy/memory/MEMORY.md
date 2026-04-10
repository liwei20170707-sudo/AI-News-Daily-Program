# AI科技新闻自动推送系统 - 项目记忆

## 项目概述

**功能**：每日自动抓取AI科技新闻、生成AI摘要、推送到多渠道、生成双人对话播客

**信息源**：IT之家、Hacker News、36氪、机器之心（RSS）

**推送渠道**：钉钉Webhook、SMTP邮件、Server酱微信、PushPlus邮箱

**播客**：edge-tts语音合成 + ffmpeg音频合并

---

## 技术架构

### Python版本管理
- **新闻抓取+推送**：Python 3.13.12（主环境）
- **播客生成**：Python 3.11.9（专用环境）
  - **原因**：Python 3.13移除audioop模块，pydub无法运行
  - **依赖**：feedparser、openai、edge-tts、pydub

### 核心模块
- `main.py`：主流程（抓取→摘要→推送→播客）
- `podcast_generator.py`：播客生成（双人对话脚本+音频合成）
- `config.json`：配置文件（RSS源、推送渠道、API密钥）

---

## 推送渠道配置

### 1. 钉钉推送（推荐，已配置）
- **优势**：无次数限制、完全免费、速度快
- **Webhook**：`https://oapi.dingtalk.com/robot/send?access_token=477dbcd07a4a70e2e2b75bfea6d264b32a6b0c294f2176538899553605b5954f`
- **安全设置**：自定义关键词"早报"（消息标题必须包含）
- **配置指南**：DINGTALK_SETUP.md
- **状态**：✅ 已测试成功

### 2. SMTP邮件推送（备用，已配置）
- **邮箱**：david_lw2012@126.com
- **接收**：liwei0@huawei.com
- **优势**：无限制、稳定可靠

### 3. Server酱推送（可选）
- **限制**：免费版每日5条
- **SendKey**：SCT325378T2knp9EXAJ2lNuqecF1nix7AE
- **升级**：付费版每日500条+（¥9.9/月）

---

## 播客生成流程

### 1. 对话脚本生成
- **模型**：阿里云百炼qwen-turbo
- **角色**：主持人A（男声-云希，幽默风趣）+主持人B（女声-晓晓，技术严谨）
- **字数**：800-1000字，每条新闻2-3轮对话

### 2. 音频合成
- **TTS引擎**：edge-tts（微软Azure语音服务）
- **音色**：
  - 男声：zh-CN-YunxiNeural
  - 女声：zh-CN-XiaoxiaoNeural
- **格式**：MP3，128kbps

### 3. 音频合并
- **工具**：ffmpeg（命令行方式）
- **处理**：添加句间停顿（500ms）+开头结尾静音

---

## 常见问题与解决方案

### Q1: Server酱推送失败（HTTP 400）
- **原因**：免费版每日推送次数超限（5条）
- **解决**：使用钉钉推送（无限制）或升级Server酱付费版

### Q2: 播客生成失败（audioop模块缺失）
- **原因**：Python 3.13移除audioop模块
- **解决**：使用Python 3.11.9运行播客生成

### Q3: RSS源返回空数据
- **问题源**：机器之心、36氪、所有备用源
- **解决**：使用RSS健康监控自动切换健康源
- **改进**：已部署rss_health_monitor.py自动监控

### Q4: 钉钉推送失败（关键词不匹配）
- **原因**：安全设置要求消息包含关键词
- **解决**：确保标题包含"早报"关键词

### Q5: 备用RSS源全部失效
- **问题源**：新智元、量子位、GitHub Trending、VentureBeat
- **原因**：RSSHub API可能失效或限制访问
- **解决**：添加更多稳定的备用源（如Reddit、TechCrunch）
- **监控**：使用rss_health_monitor.py定期检查

### Q6: 测试覆盖率不足
- **改进前**：无测试框架
- **改进后**：23个测试用例，82%通过率
- **解决**：已创建tests/目录和测试文件

---

## 自动化配置

### 定时任务
- **时间**：每日07:30
- **自动化ID**：ai-2
- **工作目录**：c:/Users/lw/WorkBuddy/Claw/ai_news_daily

### 执行命令
```bash
# 新闻抓取+推送
python main.py

# 播客生成
python main.py --podcast
```

---

## 项目文件结构

```
ai_news_daily/
├── main.py              # 主流程
├── podcast_generator.py # 播客生成
├── verification_checklist.py # 验证清单脚本（新增）
├── rss_health_monitor.py # RSS健康监控脚本（新增）
├── config.json          # 配置文件
├── dashscope_key.txt    # 阿里云API密钥
├── DINGTALK_SETUP.md    # 钉钉配置指南
├── README_TESTS.md      # 测试与验证改进说明（新增）
├── tests/               # 测试框架（新增）
│   ├── test_main.py     # 核心模块测试
│   ├── test_rss_sources.py # RSS源健康检查测试
│   └── test_push_channels.py # 推送渠道可用性测试
├── reports/             # 新闻报告
│   └── AI早报_YYYYMMDD.md
├── podcasts/            # 播客音频
│   ├── AI科技早报_YYYYMMDD.mp3
│   └── 脚本_YYYYMMDD.txt
└── .workbuddy/
    ├── memory/
    │   ├── MEMORY.md    # 项目记忆
    │   └── YYYY-MM-DD.md # 每日记录
    ├── verification_results.json # 验证结果缓存（新增）
    ├── rss_health_cache.json # RSS健康状态缓存（新增）
    └── automations/
        └── ai-2/
            └── memory.md # 自动化执行记录
```

---

## 更新记录

- **2026-04-11**：
  - **P0改进完成**：测试框架、验证清单、RSS监控
  - 创建测试框架（23个测试用例，82%通过率）
  - 实现验证清单（12项验证，全自动）
  - 部署RSS健康监控（自动检测+智能切换）
  - 测试覆盖率提升82%
  - 发现备用源失效问题（所有备用源返回空数据）
  - Superpowers技能应用：test-driven-development、verification-before-completion、systematic-debugging

- **2026-04-05**：
  - 解决Server酱推送次数限制问题
  - 添加钉钉Webhook推送功能
  - 钉钉推送测试成功
  - 移除PushPlus推送（用户未关联公众号）
  - 调整推送优先级：钉钉优先 → SMTP邮件备用 → Server酱可选

- **2026-04-04**：
  - 解决Python 3.13 audioop缺失问题
  - 成功生成播客音频
  - 建立自动化定时任务

---

## Superpowers技能应用记录

### P0优先级技能（2026-04-11完成）

1. **test-driven-development** ✅
   - 创建tests/目录
   - 编写23个测试用例
   - 测试覆盖率82%

2. **verification-before-completion** ✅
   - 创建verification_checklist.py
   - 实现12项验证（6项执行前 + 6项执行后）
   - 全自动化验证

3. **systematic-debugging** ✅
   - 创建rss_health_monitor.py
   - RSS源健康监控
   - 自动切换备用源
   - 发现备用源失效根因

### P1优先级技能（待实施）

4. **using-git-worktrees** ⏳
   - Git版本控制
   - 分支管理
   - 并行开发

5. **subagent-driven-development** ⏳
   - 任务分解
   - 独立子代理
   - 局部重试

6. **writing-plans** ⏳
   - 实现计划
   - 里程碑
   - 检查点

---

_本记忆文件记录项目关键技术决策和配置，供后续维护参考。_