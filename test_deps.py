"""测试依赖"""
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

print("测试 edge-tts...")
try:
    import edge_tts
    print("✅ edge-tts 导入成功")
except Exception as e:
    print(f"❌ edge-tts 导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试 pydub...")
try:
    from pydub import AudioSegment
    print("✅ pydub 导入成功")
    print("测试 AudioSegment...")
    silence = AudioSegment.silent(duration=100)
    print(f"✅ AudioSegment 工作正常，长度: {len(silence)}ms")
except Exception as e:
    print(f"❌ pydub 导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试 openai...")
try:
    from openai import OpenAI
    print("✅ openai 导入成功")
except Exception as e:
    print(f"❌ openai 导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n所有依赖测试完成")