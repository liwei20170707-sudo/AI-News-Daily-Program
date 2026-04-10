"""生成今日播客"""
import sys
import asyncio
import re
from pathlib import Path

# Windows编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 设置路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    print("=" * 60)
    print("🎙️ 开始生成AI科技早报播客")
    print("=" * 60)
    
    # 导入模块
    print("\n导入模块...")
    from openai import OpenAI
    from podcast_generator_ffmpeg import generate_podcast
    
    # 读取API Key
    print("读取API Key...")
    api_key_file = Path(__file__).parent / "dashscope_key.txt"
    api_key = api_key_file.read_text(encoding='utf-8').strip()
    
    # 创建客户端
    print("创建阿里云百炼客户端...")
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    # 读取今日报告
    print("读取今日报告...")
    report_file = Path(__file__).parent / "reports" / "AI早报_20260405.md"
    report_content = report_file.read_text(encoding='utf-8')
    
    # 从报告中提取新闻标题和摘要
    print("提取新闻内容...")
    news_items = []
    
    # 匹配格式: ## 数字. 标题
    # > 📌 摘要
    pattern = r'## \d+\. (.+)\n> 📌 (.+)'
    matches = re.findall(pattern, report_content)
    
    for title, summary in matches[:8]:
        news_items.append({
            "title": title,
            "summary": summary
        })
    
    print(f"提取到 {len(news_items)} 条新闻")
    
    # 生成播客
    print("\n开始生成播客...")
    result = asyncio.run(generate_podcast(client, news_items))
    
    if result:
        print("\n" + "=" * 60)
        print("✅ 播客生成成功！")
        print("=" * 60)
        print(f"音频文件: {result['audio_file']}")
        print(f"脚本文件: {result['script_file']}")
        print(f"时长: {result['duration'] // 60}分{result['duration'] % 60}秒")
        print("=" * 60)
    else:
        print("\n❌ 播客生成失败")
        
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()