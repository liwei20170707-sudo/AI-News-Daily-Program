"""手动生成播客"""
import sys
import asyncio
from pathlib import Path

# 设置路径
sys.path.insert(0, str(Path(__file__).parent))

# Windows编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

try:
    print("导入模块...")
    from openai import OpenAI
    from podcast_generator import generate_podcast
    
    print("读取API Key...")
    api_key_file = Path(__file__).parent / "dashscope_key.txt"
    api_key = api_key_file.read_text(encoding='utf-8').strip()
    
    print("创建客户端...")
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    print("读取报告...")
    report_file = Path(__file__).parent / "reports" / "AI早报_20260405.md"
    report_content = report_file.read_text(encoding='utf-8')
    
    # 从报告中提取新闻标题
    import re
    titles = re.findall(r'## \d+\. (.+)', report_content)
    
    news_list = [{"title": title, "summary": ""} for title in titles[:8]]
    
    print(f"准备生成播客，共{len(news_list)}条新闻...")
    
    # 生成播客
    result = asyncio.run(generate_podcast(client, news_list))
    
    if result:
        print(f"\n✅ 播客生成成功！")
        print(f"   文件: {result['audio_file']}")
        print(f"   时长: {result['duration'] // 60}分{result['duration'] % 60}秒")
    else:
        print("❌ 播客生成失败")
        
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()