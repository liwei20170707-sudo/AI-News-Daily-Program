"""
AI科技新闻系统 - 核心模块测试
测试覆盖：RSS抓取、AI摘要、推送渠道
"""

import unittest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import feedparser
from unittest.mock import Mock, patch, MagicMock
from main import (
    load_config,
    fetch_rss_feed,
    fetch_all_feeds,
    summarize_news,
    build_markdown_report,
    push_dingtalk,
    push_serverchan,
    push_smtp_email
)


class TestConfigLoading(unittest.TestCase):
    """配置加载测试"""
    
    def test_config_file_exists(self):
        """测试配置文件是否存在"""
        config_file = Path(__file__).parent.parent / "config.json"
        self.assertTrue(config_file.exists(), "配置文件必须存在")
    
    def test_config_structure(self):
        """测试配置文件结构"""
        config = load_config()
        
        # 必需字段
        self.assertIn('feeds', config)
        self.assertIn('push', config)
        self.assertIn('dashscope', config)
        
        # feeds结构
        self.assertTrue(len(config['feeds']) > 0)
        for feed in config['feeds']:
            self.assertIn('name', feed)
            self.assertIn('url', feed)
            self.assertIn('max_items', feed)
        
        # push结构
        self.assertIn('emails', config['push'])
        self.assertTrue(len(config['push']['emails']) > 0)
    
    def test_backup_feeds_configured(self):
        """测试备用RSS源已配置"""
        config = load_config()
        self.assertIn('feeds_backup', config)
        self.assertTrue(len(config['feeds_backup']) >= 3, "至少需要3个备用RSS源")


class TestRSSFetching(unittest.TestCase):
    """RSS抓取测试"""
    
    def test_fetch_single_feed(self):
        """测试单个RSS源抓取"""
        # 使用稳定的RSS源测试
        test_url = "https://www.ithome.com/rss"
        items = fetch_rss_feed(test_url, max_items=5)
        
        # 验证返回结构
        self.assertTrue(len(items) > 0, "应该返回至少1条新闻")
        
        for item in items:
            self.assertIn('title', item)
            self.assertIn('link', item)
            self.assertIn('desc', item)
            
            # 验证字段不为空
            self.assertTrue(len(item['title']) > 0)
            self.assertTrue(item['link'].startswith('http'))
    
    def test_fetch_invalid_url(self):
        """测试无效RSS源处理"""
        invalid_url = "https://invalid-url.com/rss"
        items = fetch_rss_feed(invalid_url)
        
        # 应该返回空列表，不应抛出异常
        self.assertEqual(len(items), 0)
    
    def test_fetch_all_feeds(self):
        """测试所有RSS源抓取"""
        config = load_config()
        news_list = fetch_all_feeds(config)
        
        # 验证总数限制
        self.assertTrue(len(news_list) <= 40)
        
        # 验证去重
        titles = [item['title'][:50] for item in news_list]
        self.assertEqual(len(titles), len(set(titles)), "标题应该去重")
    
    def test_fetch_with_backup(self):
        """测试备用源切换"""
        config = load_config()
        
        # 使用备用源
        news_list = fetch_all_feeds(config, use_backup=True)
        
        self.assertTrue(len(news_list) > 0, "备用源应该能返回新闻")


class TestAISummary(unittest.TestCase):
    """AI摘要测试"""
    
    def test_summary_with_mock_client(self):
        """测试摘要生成（模拟客户端）"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "这是一条关于AI技术的测试摘要"
        
        mock_client.chat.completions.create = Mock(return_value=mock_response)
        
        title = "测试新闻标题"
        snippet = "这是测试新闻内容，用于验证摘要生成功能"
        
        summary = summarize_news(mock_client, title, snippet)
        
        # 验证返回摘要
        self.assertTrue(len(summary) > 0)
        self.assertIsInstance(summary, str)
    
    def test_summary_without_client(self):
        """测试无客户端时的降级处理"""
        title = "测试新闻标题"
        snippet = "这是测试新闻内容"
        
        summary = summarize_news(None, title, snippet)
        
        # 应该返回原始片段的前80字
        self.assertEqual(summary, snippet[:80])
    
    def test_summary_empty_snippet(self):
        """测试空内容处理"""
        summary = summarize_news(None, "标题", "")
        
        self.assertEqual(summary, "暂无摘要")


class TestReportGeneration(unittest.TestCase):
    """报告生成测试"""
    
    def test_markdown_report_structure(self):
        """测试Markdown报告结构"""
        test_news = [
            {
                'title': '测试新闻1',
                'link': 'https://test.com/1',
                'desc': '测试内容1',
                'summary': '测试摘要1',
                'source': '测试源'
            },
            {
                'title': '测试新闻2',
                'link': 'https://test.com/2',
                'desc': '测试内容2',
                'summary': '测试摘要2',
                'source': '测试源'
            }
        ]
        
        report = build_markdown_report(test_news, "2026年04月11日")
        
        # 验证必需元素
        self.assertIn('# 🤖 AI科技早报', report)
        self.assertIn('2026年04月11日', report)
        self.assertIn('测试新闻1', report)
        self.assertIn('测试新闻2', report)
        self.assertIn('[阅读原文]', report)
    
    def test_report_with_empty_news(self):
        """测试空新闻列表处理"""
        report = build_markdown_report([], "2026年04月11日")
        
        # 应该生成空报告，不抛出异常
        self.assertIn('共 0 条精选', report)


class TestPushChannels(unittest.TestCase):
    """推送渠道测试"""
    
    @patch('urllib.request.urlopen')
    def test_dingtalk_push_success(self, mock_urlopen):
        """测试钉钉推送成功"""
        mock_response = Mock()
        mock_response.read = Mock(return_value=b'{"errcode":0}')
        mock_urlopen.return_value = mock_response
        
        config = {
            'push': {
                'dingtalk_webhook': 'https://test-webhook.com'
            }
        }
        
        result = push_dingtalk(config, "测试标题", "测试内容")
        self.assertTrue(result)
    
    @patch('urllib.request.urlopen')
    def test_dingtalk_push_failure(self, mock_urlopen):
        """测试钉钉推送失败"""
        mock_response = Mock()
        mock_response.read = Mock(return_value=b'{"errcode":1}')
        mock_urlopen.return_value = mock_response
        
        config = {
            'push': {
                'dingtalk_webhook': 'https://test-webhook.com'
            }
        }
        
        result = push_dingtalk(config, "测试标题", "测试内容")
        self.assertFalse(result)
    
    @patch('urllib.request.urlopen')
    def test_serverchan_push_success(self, mock_urlopen):
        """测试Server酱推送成功"""
        mock_response = Mock()
        mock_response.read = Mock(return_value=b'{"code":0}')
        mock_urlopen.return_value = mock_response
        
        config = {
            'push': {
                'serverchan_key': 'test_key'
            }
        }
        
        result = push_serverchan(config, "测试标题", "测试内容")
        self.assertTrue(result)
    
    def test_push_without_config(self):
        """测试无配置时的处理"""
        config = {'push': {}}
        
        result = push_dingtalk(config, "测试", "内容")
        self.assertFalse(result)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow_mock(self):
        """测试完整流程（模拟）"""
        config = load_config()
        
        # 验证配置加载
        self.assertIsNotNone(config)
        
        # 验证RSS源配置
        self.assertTrue(len(config['feeds']) > 0)
        
        # 集成测试：验证推送配置
        self.assertIn('emails', config['push'])


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)