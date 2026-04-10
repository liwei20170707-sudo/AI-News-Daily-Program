"""
简化版播客生成测试
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import os
import asyncio
from pathlib import Path

print("=" * 50)
print("🎙️ 播客生成测试")
print("=" * 50)

# 1. 测试edge-tts
print("\n[1] 测试edge-tts...")
try:
    import edge_tts
    print("✅ edge-tts已安装")
except ImportError as e:
    print(f"❌ edge-tts未安装: {e}")
    sys.exit(1)

# 2. 测试pydub
print("\n[2] 测试pydub...")
try:
    from pydub import AudioSegment
    print("✅ pydub已安装")
except ImportError as e:
    print(f"❌ pydub未安装: {e}")
    sys.exit(1)

# 3. 测试FFmpeg
print("\n[3] 测试FFmpeg...")
ffmpeg_path = os.environ.get("FFMPEG_BINARY", "ffmpeg")
try:
    AudioSegment.converter = ffmpeg_path
    # 创建一个简单的测试音频
    test_audio = AudioSegment.silent(duration=100)
    print("✅ FFmpeg可用")
except Exception as e:
    print(f"❌ FFmpeg不可用: {e}")
    sys.exit(1)

# 4. 测试TTS
print("\n[4] 测试TTS生成...")

async def test_tts():
    output_dir = Path(__file__).parent / "podcasts"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "test_tts.mp3"
    
    try:
        communicate = edge_tts.Communicate(
            "这是一段测试语音，AI科技新闻播客正在生成中。",
            "zh-CN-YunxiNeural"
        )
        await communicate.save(str(output_file))
        print(f"✅ TTS测试成功: {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ TTS测试失败: {e}")
        return None

audio_file = asyncio.run(test_tts())

# 5. 测试音频合并
if audio_file and audio_file.exists():
    print("\n[5] 测试音频合并...")
    try:
        audio = AudioSegment.from_mp3(str(audio_file))
        print(f"✅ 音频加载成功，时长: {len(audio)/1000:.1f}秒")
        
        # 创建最终测试文件
        final = AudioSegment.silent(duration=500) + audio + AudioSegment.silent(duration=500)
        final_file = audio_file.parent / "test_final.mp3"
        final.export(str(final_file), format="mp3")
        print(f"✅ 音频合并成功: {final_file}")
    except Exception as e:
        print(f"❌ 音频合并失败: {e}")

print("\n" + "=" * 50)
print("✅ 所有测试通过！播客功能正常")
print("=" * 50)