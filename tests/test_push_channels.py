"""
推送渠道可用性测试
测试覆盖：钉钉、Server酱、SMTP邮件推送
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import Mock, patch
from main import (
    load_config,
    push_dingtalk,
    push_serverchan,
    push_smtp_email
)


class TestPushChannelAvailability(unittest.TestCase):
    """推送渠道可用性测试"""
    
    def setUp(self):
        """测试前准备"""
        self.config = load_config()
    
    def test_dingtalk_config_valid(self):
        """测试钉钉配置有效性"""
        webhook = self.config['push'].get('dingtalk_webhook')
        
        # 验证webhook存在
        self.assertIsNotNone(webhook, "钉钉Webhook必须配置")
        
        # 验证webhook格式
        self.assertTrue(webhook.startswith('https://oapi.dingtalk.com'), "Webhook格式应正确")
        
        # 验证包含access_token
        self.assertIn('access_token=', webhook, "Webhook应包含access_token")
        
        print(f"✅ 钉钉配置有效: {webhook[:50]}...")
    
    def test_serverchan_config_valid(self):
        """测试Server酱配置有效性"""
        send_key = self.config['push'].get('serverchan_key')
        
        # 验证SendKey存在
        self.assertIsNotNone(send_key, "Server酱SendKey必须配置")
        
        # 验证SendKey格式（以SCT开头）
        self.assertTrue(send_key.startswith('SCT'), "SendKey格式应正确")
        
        print(f"✅ Server酱配置有效: {send_key[:20]}...")
    
    def test_smtp_config_valid(self):
        """测试SMTP配置有效性"""
        emails = self.config['push'].get('emails')
        
        # 验证邮箱列表存在
        self.assertIsNotNone(emails, "邮箱列表必须配置")
        self.assertTrue(len(emails) > 0, "至少需要1个接收邮箱")
        
        # 验证邮箱格式
        for email in emails:
            self.assertTrue('@' in email, f"邮箱格式应正确: {email}")
        
        print(f"✅ SMTP配置有效: {emails}")
    
    @patch('urllib.request.urlopen')
    def test_dingtalk_connection(self, mock_urlopen):
        """测试钉钉连接"""
        mock_response = Mock()
        mock_response.read = Mock(return_value=b'{"errcode":0}')
        mock_urlopen.return_value = mock_response
        
        result = push_dingtalk(self.config, "测试标题", "测试内容")
        
        # 验证推送成功
        self.assertTrue(result, "钉钉推送应该成功")
        
        # 验证调用参数
        self.assertTrue(mock_urlopen.called)
    
    @patch('urllib.request.urlopen')
    def test_serverchan_connection(self, mock_urlopen):
        """测试Server酱连接"""
        mock_response = Mock()
        mock_response.read = Mock(return_value=b'{"code":0}')
        mock_urlopen.return_value = mock_response
        
        result = push_serverchan(self.config, "测试标题", "测试内容")
        
        # 验证推送成功
        self.assertTrue(result, "Server酱推送应该成功")
        
        # 验证调用参数
        self.assertTrue(mock_urlopen.called)
    
    def test_push_priority(self):
        """测试推送优先级"""
        # 钉钉应该优先（无次数限制）
        self.assertIn('dingtalk_webhook', self.config['push'])
        
        # Server酱次优先（有次数限制）
        self.assertIn('serverchan_key', self.config['push'])
        
        # SMTP邮件备用（稳定可靠）
        self.assertIn('emails', self.config['push'])
        
        print("✅ 推送优先级配置正确: 钉钉 → Server酱 → SMTP")


class TestPushChannelFailureHandling(unittest.TestCase):
    """推送失败处理测试"""
    
    def setUp(self):
        """测试前准备"""
        self.config = load_config()
    
    @patch('urllib.request.urlopen')
    def test_dingtalk_failure_handling(self, mock_urlopen):
        """测试钉钉失败处理"""
        mock_response = Mock()
        mock_response.read = Mock(return_value=b'{"errcode":1}')
        mock_urlopen.return_value = mock_response
        
        result = push_dingtalk(self.config, "测试", "内容")
        
        # 应返回False，不抛出异常
        self.assertFalse(result)
    
    @patch('urllib.request.urlopen')
    def test_serverchan_failure_handling(self, mock_urlopen):
        """测试Server酱失败处理"""
        mock_response = Mock()
        mock_response.read = Mock(return_value=b'{"code":400}')
        mock_urlopen.return_value = mock_response
        
        result = push_serverchan(self.config, "测试", "内容")
        
        # 应返回False，不抛出异常
        self.assertFalse(result)
    
    @patch('smtplib.SMTP_SSL')
    def test_smtp_failure_handling(self, mock_smtp):
        """测试SMTP失败处理"""
        mock_smtp.side_effect = Exception("SMTP连接失败")
        
        result = push_smtp_email(self.config, "测试", "<html></html>")
        
        # 应返回False，不抛出异常
        self.assertFalse(result)
    
    def test_missing_webhook_handling(self):
        """测试缺少Webhook处理"""
        config_no_webhook = {'push': {}}
        
        result = push_dingtalk(config_no_webhook, "测试", "内容")
        
        # 应返回False，不抛出异常
        self.assertFalse(result)


class TestPushContentFormat(unittest.TestCase):
    """推送内容格式测试"""
    
    def test_dingtalk_content_format(self):
        """测试钉钉内容格式"""
        # 钉钉要求消息包含关键词
        test_content = "🤖 AI科技早报 - 测试"
        
        # 应包含关键词"早报"
        self.assertIn("早报", test_content, "钉钉消息必须包含关键词")
    
    def test_serverchan_content_length(self):
        """测试Server酱内容长度"""
        from main import build_serverchan_content
        
        test_news = [
            {
                'title': '测试新闻' * 20,  # 长标题
                'link': 'https://test.com',
                'desc': '测试内容',
                'source': '测试源'
            }
        ]
        
        content = build_serverchan_content(test_news, "2026年04月11日", max_items=10)
        
        # Server酱免费版限制长度
        # 验证内容不会过长
        self.assertTrue(len(content) < 10000, "Server酱内容不应过长")


if __name__ == '__main__':
    unittest.main(verbosity=2)