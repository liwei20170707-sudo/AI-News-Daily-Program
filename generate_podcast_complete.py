"""
完整播客生成流程 - 包含RSS更新和GitHub推送
功能：生成播客 + 更新RSS + 推送到GitHub Pages

使用方式：
  python generate_podcast_complete.py
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# Windows编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from podcast_generator_ffmpeg import generate_podcast
from update_podcast_rss import update_podcast_rss
from push_to_github import push_to_github
from openai import OpenAI


async def generate_podcast_complete(client, news_list, date_str=None):
    """完整播客生成流程"""
    
    print("=" * 70)
    print("🎙️ AI科技新闻播客完整生成流程")
    print("=" * 70)
    
    # 1. 生成播客
    print("\n【阶段1】生成播客音频...")
    result = await generate_podcast(client, news_list, date_str)
    
    if not result:
        print("❌ 播客生成失败，退出")
        return None
    
    # 2. 更新RSS
    print("\n【阶段2】更新RSS订阅...")
    rss_success = update_podcast_rss(result['audio_file'], result['script_file'])
    
    if not rss_success:
        print("⚠️ RSS更新失败，但播客已生成")
    
    # 3. 推送到GitHub
    print("\n【阶段3】推送到GitHub Pages...")
    today = datetime.now().strftime('%Y年%m月%d日')
    github_success = push_to_github(f"更新播客RSS - {today}")
    
    if not github_success:
        print("⚠️ GitHub推送失败，需要手动推送")
        print("   手动推送命令: git push")
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("📊 完整流程执行结果")
    print("=" * 70)
    
    print(f"✅ 播客生成: {result['audio_file']}")
    print(f"✅ 脚本保存: {result['script_file']}")
    print(f"✅ 时长: {result['duration'] // 60}分{result['duration'] % 60}秒")
    
    if rss_success:
        print("✅ RSS更新: 成功")
    else:
        print("⚠️ RSS更新: 失败")
    
    if github_success:
        print("✅ GitHub推送: 成功")
        print(f"   🌐 订阅地址: https://liwei20170707-sudo.github.io/AI-News-Daily-Program/podcast.xml")
    else:
        print("⚠️ GitHub推送: 失败（网络问题）")
        print("   💡 请手动执行: cd ai_news_daily && git push")
    
    print("=" * 70)
    
    return {
        'audio_file': result['audio_file'],
        'script_file': result['script_file'],
        'duration': result['duration'],
        'rss_updated': rss_success,
        'github_pushed': github_success
    }


# ========== 测试入口 ==========

if __name__ == "__main__":
    # 测试用的模拟新闻
    test_news = [
        {"title": "OpenAI发布GPT-5", "summary": "OpenAI发布新一代大模型GPT-5，性能提升显著"},
        {"title": "苹果推出AI手机", "summary": "苹果发布搭载AI芯片的新款iPhone，支持本地大模型"},
        {"title": "特斯拉机器人量产", "summary": "特斯拉Optimus机器人开始量产，售价2万美元"},
    ]
    
    # 加载API密钥
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        local_key_file = Path(__file__).parent / "dashscope_key.txt"
        if local_key_file.exists():
            api_key = local_key_file.read_text(encoding='utf-8').strip()
    
    if not api_key:
        print("❌ 请配置DASHSCOPE_API_KEY环境变量")
        sys.exit(1)
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    # 运行完整流程
    asyncio.run(generate_podcast_complete(client, test_news))