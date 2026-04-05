@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo    一键上传到GitHub
echo ============================================
echo.

:: 设置提交信息
set MSG=文档归档：更新README和添加一键上传脚本

:: 执行Git操作
echo 📤 正在上传...
git add .
git commit -m "%MSG%"
git push

if errorlevel 1 (
    echo.
    echo ❌ 上传失败！请先配置GitHub认证：
    echo.
    echo 方法1：使用GitHub CLI（推荐）
    echo   winget install GitHub.cli
    echo   gh auth login
    echo.
    echo 方法2：使用Personal Access Token
    echo   1. 访问 https://github.com/settings/tokens
    echo   2. 创建Token（勾选repo权限）
    echo   3. 运行: git config --global credential.helper store
    echo   4. 再次运行本脚本
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ 上传成功！
echo 🌐 https://github.com/liwei20170707-sudo/AI-News-Daily-Program
echo.
pause