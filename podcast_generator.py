"""
AI科技新闻播客生成器 - 阶段二
功能：将新闻改写成双人对话脚本，生成分角色音频，合成完整播客MP3

依赖：
  pip install edge-tts pydub
  
系统要求：
  - FFmpeg（用于音频处理）
  - GitHub Actions 自带 ffmpeg，无需额外安装
"""

import os
import sys
import re
import json
import asyncio
import argparse
from datetime import datetime
from pathlib import Path

# Windows编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

try:
    import edge_tts
except ImportError:
    print("❌ 缺少依赖: pip install edge-tts")
    sys.exit(1)

try:
    from pydub import AudioSegment
except ImportError:
    print("❌ 缺少依赖: pip install pydub")
    print("   还需要安装FFmpeg: https://ffmpeg.org/download.html")
    sys.exit(1)

from openai import OpenAI

# ========== 配置 ==========
PODCAST_DIR = Path(__file__).parent / "podcasts"
PODCAST_DIR.mkdir(exist_ok=True)

# 音色配置
VOICE_HOST_A = "zh-CN-YunxiNeural"      # 男声：云希（幽默风趣）
VOICE_HOST_B = "zh-CN-XiaoxiaoNeural"   # 女声：晓晓（技术严谨）

# 播客元信息
PODCAST_TITLE = "AI科技早报"
PODCAST_AUTHOR = "AI新闻编辑部"
PODCAST_DESCRIPTION = "每日AI科技热点，双人对话播报，让科技资讯听得懂"


# ========== 对话脚本生成 ==========
def generate_dialogue_script(client, news_list, model="qwen-turbo"):
    """将新闻列表改写成双人对话脚本"""
    
    # 准备新闻摘要（限制8条，控制播客时长）
    news_text = "\n".join([
        f"• {item.get('title', '未知标题')}：{item.get('summary', item.get('desc', ''))[:100]}"
        for item in news_list[:8]
    ])
    
    prompt = f"""你是一位播客脚本编剧。请将以下AI科技新闻改写成一段双人对话脚本。

角色设定：
- 主持人A（男声-云希）：幽默风趣，负责抛出话题和吐槽，语气轻松活泼
- 主持人B（女声-晓晓）：技术严谨，负责解释原理和补充，语气专业但不枯燥

要求：
1. 对话自然流畅，像两个朋友聊天
2. 每条新闻用2-3轮对话讲清楚核心价值
3. 适当加入过渡语和互动（如"说到这个...""没错！""哈哈"等）
4. 总字数控制在800-1200字，约3-5分钟时长
5. 每句话前用"A："或"B："标明说话人
6. 直接输出对话内容，不要其他说明

新闻内容：
{news_text}

对话脚本："""

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=2000
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ 对话脚本生成失败: {e}")
        return None


def parse_dialogue_script(script_text):
    """解析对话脚本，返回[(说话人, 台词)]列表"""
    # 匹配 A：xxx 或 B：xxx 格式
    pattern = r'([AB])[：:]\s*([^AB]+?)(?=[AB][：:]|$)'
    matches = re.findall(pattern, script_text, re.DOTALL)
    
    dialogues = []
    for speaker, sentence in matches:
        sentence = sentence.strip()
        if sentence and len(sentence) > 1:
            dialogues.append((speaker, sentence))
    
    return dialogues


# ========== 音频生成 ==========
async def text_to_speech(text, voice, output_file):
    """使用edge-tts生成单段语音"""
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(output_file))
        return True
    except Exception as e:
        print(f"❌ TTS生成失败: {e}")
        return False


async def generate_dialogue_audio(dialogues, output_dir):
    """生成所有对话音频片段"""
    audio_files = []
    
    for i, (speaker, sentence) in enumerate(dialogues):
        voice = VOICE_HOST_A if speaker == 'A' else VOICE_HOST_B
        temp_file = output_dir / f"segment_{i:03d}_{speaker}.mp3"
        
        print(f"  🎙️ 生成音频 [{i+1}/{len(dialogues)}]: {speaker} - {sentence[:35]}...")
        
        success = await text_to_speech(sentence, voice, temp_file)
        if success:
            audio_files.append(temp_file)
        else:
            print(f"    ⚠️ 跳过该片段")
    
    return audio_files


