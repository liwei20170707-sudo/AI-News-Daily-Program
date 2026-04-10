import asyncio
import edge_tts
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test():
    print("正在测试TTS...")
    try:
        communicate = edge_tts.Communicate("你好，这是测试", "zh-CN-XiaoxiaoNeural")
        await communicate.save("c:/Users/lw/WorkBuddy/Claw/ai_news_daily/podcasts/test.mp3")
        print("✅ TTS成功！")
    except Exception as e:
        print(f"❌ TTS失败: {e}")

asyncio.run(test())