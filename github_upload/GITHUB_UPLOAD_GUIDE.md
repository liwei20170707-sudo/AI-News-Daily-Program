# GitHub 一键上传指南

## 🚀 三种方案对比

| 方案 | 难度 | 推荐度 | 说明 |
|------|------|--------|------|
| **方案A：GitHub CLI** | ⭐ 简单 | ⭐⭐⭐⭐⭐ | 最简单，自动处理认证 |
| **方案B：Personal Access Token** | ⭐⭐ 中等 | ⭐⭐⭐⭐ | 需要手动创建Token |
| **方案C：SSH密钥** | ⭐⭐⭐ 复杂 | ⭐⭐⭐ | 最安全，但配置复杂 |

---

## 方案A：使用GitHub CLI（推荐）

### 步骤1：安装GitHub CLI

```powershell
# 使用winget安装
winget install GitHub.cli
```

### 步骤2：登录GitHub

```powershell
# 登录GitHub
gh auth login

# 选择：
# ? What account? GitHub.com
# ? Preferred protocol? HTTPS
# ? Authenticate? Login with a web browser
```

### 步骤3：一键上传

```powershell
# 运行脚本
quick_upload.bat

# 输入提交信息，回车即可
```

---

## 方案B：使用Personal Access Token

### 步骤1：创建Token

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token (classic)"**
3. 勾选权限：
   - ✅ repo（全部）
   - ✅ workflow
4. 点击 **"Generate token"**
5. **复制Token**（只显示一次）

### 步骤2：配置Git

```powershell
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入：
# Username: 你的GitHub用户名
# Password: 粘贴Token（不是密码）
```

### 步骤3：一键上传

```powershell
# 运行脚本
upload_to_github.bat
```

---

## 方案C：使用SSH密钥

### 步骤1：生成SSH密钥

```powershell
# 生成密钥
ssh-keygen -t ed25519 -C "你的邮箱"

# 按三次回车（使用默认路径，不设密码）
```

### 步骤2：添加到GitHub

```powershell
# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 复制内容，添加到：
# GitHub → Settings → SSH and GPG keys → New SSH key
```

### 步骤3：修改仓库地址

```powershell
# 使用SSH地址
git remote set-url origin git@github.com:用户名/仓库名.git
```

---

## 📁 脚本说明

### quick_upload.bat（推荐）
- 使用GitHub CLI
- 自动处理认证
- 最简单的方式

### upload_to_github.bat
- 使用Git命令
- 需要配置Token或SSH
- 适合高级用户

---

## 🔧 配置文件修改

编辑 `upload_to_github.bat`，修改以下配置：

```batch
set GITHUB_USER=你的用户名
set GITHUB_REPO=你的仓库名
set GITHUB_EMAIL=你的邮箱
set GITHUB_NAME=你的名字
```

---

## ⚠️ 常见问题

### Q: 推送失败，提示"Permission denied"
**A**: 使用GitHub CLI登录：
```powershell
gh auth login
```

### Q: 推送失败，提示"fatal: 'origin' already exists"
**A**: 更新远程地址：
```powershell
git remote set-url origin https://github.com/用户名/仓库名.git
```

### Q: 如何查看当前配置？
**A**: 运行：
```powershell
git remote -v
git config user.name
git config user.email
```

---

## 🎯 快速开始

```powershell
# 1. 安装GitHub CLI
winget install GitHub.cli

# 2. 登录
gh auth login

# 3. 上传
quick_upload.bat
```

---

_最后更新：2026-04-04_