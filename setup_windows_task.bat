@echo off
chcp 65001 >nul
echo ============================================
echo    配置Windows定时任务
echo ============================================
echo.
echo 此脚本将创建两个Windows定时任务：
echo   1. AI新闻抓取任务 - 每日04:00运行
echo   2. AI新闻推送任务 - 每日07:30运行
echo.

set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%main.py

echo [1] 创建抓取任务（04:00）...
schtasks /create /tn "AI_News_Fetch" /tr "python \"%PYTHON_SCRIPT%\" --test" /sc daily /st 04:00 /f

echo.
echo [2] 创建推送任务（07:30）...
schtasks /create /tn "AI_News_Push" /tr "python \"%PYTHON_SCRIPT%\"" /sc daily /st 07:30 /f

echo.
echo ============================================
echo    定时任务配置完成！
echo ============================================
echo.
echo 查看任务列表：
echo   schtasks /query /tn "AI_News_*"
echo.
echo 删除任务：
echo   schtasks /delete /tn "AI_News_Fetch" /f
echo   schtasks /delete /tn "AI_News_Push" /f
echo.
pause