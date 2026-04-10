"""
测试SMTP邮件发送
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from datetime import datetime
from pathlib import Path

# SMTP配置
smtp_host = "smtp.126.com"
smtp_port = 465
smtp_user = "david_lw2012@126.com"
smtp_pass = "YYVBJ4F8cGBrGCXQ"

# 收件人
emails = ["liwei0@huawei.com"]

# 读取今日报告
report_file = Path(__file__).parent / "reports" / f"AI早报_{datetime.now().strftime('%Y%m%d')}.md"
if report_file.exists():
    content = report_file.read_text(encoding='utf-8')
else:
    content = "测试邮件内容"

# 构建邮件
title = f"🤖 AI科技早报 - {datetime.now().strftime('%Y年%m月%d日')}"

msg = MIMEMultipart('alternative')
msg['Subject'] = title
msg['From'] = f"AI助手 <{smtp_user}>"
msg['To'] = ", ".join(emails)

# 纯文本版本
text_part = MIMEText(content, 'plain', 'utf-8')
msg.attach(text_part)

# HTML版本
html_content = f"""
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: sans-serif; padding: 20px;">
<h1>🤖 AI科技早报</h1>
<p>📅 {datetime.now().strftime('%Y年%m月%d日')}</p>
<pre style="white-space: pre-wrap; font-family: monospace;">{content}</pre>
</body>
</html>
"""
html_part = MIMEText(html_content, 'html', 'utf-8')
msg.attach(html_part)

# 发送邮件
print("📤 正在发送邮件...")
print(f"   收件人: {emails}")

try:
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, emails, msg.as_string())
    
    print("✅ 邮件发送成功！")
    print("   请检查邮箱收件箱")
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")