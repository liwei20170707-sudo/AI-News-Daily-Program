"""测试播客模块导入"""
import sys
import traceback

try:
    print("开始导入播客模块...")
    from podcast_generator import generate_podcast
    print("✅ 播客模块导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    traceback.print_exc()