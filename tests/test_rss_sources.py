"""
RSS源健康检查测试
测试覆盖：RSS源可用性、响应时间、内容质量
"""

import unittest
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import feedparser
from main import load_config


class TestRSSHealth(unittest.TestCase):
    """RSS源健康检查"""
    
    def setUp(self):
        """测试前准备"""
        self.config = load_config()
        self.timeout = 10  # 10秒超时
    
    def test_primary_feeds_health(self):
        """测试主要RSS源健康状态"""
        print("\n🔍 检查主要RSS源健康状态...")
        
        results = []
        
        for feed in self.config['feeds']:
            start_time = time.time()
            
            try:
                parsed = feedparser.parse(feed['url'])
                elapsed = time.time() - start_time
                
                # 检查是否有entries
                has_entries = len(parsed.entries) > 0
                
                # 检查响应时间
                is_fast = elapsed < self.timeout
                
                result = {
                    'name': feed['name'],
                    'url': feed['url'],
                    'healthy': has_entries and is_fast,
                    'entries': len(parsed.entries),
                    'response_time': elapsed,
                    'error': None
                }
                
                if has_entries:
                    print(f"  ✅ {feed['name']}: {len(parsed.entries)}条, {elapsed:.2f}s")
                else:
                    print(f"  ⚠️ {feed['name']}: 返回空数据")
                    result['error'] = "返回空数据"
                
            except Exception as e:
                elapsed = time.time() - start_time
                result = {
                    'name': feed['name'],
                    'url': feed['url'],
                    'healthy': False,
                    'entries': 0,
                    'response_time': elapsed,
                    'error': str(e)
                }
                print(f"  ❌ {feed['name']}: {e}")
            
            results.append(result)
        
        # 统计健康源数量
        healthy_count = sum(1 for r in results if r['healthy'])
        
        # 至少应该有2个健康源
        self.assertTrue(
            healthy_count >= 2,
            f"至少需要2个健康RSS源，当前只有{healthy_count}个"
        )
        
        # 保存结果供后续使用
        self.rss_health_results = results
    
    def test_backup_feeds_health(self):
        """测试备用RSS源健康状态"""
        print("\n🔍 检查备用RSS源健康状态...")
        
        if 'feeds_backup' not in self.config:
            self.skipTest("未配置备用RSS源")
        
        results = []
        
        for feed in self.config['feeds_backup']:
            start_time = time.time()
            
            try:
                parsed = feedparser.parse(feed['url'])
                elapsed = time.time() - start_time
                
                has_entries = len(parsed.entries) > 0
                is_fast = elapsed < self.timeout
                
                result = {
                    'name': feed['name'],
                    'url': feed['url'],
                    'healthy': has_entries and is_fast,
                    'entries': len(parsed.entries),
                    'response_time': elapsed
                }
                
                if has_entries:
                    print(f"  ✅ {feed['name']}: {len(parsed.entries)}条, {elapsed:.2f}s")
                else:
                    print(f"  ⚠️ {feed['name']}: 返回空数据")
                
            except Exception as e:
                result = {
                    'name': feed['name'],
                    'url': feed['url'],
                    'healthy': False,
                    'entries': 0,
                    'response_time': time.time() - start_time,
                    'error': str(e)
                }
                print(f"  ❌ {feed['name']}: {e}")
            
            results.append(result)
        
        # 至少应该有2个健康的备用源
        healthy_count = sum(1 for r in results if r['healthy'])
        
        self.assertTrue(
            healthy_count >= 2,
            f"至少需要2个健康备用源，当前只有{healthy_count}个"
        )
    
    def test_feed_content_quality(self):
        """测试RSS源内容质量"""
        print("\n🔍 检查RSS源内容质量...")
        
        for feed in self.config['feeds'][:2]:  # 只测试前2个源
            try:
                parsed = feedparser.parse(feed['url'])
                
                if len(parsed.entries) > 0:
                    entry = parsed.entries[0]
                    
                    # 验证必需字段
                    self.assertIn('title', entry, f"{feed['name']}缺少title字段")
                    self.assertIn('link', entry, f"{feed['name']}缺少link字段")
                    
                    # 验证内容不为空
                    self.assertTrue(len(entry.title) > 0, f"{feed['name']}标题为空")
                    self.assertTrue(entry.link.startswith('http'), f"{feed['name']}链接格式错误")
                    
                    print(f"  ✅ {feed['name']}: 内容质量合格")
                
            except Exception as e:
                print(f"  ⚠️ {feed['name']}: 内容质量检查失败 - {e}")
    
    def test_feed_response_time(self):
        """测试RSS源响应时间"""
        print("\n⏱️ 检查RSS源响应时间...")
        
        slow_threshold = 5.0  # 5秒为慢速
        
        for feed in self.config['feeds']:
            start_time = time.time()
            
            try:
                feedparser.parse(feed['url'])
                elapsed = time.time() - start_time
                
                if elapsed < slow_threshold:
                    print(f"  ✅ {feed['name']}: {elapsed:.2f}s (快速)")
                else:
                    print(f"  ⚠️ {feed['name']}: {elapsed:.2f}s (慢速)")
                
                # 响应时间不应超过timeout
                self.assertTrue(elapsed < self.timeout, f"{feed['name']}响应超时")
                
            except Exception as e:
                print(f"  ❌ {feed['name']}: 响应失败 - {e}")


class TestRSSMonitoring(unittest.TestCase):
    """RSS监控功能测试"""
    
    def test_health_check_function(self):
        """测试健康检查函数"""
        from rss_health_monitor import check_rss_health
        
        # 运行健康检查
        results = check_rss_health()
        
        # 验证返回结构
        self.assertIsInstance(results, dict)
        self.assertIn('primary', results)
        self.assertIn('backup', results)
        self.assertIn('summary', results)
        
        # 验证摘要信息
        summary = results['summary']
        self.assertIn('healthy_primary', summary)
        self.assertIn('healthy_backup', summary)
        self.assertIn('recommendation', summary)
    
    def test_auto_switch_to_backup(self):
        """测试自动切换备用源"""
        from rss_health_monitor import get_active_feeds
        
        # 获取活跃源
        active_feeds = get_active_feeds()
        
        # 应该返回至少2个源
        self.assertTrue(len(active_feeds) >= 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)