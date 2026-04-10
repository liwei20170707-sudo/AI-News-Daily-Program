"""
测试播客对话脚本生成（不需要FFmpeg）
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import os
from pathlib import Path
from openai import OpenAI

# 加载API Key
api_key = None
local_key_file = Path(__file__).parent / "dashscope_key.txt"
if local_key_file.exists():
    api_key = local_key_file.read_text(encoding='utf-8').strip()

if not api_key:
    print("❌ 请配置DASHSCOPE_API_KEY")
    sys.exit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 测试新闻
test_news = [
    {"title": "OpenAI发布GPT-5", "summary": "OpenAI发布新一代大模型GPT-5，性能提升显著，支持百万级上下文"},
    {"title": "苹果推出AI手机", "summary": "苹果发布搭载AI芯片的新款iPhone，支持本地大模型运行"},
    {"title": "特斯拉机器人量产", "summary": "特斯拉Optimus机器人开始量产，售价2万美元，预计年产量1万台"},
]

# 生成对话脚本
news_text = "\n".join([f"• {item['title']}：{item['summary']}" for item in test_news])

prompt = f"""你是一位播客脚本编剧。请将以下AI科技新闻改写成一段双人对话脚本。

角色设定：
- 主持人A（男声-云希）：幽默风趣，负责抛出话题和吐槽，语气轻松活泼
- 主持人B（女声-晓晓）：技术严谨，负责解释原理和补充，语气专业但不枯燥

要求：
1. 对话自然流畅，像两个朋友聊天
2. 每条新闻用2-3轮对话讲清楚核心价值
3. 适当加入过渡语和互动
4. 总字数控制在600-800字
5. 每句话前用"A："或"B："标明说话人
6. 直接输出对话内容，不要其他说明

新闻内容：
{news_text}

对话脚本："""

print("📝 正在生成对话脚本...\n")

resp = client.chat.completions.create(
    model="qwen-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.8,
    max_tokens=1500
)

script = resp.choices[0].message.content.strip()

print("=" * 50)
print("🎙️ 对话脚本生成成功！")
print("=" * 50)
print(script)
print("=" * 50)

# 保存脚本
output_file = Path(__file__).parent / "podcasts" / f"测试脚本_{os.getpid()}.txt"
output_file.parent.mkdir(exist_ok=True)
output_file.write_text(script, encoding='utf-8')
print(f"\n✅ 脚本已保存: {output_file}")