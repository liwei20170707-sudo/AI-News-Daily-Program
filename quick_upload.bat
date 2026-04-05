@echo off
chcp 65001 >nul
echo ============================================
echo    GitHub 快速上传（使用GitHub CLI）
echo ============================================
echo.

cd /d "%~dp0"

:: 检查gh是否安装
gh --version >nul 2>&1
if errorlevel 1 (
    echo ❌ GitHub CLI未安装
    echo.
    echo 正在安装GitHub CLI...
    winget install GitHub.cli --accept-package-agreements --accept-source-agreements
    
    echo.
    echo 请先登录GitHub：
    gh auth login
    echo.
    echo 登录完成后，重新运行此脚本
    pause
    exit /b 1
)

:: 检查登录状态
gh auth status >nul 2>&1
if errorlevel 1 (
    echo 🔐 请先登录GitHub...
    gh auth login
)

:: 设置仓库信息
set REPO=liwei20170707-sudo/AI-News-Daily-Program

:: 获取提交信息
set /p MSG="请输入提交信息: "
if "%MSG%"=="" set MSG=更新文档 %date%

echo.
echo 📤 正在上传到GitHub...

:: 使用gh repo sync或直接git操作
git add .
git commit -m "%MSG%"
git push origin main

if errorlevel 1 (
    :: 如果失败，尝试强制推送
    echo ⚠️ 尝试强制推送...
    git push -u origin main --force
)

echo.
echo ✅ 完成！
echo 🌐 https://github.com/%REPO%
echo.
pause