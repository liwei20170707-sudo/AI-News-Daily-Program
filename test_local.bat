@echo off
chcp 65001 >nul
echo ============================================
echo    AI科技新闻推送系统 - 本地测试
echo ============================================
echo.

cd /d "%~dp0"

echo [1] 安装依赖...
pip install feedparser requests openai -q

echo.
echo [2] 运行测试（仅抓取，不推送）...
python main.py --test

echo.
echo ============================================
echo    测试完成！查看上方输出预览报告
echo ============================================
pause