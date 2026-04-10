@echo off
chcp 65001 >nul
echo ============================================
echo    安装GitHub CLI
echo ============================================
echo.

echo 正在安装GitHub CLI...
winget install GitHub.cli --accept-package-agreements --accept-source-agreements

if errorlevel 1 (
    echo.
    echo ❌ 安装失败！请手动安装：
    echo    下载地址: https://cli.github.com/
    pause
    exit /b 1
)

echo.
echo ✅ 安装成功！
echo.
echo 接下来请登录GitHub：
echo.
gh auth login
echo.
echo 登录完成后，运行 push.bat 即可一键上传
echo.
pause