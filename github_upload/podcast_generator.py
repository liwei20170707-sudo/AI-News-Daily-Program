"""
AI科技新闻播客生成器 - 阶段二
功能：将新闻改写成双人对话脚本，生成分角色音频，合成完整播客MP3

依赖：
  pip install edge-tts pydub
  
系统要求：
  - FFmpeg（用于音频处理）
  - Windows: 下载 https://ffmpeg.org/download.html 并添加到PATH
"""

import os
import sys
import re
import json
import asyncio
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
VOICE_HOST_A = "zh-CN-YunxiNeural"    # 男声：云希（幽默风趣）
VOICE_HOST_B = "zh-CN-XiaoxiaoNeural"  # 女声：晓晓（技术严谨）

# 播客元信息
PODCAST_TITLE = "AI科技早报"
PODCAST_AUTHOR = "AI新闻编辑部"
PODCAST_DESCRIPTION = "每日AI科技热点，双人对话播报，让科技资讯听得懂"

# ========== 对话脚本生成 ==========
def generate_dialogue_script(client, news_list, model="qwen-turbo"):
    """将新闻列表改写成双人对话脚本"""
    
    # 准备新闻摘要
    news_text = "\n".join([
        f"• {item['title']}：{item.get('summary', item.get('desc', '')[:100])}"
        for item in news_list[:8]  # 限制8条新闻
    ])
    
    prompt = f"""你是一位播客脚本编剧。请将以下AI科技新闻改写成一段双人对话脚本。

角色设定：
- 主持人A（男声-云希）：幽默风趣，负责抛出话题和吐槽，语气轻松活泼
- 主持人B（女声-晓晓）：技术严谨，负责解释原理和补充，语气专业但不枯燥

要求：
1. 对话自然流畅，像两个朋友聊天
2. 每条新闻用2-3轮对话讲清楚核心价值
3. 适当加入过渡语和互动
4. 总字数控制在800-1000字
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
    pattern = r'([AB])[：:]\s*([^AB]+?)(?=[AB][：:]|$)'
    matches = re.findall(pattern, script_text, re.DOTALL)
    
    dialogues = []
    for speaker, sentence in matches:
        sentence = sentence.strip()
        if sentence:
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
        
        print(f"  🎙️ 生成音频 [{i+1}/{len(dialogues)}]: {speaker} - {sentence[:30]}...")
        
        success = await text_to_speech(sentence, voice, temp_file)
        if success:
            audio_files.append(temp_file)
        else:
            print(f"    ⚠️ 跳过该片段")
    
    return audio_files


def merge_audio_files(audio_files, output_file, pause_ms=500):
    """合并音频文件，添加停顿"""
    print(f"\n🎵 合并音频片段...")
    
    final_audio = AudioSegment.silent(duration=500)  # 开头静音
    
    for audio_file in audio_files:
        try:
            segment = AudioSegment.from_mp3(str(audio_file))
            final_audio += segment
            final_audio += AudioSegment.silent(duration=pause_ms)  # 句间停顿
        except Exception as e:
            print(f"  ⚠️ 无法加载音频 {audio_file}: {e}")
    
    final_audio += AudioSegment.silent(duration=1000)  # 结尾静音
    
    # 导出
    final_audio.export(str(output_file), format="mp3", bitrate="128k")
    print(f"  ✅ 播客音频已保存: {output_file}")
    
    return output_file


# ========== 播客RSS生成 ==========
def generate_podcast_rss(episode_file, episode_title, episode_description, 
                         pub_date, rss_file, base_url):
    """生成播客RSS XML文件"""
    
    file_size = os.path.getsize(episode_file)
    duration_ms = len(AudioSegment.from_mp3(str(episode_file)))
    duration_min = duration_ms // 60000
    duration_sec = (duration_ms % 60000) // 1000
    duration_str = f"{duration_min}:{duration_sec:02d}"
    
    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
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
        <title>{episode_title}</title>
        <description>{episode_description}</description>
        <pubDate>{pub_date}</pubDate>
        <enclosure url="{base_url}/{episode_file.name}" length="{file_size}" type="audio/mpeg"/>
        <itunes:duration>{duration_str}</itunes:duration>
        <itunes:summary>{episode_description}</itunes:summary>
    </item>
</channel>
</rss>"""
    
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
    
    # 1. 生成对话脚本
    print("\n📝 正在生成对话脚本...")
    script = generate_dialogue_script(client, news_list)
    
    if not script:
        print("❌ 对话脚本生成失败，退出")
        return None
    
    print("✅ 对话脚本生成成功")
    print(f"\n--- 脚本预览 ---\n{script[:500]}...\n")
    
    # 2. 解析对话
    dialogues = parse_dialogue_script(script)
    print(f"📊 共解析出 {len(dialogues)} 段对话")
    
    if not dialogues:
        print("❌ 未解析到有效对话，退出")
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
        "duration": len(AudioSegment.from_mp3(str(output_file))) // 1000
    }


# ========== 测试入口 ==========
if __name__ == "__main__":
    # 测试用的模拟新闻
    test_news = [
        {"title": "OpenAI发布GPT-5", "summary": "OpenAI发布新一代大模型GPT-5，性能提升显著"},
        {"title": "苹果推出AI手机", "summary": "苹果发布搭载AI芯片的新款iPhone，支持本地大模型"},
        {"title": "特斯拉机器人量产", "summary": "特斯拉Optimus机器人开始量产，售价2万美元"},
    ]
    
    # 需要配置API Key
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
    
    # 运行
    asyncio.run(generate_podcast(client, test_news))