@echo off
chcp 65001 >nul
echo ============================================
echo    准备GitHub上传文件
echo ============================================
echo.

cd /d "%~dp0"

echo [1] 创建临时目录...
if exist "github_upload" rmdir /s /q "github_upload"
mkdir "github_upload"
mkdir "github_upload\.github\workflows"

echo [2] 复制文件...
copy "config.json" "github_upload\"
copy "main.py" "github_upload\"
copy "requirements.txt" "github_upload\"
copy "README.md" "github_upload\"
copy ".gitignore" "github_upload\"
copy "GITHUB_SETUP.md" "github_upload\"
copy ".github\workflows\daily.yml" "github_upload\.github\workflows\"

echo [3] 创建reports目录...
mkdir "github_upload\reports"
echo. > "github_upload\reports\.gitkeep"

echo.
echo ============================================
echo    准备完成！
echo ============================================
echo.
echo 文件已复制到: %cd%\github_upload
echo.
echo 下一步：
echo   1. 登录 GitHub.com
echo   2. 创建仓库: AI-program001
echo   3. 将 github_upload 文件夹中的所有文件上传
echo   4. 配置 Secrets（详见 GITHUB_SETUP.md）
echo.
pause