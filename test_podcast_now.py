"""
播客功能测试脚本
测试播客生成流程是否正常
"""

import sys
import os
from pathlib import Path

# Windows编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

import asyncio
from datetime import datetime
from podcast_generator_ffmpeg import generate_podcast
from openai import OpenAI

# 测试新闻数据
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

# 创建客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 测试播客生成
print("=" * 60)
print("🧪 播客功能测试")
print("=" * 60)

try:
    result = asyncio.run(generate_podcast(client, test_news))
    
    if result:
        print("\n" + "=" * 60)
        print("✅ 播客功能测试成功！")
        print("=" * 60)
        print(f"音频文件: {result['audio_file']}")
        print(f"脚本文件: {result['script_file']}")
        print(f"时长: {result['duration'] // 60}分{result['duration'] % 60}秒")
        
        # 验证文件存在
        if result['audio_file'].exists():
            size = result['audio_file'].stat().st_size
            print(f"文件大小: {size / 1024 / 1024:.2f} MB")
            print("✅ 音频文件已生成")
        else:
            print("❌ 音频文件不存在")
        
        if result['script_file'].exists():
            print("✅ 脚本文件已生成")
        else:
            print("❌ 脚本文件不存在")
    else:
        print("\n❌ 播客生成失败")
        sys.exit(1)

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)