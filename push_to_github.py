"""
GitHub自动推送脚本
功能：将播客文件和RSS推送到GitHub Pages

使用方式：
  python push_to_github.py [--commit COMMIT_MSG]
"""

import sys
import os
from pathlib import Path
import subprocess
from datetime import datetime

# Windows编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# ========== 配置 ==========

PROJECT_DIR = Path(__file__).parent


# ========== Git操作 ==========

def run_git_command(cmd, check=True):
    """执行Git命令"""
    result = subprocess.run(
        cmd,
        cwd=str(PROJECT_DIR),
        capture_output=True,
        text=True,
        check=check
    )
    
    if result.returncode != 0:
        print(f"❌ Git命令失败: {cmd}")
        print(f"   错误: {result.stderr}")
        if check:
            raise Exception(f"Git命令失败: {result.stderr}")
    
    return result


def push_to_github(commit_msg=None):
    """推送到GitHub"""
    
    print("=" * 60)
    print("🚀 推送到GitHub Pages")
    print("=" * 60)
    
    # 检查Git状态
    print("\n🔍 检查Git状态...")
    result = run_git_command(['git', 'status', '--short'], check=False)
    
    if not result.stdout.strip():
        print("  ✅ 无变更需要推送")
        return True
    
    # 显示变更文件
    print(f"  📝 变更文件:")
    for line in result.stdout.strip().split('\n'):
        print(f"     {line}")
    
    # 生成提交消息
    if not commit_msg:
        today = datetime.now().strftime('%Y年%m月%d日')
        commit_msg = f"更新播客 - {today}"
    
    print(f"\n📝 提交消息: {commit_msg}")
    
    # 添加所有变更
    print("\n➕ 添加变更文件...")
    run_git_command(['git', 'add', '-A'])
    
    # 提交
    print("\n💾 提交变更...")
    run_git_command(['git', 'commit', '-m', commit_msg])
    
    # 推送
    print("\n🚀 推送到GitHub...")
    result = run_git_command(['git', 'push'], check=False)
    
    if result.returncode != 0:
        print(f"  ⚠️ 推送失败: {result.stderr}")
        print("  💡 可能需要检查网络连接或GitHub认证")
        return False
    
    print("  ✅ 推送成功")
    
    # 显示推送URL
    print(f"\n🌐 GitHub Pages地址:")
    print(f"   https://liwei20170707-sudo.github.io/AI-News-Daily-Program/")
    print(f"   RSS订阅: https://liwei20170707-sudo.github.io/AI-News-Daily-Program/podcast.xml")
    
    return True


# ========== 主流程 ==========

def main():
    """主流程"""
    
    # 解析参数
    commit_msg = None
    
    args = sys.argv[1:]
    
    if '--commit' in args:
        idx = args.index('--commit')
        if idx + 1 < len(args):
            commit_msg = args[idx + 1]
    
    # 推送
    success = push_to_github(commit_msg)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ GitHub推送完成！")
        print("=" * 60)
        print("💡 请等待几分钟，GitHub Pages会自动更新")
        print("💡 Pocket Casts会在下次刷新时收到新播客")
    else:
        print("\n❌ GitHub推送失败")
        print("💡 请手动执行: git push")
        sys.exit(1)


if __name__ == "__main__":
    main()