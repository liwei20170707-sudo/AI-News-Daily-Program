@echo off
chcp 65001 >nul
echo ============================================
echo    AI科技新闻播客生成器 - 测试
echo ============================================
echo.

cd /d "%~dp0"

echo [1] 安装依赖...
pip install edge-tts pydub -q

echo.
echo [2] 检查FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ FFmpeg未安装，请先安装FFmpeg
    echo    下载地址: https://ffmpeg.org/download.html
    echo    或运行: winget install ffmpeg
    pause
    exit /b 1
)

echo.
echo [3] 运行播客生成测试...
python podcast_generator.py

echo.
echo ============================================
echo    测试完成！
echo ============================================
pause