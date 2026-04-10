@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================
echo    GitHub 一键上传工具
echo ============================================
echo.

cd /d "%~dp0"

:: 配置区（请根据你的信息修改）
set GITHUB_USER=liwei20170707-sudo
set GITHUB_REPO=AI-News-Daily-Program
set GITHUB_EMAIL=liwei0@huawei.com
set GITHUB_NAME=卫哥

:: 检查Git是否安装
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git未安装，请先安装Git
    echo    下载地址: https://git-scm.com/downloads
    pause
    exit /b 1
)

:: 检查是否在Git仓库中
if not exist ".git" (
    echo 📁 初始化Git仓库...
    git init
    git remote add origin https://github.com/%GITHUB_USER%/%GITHUB_REPO%.git
)

:: 配置Git用户信息
git config user.email "%GITHUB_EMAIL%"
git config user.name "%GITHUB_NAME%"

:: 添加所有文件
echo.
echo 📤 正在添加文件...
git add .

:: 获取提交信息
set /p COMMIT_MSG="请输入提交信息（直接回车使用默认）: "
if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=更新：文档归档 %date% %time:~0,5%
)

:: 提交
echo.
echo 💾 正在提交...
git commit -m "%COMMIT_MSG%"

:: 推送
echo.
echo 🚀 正在推送到GitHub...
git branch -M main
git push -u origin main --force

if errorlevel 1 (
    echo.
    echo ❌ 推送失败！可能原因：
    echo    1. 未配置GitHub认证
    echo    2. 网络连接问题
    echo.
    echo 🔧 解决方案：
    echo    方案A: 使用GitHub CLI（推荐）
    echo       1. 安装: winget install GitHub.cli
    echo       2. 登录: gh auth login
    echo.
    echo    方案B: 使用Personal Access Token
    echo       1. 访问: https://github.com/settings/tokens
    echo       2. 创建Token（勾选repo权限）
    echo       3. 运行: git config --global credential.helper store
    echo       4. 再次运行本脚本，输入用户名和Token
    echo.
) else (
    echo.
    echo ✅ 上传成功！
    echo 🌐 仓库地址: https://github.com/%GITHUB_USER%/%GITHUB_REPO%
)

echo.
pause