def merge_audio_files(audio_files, output_file, pause_ms=500):
    """合并音频文件，添加停顿"""
    print(f"\n🎵 合并音频片段...")
    
    if not audio_files:
        print("❌ 没有音频文件可合并")
        return None
    
    final_audio = AudioSegment.silent(duration=500)  # 开头静音
    
    for i, audio_file in enumerate(audio_files):
        try:
            segment = AudioSegment.from_mp3(str(audio_file))
            final_audio += segment
            final_audio += AudioSegment.silent(duration=pause_ms)  # 句间停顿
            print(f"  ✅ 已合并: {audio_file.name}")
        except Exception as e:
            print(f"  ⚠️ 无法加载音频 {audio_file.name}: {e}")
    
    final_audio += AudioSegment.silent(duration=1000)  # 结尾静音
    
    # 导出
    final_audio.export(str(output_file), format="mp3", bitrate="128k")
    print(f"\n  ✅ 播客音频已保存: {output_file}")
    print(f"  📊 总时长: {len(final_audio) // 1000} 秒")
    
    return output_file


# ========== 播客RSS生成 ==========
def generate_podcast_rss(audio_file, date_str, rss_file, base_url):
    """生成播客RSS XML文件"""
    
    file_size = audio_file.stat().st_size
    
    try:
        audio_seg = AudioSegment.from_mp3(str(audio_file))
        duration_sec = len(audio_seg) // 1000
        duration_min = duration_sec // 60
        duration_sec_rem = duration_sec % 60
        duration_str = f"{duration_min}:{duration_sec_rem:02d}"
    except:
        duration_str = "5:00"
    
    pub_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0800')
    
    rss_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
    <title>{PODCAST_TITLE}</title>
    <link>{base_url}</link>
    <language>zh-CN</language>
    <author>{PODCAST_AUTHOR}</author>
    <description>{PODCAST_DESCRIPTION}</description>
    <itunes:author>{PODCAST_AUTHOR}</itunes:author>
    <itunes:summary>{PODCAST_DESCRIPTION}</itunes:summary>
    <itunes:category text="Technology"/>
    <itunes:explicit>false</itunes:explicit>
    
    <item>
        <title>{PODCAST_TITLE} - {date_str}</title>
        <description>今日AI科技新闻精选，双人对话播报</description>
        <pubDate>{pub_date}</pubDate>
        <enclosure url="{base_url}/{audio_file.name}" length="{file_size}" type="audio/mpeg"/>
        <itunes:duration>{duration_str}</itunes:duration>
        <itunes:summary>今日AI科技新闻精选，双人对话播报</itunes:summary>
    </item>
