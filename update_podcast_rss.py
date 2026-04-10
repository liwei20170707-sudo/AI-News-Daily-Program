"""
播客RSS更新脚本
功能：将新生成的播客添加到podcast.xml RSS订阅文件

使用方式：
  python update_podcast_rss.py --audio AUDIO_FILE --script SCRIPT_FILE
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import subprocess

# Windows编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# ========== 配置 ==========

PODCAST_DIR = Path(__file__).parent / "podcasts"
RSS_FILE = Path(__file__).parent / "podcast.xml"

PODCAST_TITLE = "AI科技早报"
PODCAST_AUTHOR = "AI新闻编辑部"
PODCAST_DESCRIPTION = "每日AI科技热点，双人对话播报，让科技资讯听得懂"

BASE_URL = "https://liwei20170707-sudo.github.io/AI-News-Daily-Program"


# ========== RSS更新 ==========

def get_audio_duration(audio_file):
    """使用ffprobe获取音频时长"""
    result = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(audio_file)
    ], capture_output=True, text=True, check=True)
    
    duration_sec = float(result.stdout.strip())
    duration_min = int(duration_sec // 60)
    duration_sec_rem = int(duration_sec % 60)
    
    return f"{duration_min}:{duration_sec_rem:02d}"


def extract_description_from_script(script_file):
    """从脚本文件提取播客描述"""
    if not script_file.exists():
        return "AI科技早报，双人对话播报"
    
    content = script_file.read_text(encoding='utf-8')
    
    # 提取前3段对话作为描述
    lines = content.strip().split('\n')
    description_lines = []
    
    for line in lines[:6]:
        if line.strip():
            description_lines.append(line.strip())
    
    if description_lines:
        return ' '.join(description_lines)[:200]
    
    return "AI科技早报，双人对话播报"


def update_podcast_rss(audio_file, script_file=None):
    """更新podcast.xml RSS文件"""
    
    print("=" * 60)
    print("📝 更新播客RSS订阅")
    print("=" * 60)
    
    # 检查音频文件
    if not audio_file.exists():
        print(f"❌ 音频文件不存在: {audio_file}")
        return False
    
    # 获取音频信息
    file_size = audio_file.stat().st_size
    duration = get_audio_duration(audio_file)
    
    # 提取日期
    date_str = audio_file.stem.split('_')[-1]  # AI科技早报_20260411 -> 20260411
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    date_formatted = date_obj.strftime('%Y年%m月%d日')
    pub_date = date_obj.strftime('%a, %d %b %Y 07:30:00 +0800')
    
    # 提取描述
    if script_file and script_file.exists():
        description = extract_description_from_script(script_file)
    else:
        description = f"AI科技早报 - {date_formatted}"
    
    print(f"  📅 日期: {date_formatted}")
    print(f"  ⏱️  时长: {duration}")
    print(f"  📦 大小: {file_size / 1024 / 1024:.2f} MB")
    print(f"  📝 描述: {description[:80]}...")
    
    # 读取现有RSS
    if RSS_FILE.exists():
        rss_content = RSS_FILE.read_text(encoding='utf-8')
    else:
        # 创建新的RSS文件
        rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
    <title>{PODCAST_TITLE}</title>
    <link>{BASE_URL}/</link>
    <language>zh-CN</language>
    <author>{PODCAST_AUTHOR}</author>
    <description>{PODCAST_DESCRIPTION}</description>
    <itunes:author>{PODCAST_AUTHOR}</itunes:author>
    <itunes:summary>{PODCAST_DESCRIPTION}</itunes:summary>
    <itunes:category text="Technology"/>
    <itunes:explicit>false</itunes:explicit>
    
</channel>
</rss>"""
    
    # 创建新条目
    new_item = f"""    <item>
        <title>AI科技早报 - {date_formatted}</title>
        <description>{description}</description>
        <pubDate>{pub_date}</pubDate>
        <enclosure url="{BASE_URL}/podcasts/{audio_file.name}" length="{file_size}" type="audio/mpeg"/>
        <itunes:duration>{duration}</itunes:duration>
        <itunes:summary>{description}</itunes:summary>
    </item>
"""
    
    # 插入新条目（在第一个item之前）
    if '<item>' in rss_content:
        # 找到第一个item的位置
        insert_pos = rss_content.find('<item>')
        updated_rss = rss_content[:insert_pos] + new_item + rss_content[insert_pos:]
    else:
        # 没有item，插入到channel结束标签前
        insert_pos = rss_content.find('</channel>')
        updated_rss = rss_content[:insert_pos] + new_item + rss_content[insert_pos:]
    
    # 保存RSS文件
    RSS_FILE.write_text(updated_rss, encoding='utf-8')
    
    print(f"\n✅ RSS文件已更新: {RSS_FILE}")
    
    return True


# ========== 主流程 ==========

def main():
    """主流程"""
    
    # 解析参数
    audio_file = None
    script_file = None
    
    args = sys.argv[1:]
    
    if '--audio' in args:
        idx = args.index('--audio')
        if idx + 1 < len(args):
            audio_file = Path(args[idx + 1])
    
    if '--script' in args:
        idx = args.index('--script')
        if idx + 1 < len(args):
            script_file = Path(args[idx + 1])
    
    # 如果没有指定，使用今天的文件
    if not audio_file:
        today = datetime.now().strftime('%Y%m%d')
        audio_file = PODCAST_DIR / f"AI科技早报_{today}.mp3"
        
        if script_file is None:
            script_file = PODCAST_DIR / f"脚本_{today}.txt"
    
    # 更新RSS
    success = update_podcast_rss(audio_file, script_file)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ RSS更新完成！")
        print("=" * 60)
        print(f"订阅地址: {BASE_URL}/podcast.xml")
    else:
        print("\n❌ RSS更新失败")
        sys.exit(1)


if __name__ == "__main__":
    main()