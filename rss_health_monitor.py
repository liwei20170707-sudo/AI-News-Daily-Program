"""
RSS源健康监控脚本 - systematic-debugging
自动检测RSS源健康状态，失效时切换备用源

使用方式：
  python rss_health_monitor.py [--check] [--switch] [--report]
  
参数：
  --check     检查RSS源健康状态
  --switch    自动切换到备用源
  --report    生成健康报告
"""

import sys
import os

# Windows控制台编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import json
import time
import feedparser
from pathlib import Path
from datetime import datetime


class RSSHealthMonitor:
    """RSS源健康监控器"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.config_file = self.project_dir / "config.json"
        self.health_cache = self.project_dir / ".workbuddy" / "rss_health_cache.json"
        
        # 加载配置
        with open(self.config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 健康检查阈值
        self.timeout = 10  # 10秒超时
        self.min_entries = 1  # 至少1条新闻
        self.max_failures = 3  # 连续失败3次标记为不健康
    
    def check_rss_health(self):
        """检查RSS源健康状态"""
        print("=" * 60)
        print("🔍 RSS源健康检查")
        print("=" * 60)
        
        results = {
            'primary': [],
            'backup': [],
            'summary': {
                'timestamp': datetime.now().isoformat(),
                'healthy_primary': 0,
                'healthy_backup': 0,
                'recommendation': None
            }
        }
        
        # 检查主要源
        print("\n📡 主要RSS源:")
        for feed in self.config['feeds']:
            result = self._check_single_feed(feed)
            results['primary'].append(result)
            
            if result['healthy']:
                results['summary']['healthy_primary'] += 1
        
        # 检查备用源
        print("\n🔄 备用RSS源:")
        if 'feeds_backup' in self.config:
            for feed in self.config['feeds_backup']:
                result = self._check_single_feed(feed)
                results['backup'].append(result)
                
                if result['healthy']:
                    results['summary']['healthy_backup'] += 1
        
        # 生成建议
        self._generate_recommendation(results)
        
        # 保存结果
        self._save_health_cache(results)
        
        return results
    
    def _check_single_feed(self, feed):
        """检查单个RSS源"""
        start_time = time.time()
        
        result = {
            'name': feed['name'],
            'url': feed['url'],
            'healthy': False,
            'entries': 0,
            'response_time': 0,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            parsed = feedparser.parse(feed['url'])
            elapsed = time.time() - start_time
            
            result['entries'] = len(parsed.entries)
            result['response_time'] = elapsed
            
            # 判断健康状态
            has_entries = len(parsed.entries) >= self.min_entries
            is_fast = elapsed < self.timeout
            
            result['healthy'] = has_entries and is_fast
            
            if result['healthy']:
                print(f"  ✅ {feed['name']}: {result['entries']}条, {elapsed:.2f}s")
            else:
                if not has_entries:
                    result['error'] = "返回空数据"
                    print(f"  ⚠️ {feed['name']}: 返回空数据")
                elif not is_fast:
                    result['error'] = "响应超时"
                    print(f"  ⚠️ {feed['name']}: 响应超时 ({elapsed:.2f}s)")
        
        except Exception as e:
            elapsed = time.time() - start_time
            result['response_time'] = elapsed
            result['error'] = str(e)
            print(f"  ❌ {feed['name']}: {e}")
        
        return result
    
    def _generate_recommendation(self, results):
        """生成切换建议"""
        healthy_primary = results['summary']['healthy_primary']
        healthy_backup = results['summary']['healthy_backup']
        
        print("\n" + "=" * 60)
        print("📊 健康状态汇总:")
        print(f"  主要源: {healthy_primary}/{len(results['primary'])} 健康")
        print(f"  备用源: {healthy_backup}/{len(results['backup'])} 健康")
        
        # 生成建议
        if healthy_primary >= 2:
            results['summary']['recommendation'] = "主要源健康，无需切换"
            print("\n✅ 建议: 主要源健康，无需切换")
        elif healthy_backup >= 2:
            results['summary']['recommendation'] = "建议切换到备用源"
            print("\n⚠️ 建议: 主要源不健康，建议切换到备用源")
        else:
            results['summary']['recommendation'] = "警告：RSS源严重不健康"
            print("\n❌ 警告: RSS源严重不健康，需要检查配置")
    
    def _save_health_cache(self, results):
        """保存健康检查缓存"""
        cache_dir = self.health_cache.parent
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.health_cache, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 健康检查结果已缓存: {self.health_cache}")
    
    def get_active_feeds(self):
        """获取活跃RSS源（自动选择健康源）"""
        # 加载缓存
        if self.health_cache.exists():
            with open(self.health_cache, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # 检查缓存是否过期（超过1小时）
            cache_time = datetime.fromisoformat(cache['summary']['timestamp'])
            elapsed = (datetime.now() - cache_time).total_seconds()
            
            if elapsed > 3600:  # 1小时
                print("⚠️ 健康检查缓存过期，重新检查...")
                cache = self.check_rss_health()
        else:
            # 无缓存，执行检查
            cache = self.check_rss_health()
        
        # 选择健康源
        healthy_primary = [
            r for r in cache['primary'] if r['healthy']
        ]
        
        healthy_backup = [
            r for r in cache['backup'] if r['healthy']
        ]
        
        # 优先使用主要源
        if len(healthy_primary) >= 2:
            active_feeds = [
                {
                    'name': r['name'],
                    'url': r['url'],
                    'max_items': self._get_max_items(r['name'])
                }
                for r in healthy_primary
            ]
        else:
            # 使用备用源
            active_feeds = [
                {
                    'name': r['name'],
                    'url': r['url'],
                    'max_items': self._get_max_items(r['name'])
                }
                for r in healthy_backup[:4]  # 最多4个备用源
            ]
        
        return active_feeds
    
    def _get_max_items(self, feed_name):
        """获取RSS源最大条数"""
        # 从配置中查找
        for feed in self.config['feeds']:
            if feed['name'] == feed_name:
                return feed['max_items']
        
        for feed in self.config.get('feeds_backup', []):
            if feed['name'] == feed_name:
                return feed['max_items']
        
        # 默认值
        return 5
    
    def auto_switch_to_backup(self):
        """自动切换到备用源"""
        print("=" * 60)
        print("🔄 自动切换到备用RSS源")
        print("=" * 60)
        
        # 检查健康状态
        results = self.check_rss_health()
        
        healthy_primary = results['summary']['healthy_primary']
        healthy_backup = results['summary']['healthy_backup']
        
        if healthy_primary >= 2:
            print("\n✅ 主要源健康，无需切换")
            return False
        
        if healthy_backup < 2:
            print("\n❌ 备用源不健康，无法切换")
            return False
        
        # 获取健康备用源
        healthy_backup_feeds = [
            r for r in results['backup'] if r['healthy']
        ]
        
        # 更新配置
        print("\n📝 更新配置文件...")
        
        # 保留健康的主要源
        healthy_primary_feeds = [
            r for r in results['primary'] if r['healthy']
        ]
        
        # 合并源列表
        new_feeds = [
            {
                'name': r['name'],
                'url': r['url'],
                'max_items': self._get_max_items(r['name'])
            }
            for r in healthy_primary_feeds + healthy_backup_feeds[:2]
        ]
        
        # 更新配置
        self.config['feeds'] = new_feeds
        
        # 保存配置
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已切换到 {len(new_feeds)} 个健康RSS源")
        
        return True
    
    def generate_health_report(self):
        """生成健康报告"""
        results = self.check_rss_health()
        
        report_file = self.project_dir / "reports" / f"RSS健康报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report_lines = [
            "# RSS源健康检查报告",
            "",
            f"**检查时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
            "",
            "---",
            "",
            "## 📊 健康状态汇总",
            "",
            f"- **主要源健康数**: {results['summary']['healthy_primary']}/{len(results['primary'])}",
            f"- **备用源健康数**: {results['summary']['healthy_backup']}/{len(results['backup'])}",
            f"- **建议**: {results['summary']['recommendation']}",
            "",
            "---",
            "",
            "## 📡 主要RSS源详情",
            ""
        ]
        
        for r in results['primary']:
            status = "✅ 健康" if r['healthy'] else "❌ 不健康"
            report_lines.append(f"### {r['name']}")
            report_lines.append(f"- **状态**: {status}")
            report_lines.append(f"- **新闻数**: {r['entries']}条")
            report_lines.append(f"- **响应时间**: {r['response_time']:.2f}s")
            
            if r['error']:
                report_lines.append(f"- **错误**: {r['error']}")
            
            report_lines.append("")
        
        report_lines.extend([
            "---",
            "",
            "## 🔄 备用RSS源详情",
            ""
        ])
        
        for r in results['backup']:
            status = "✅ 健康" if r['healthy'] else "❌ 不健康"
            report_lines.append(f"### {r['name']}")
            report_lines.append(f"- **状态**: {status}")
            report_lines.append(f"- **新闻数**: {r['entries']}条")
            report_lines.append(f"- **响应时间**: {r['response_time']:.2f}s")
            
            if r['error']:
                report_lines.append(f"- **错误**: {r['error']}")
            
            report_lines.append("")
        
        report_lines.extend([
            "---",
            "",
            f"_报告生成时间: {datetime.now().isoformat()}_"
        ])
        
        # 保存报告
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text("\n".join(report_lines), encoding='utf-8')
        
        print(f"\n📄 健康报告已生成: {report_file}")
        
        return report_file


def check_rss_health():
    """检查RSS源健康（供外部调用）"""
    monitor = RSSHealthMonitor()
    return monitor.check_rss_health()


def get_active_feeds():
    """获取活跃RSS源（供外部调用）"""
    monitor = RSSHealthMonitor()
    return monitor.get_active_feeds()


def main():
    """主函数"""
    monitor = RSSHealthMonitor()
    
    check_mode = '--check' in sys.argv
    switch_mode = '--switch' in sys.argv
    report_mode = '--report' in sys.argv
    
    if check_mode:
        monitor.check_rss_health()
    
    if switch_mode:
        monitor.auto_switch_to_backup()
    
    if report_mode:
        monitor.generate_health_report()
    
    if not check_mode and not switch_mode and not report_mode:
        # 默认执行健康检查
        monitor.check_rss_health()


if __name__ == "__main__":
    main()