</channel>
</rss>'''
    
    with open(rss_file, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    
    print(f"  ✅ RSS文件已生成: {rss_file}")
    return rss_file


# ========== 主流程 ==========
async def generate_podcast(client, news_list, date_str=None):
    """生成完整播客的主流程"""
    
    if date_str is None:
        date_str = datetime.now().strftime('%Y年%m月%d日')
    
    print("=" * 50)
    print("🎙️ AI科技新闻播客生成器")
    print("=" * 50)
    print(f"📅 日期: {date_str}")
    print(f"📰 新闻数量: {len(news_list)} 条")
    
    # 1. 生成对话脚本
    print("\n📝 正在生成对话脚本...")
    script = generate_dialogue_script(client, news_list)
    
    if not script:
        print("❌ 对话脚本生成失败，退出")
        return None
    
    print("✅ 对话脚本生成成功")
    
    # 显示脚本预览
    preview = script[:400].replace('\n', ' ')
    print(f"\n--- 脚本预览 ---\n{preview}...\n")
    
    # 2. 解析对话
    dialogues = parse_dialogue_script(script)
    print(f"📊 共解析出 {len(dialogues)} 段对话")
    
    if not dialogues:
        print("❌ 未解析到有效对话，退出")
        # 保存脚本供调试
        debug_file = PODCAST_DIR / f"debug_script_{datetime.now().strftime('%Y%m%d')}.txt"
        debug_file.write_text(script, encoding='utf-8')
        print(f"💡 脚本已保存到: {debug_file}")
        return None
    
    # 3. 创建临时目录
    temp_dir = PODCAST_DIR / f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    temp_dir.mkdir(exist_ok=True)
    
    # 4. 生成音频片段
    print("\n🎙️ 正在生成音频片段...")
    audio_files = await generate_dialogue_audio(dialogues, temp_dir)
    
    if not audio_files:
        print("❌ 音频生成失败，退出")
        return None
    
    # 5. 合并音频
    output_file = PODCAST_DIR / f"AI科技早报_{datetime.now().strftime('%Y%m%d')}.mp3"
    merge_audio_files(audio_files, output_file)
    
    # 6. 清理临时文件
    for f in temp_dir.iterdir():
        f.unlink()
    temp_dir.rmdir()
    
    # 7. 保存脚本
    script_file = PODCAST_DIR / f"脚本_{datetime.now().strftime('%Y%m%d')}.txt"
    script_file.write_text(script, encoding='utf-8')
    
    print("\n" + "=" * 50)
    print("✅ 播客生成完成！")
    print(f"   音频文件: {output_file}")
    print(f"   脚本文件: {script_file}")
    print("=" * 50)
    
    return {
        "audio_file": output_file,
        "script_file": script_file,
        "script": script,
    }


# ========== 加载新闻数据 ==========
def load_news_from_reports():
    """从reports目录加载新闻数据"""
    reports_dir = Path(__file__).parent / "reports"
    if not reports_dir.exists():
        print("❌ reports目录不存在")
        return None
    
    # 查找最新的JSON报告
    json_files = list(reports_dir.glob("*.json"))
    if not json_files:
        print("❌ 未找到JSON报告文件")
        return None
    
    latest_report = max(json_files, key=lambda f: f.stat().st_mtime)
    print(f"📄 使用报告: {latest_report.name}")
    
    try:
        with open(latest_report, 'r', encoding='utf-8') as f:
            data = json.load(f)
            news_list = data.get('news', [])
            print(f"📰 加载了 {len(news_list)} 条新闻")
            return news_list
    except Exception as e:
        print(f"❌ 读取报告失败: {e}")
        return None


def get_test_news():
    """获取测试新闻数据"""
    return [
        {"title": "阿里发布Qwen3.6-Plus大模型", "summary": "1.4万亿参数，成为全球最大AI聚合平台，性能超越GPT-4"},
        {"title": "特斯拉全球超级充电桩突破8万根", "summary": "中国内地已有超1.2万根，充电网络持续扩张"},
        {"title": "英特尔Nova Lake-S处理器规格曝光", "summary": "44核配288MB缓存，性能提升显著"},
        {"title": "OpenAI考虑收购AI芯片公司", "summary": "加强自研芯片能力，减少对英伟达依赖"},
        {"title": "谷歌DeepMind发布新一代AlphaFold", "summary": "蛋白质预测准确率再创新高"},
        {"title": "中国空间站将开展AI科学实验", "summary": "利用大模型辅助太空数据分析"},
    ]


# ========== 命令行入口 ==========
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI科技新闻播客生成器')
    parser.add_argument('--from-reports', action='store_true', 
                       help='从reports目录读取新闻数据')
    parser.add_argument('--test', action='store_true', 
                       help='使用测试数据运行')
    
    args = parser.parse_args()
    
    # 获取API Key
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    
    # 如果环境变量没有，尝试从本地文件读取（仅本地测试）
    if not api_key:
        local_key_file = Path(__file__).parent / "dashscope_key.txt"
        if local_key_file.exists():
            api_key = local_key_file.read_text(encoding='utf-8').strip()
            print("📁 从本地文件读取API Key")
    
    if not api_key:
        print("❌ 请配置DASHSCOPE_API_KEY环境变量")
        print("   GitHub: Settings -> Secrets -> DASHSCOPE_API_KEY")
        print("   本地: set DASHSCOPE_API_KEY=你的密钥")
        sys.exit(1)
    
    # 初始化OpenAI客户端（阿里云兼容模式）
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    news_list = None
    
    if args.test:
        print("🧪 测试模式，使用模拟数据")
        news_list = get_test_news()
    elif args.from_reports:
        print("📂 从reports目录加载新闻")
        news_list = load_news_from_reports()
        if not news_list:
            print("⚠️ 无法从报告加载，使用测试数据")
            news_list = get_test_news()
    else:
        # 默认使用测试数据
        print("📋 默认模式，使用测试数据（如需从报告加载请加 --from-reports）")
        news_list = get_test_news()
    
    # 运行播客生成
    asyncio.run(generate_podcast(client, news_list))
