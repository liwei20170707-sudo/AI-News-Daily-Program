# 更新日志 (CHANGELOG)

## [v2.0.0] - 2026-04-04

### 新增功能
- ✅ **阶段二：双人对话播客**
  - 对话脚本自动生成（阿里云百炼qwen-turbo）
  - 分角色音频生成（男声云希 + 女声晓晓）
  - 音频合并导出（MP3格式）
  - GitHub Pages播客托管
  - 播客RSS订阅支持

### 优化改进
- 📝 更新README.md，添加播客功能说明
- 📝 新增PODCAST.md播客订阅指南
- 📝 新增PROJECT_ARCHIVE.md项目归档文档
- 📝 新增index.html播客首页
- 🔧 修复GitHub Actions权限问题
- 🔧 修复GitHub Pages音频路径问题

### 配置变更
- 收件邮箱移除Gmail，仅保留liwei0@huawei.com
- 添加GitHub Actions写入权限配置

### 已知问题
- ⚠️ 机器之心RSS源不稳定
- ⚠️ edge-tts偶尔网络波动导致音频生成失败

---

## [v1.0.0] - 2026-04-04

### 新增功能
- ✅ **阶段一：文字早报**
  - RSS自动抓取（IT之家、Hacker News、36氪）
  - AI智能摘要（阿里云百炼qwen-turbo）
  - Server酱微信推送
  - SMTP邮箱推送（126邮箱）
  - GitHub Actions定时任务（北京时间07:30）

### 技术架构
- Python 3.11 + feedparser + openai
- 阿里云百炼API（北京地域）
- GitHub Actions云端运行
- Server酱 + SMTP双渠道推送

### 配置信息
- 信息源：IT之家、Hacker News、36氪
- 推送时间：北京时间07:30
- 收件邮箱：liwei0@huawei.com

---

## 版本说明

### 版本号规则
- **主版本号**：重大功能更新（阶段升级）
- **次版本号**：功能优化和bug修复
- **修订号**：小改动和配置调整

### 当前版本
- **v2.0.0**：阶段一+阶段二完成

---

_最后更新：2026-04-04_