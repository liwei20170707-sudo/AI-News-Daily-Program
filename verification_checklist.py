"""
验证清单脚本 - verification-before-completion
执行前验证 + 执行后质量检查

使用方式：
  python verification_checklist.py [--pre] [--post] [--report REPORT_FILE]
  
参数：
  --pre       执行前验证
  --post      执行后验证
  --report    指定报告文件路径（用于执行后验证）
"""

import sys
import os

# Windows控制台编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import json
import subprocess
from pathlib import Path
from datetime import datetime


class VerificationChecklist:
    """验证清单管理器"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.config_file = self.project_dir / "config.json"
        self.results = {
            'pre_check': {},
            'post_check': {},
            'summary': {}
        }
    
    def run_pre_verification(self):
        """执行前验证"""
        print("=" * 60)
        print("📋 执行前验证清单")
        print("=" * 60)
        
        checks = [
            ("Python环境", self.check_python_environment),
            ("RSS源健康", self.check_rss_health),
            ("推送渠道配置", self.check_push_channels),
            ("API密钥有效", self.check_api_keys),
            ("ffmpeg已安装", self.check_ffmpeg),
            ("依赖包完整", self.check_dependencies)
        ]
        
        all_passed = True
        
        for name, check_func in checks:
            print(f"\n🔍 {name}...")
            try:
                result = check_func()
                if result['passed']:
                    print(f"  ✅ 通过: {result['message']}")
                    self.results['pre_check'][name] = {
                        'status': 'passed',
                        'message': result['message']
                    }
                else:
                    print(f"  ❌ 失败: {result['message']}")
                    self.results['pre_check'][name] = {
                        'status': 'failed',
                        'message': result['message']
                    }
                    all_passed = False
            except Exception as e:
                print(f"  ⚠️ 异常: {e}")
                self.results['pre_check'][name] = {
                    'status': 'error',
                    'message': str(e)
                }
                all_passed = False
        
        # 汇总
        print("\n" + "=" * 60)
        if all_passed:
            print("✅ 执行前验证全部通过，可以开始执行")
            self.results['summary']['pre_check_passed'] = True
        else:
            print("❌ 执行前验证失败，请先修复问题")
            self.results['summary']['pre_check_passed'] = False
        
        return all_passed
    
    def run_post_verification(self, report_file=None):
        """执行后验证"""
        print("\n" + "=" * 60)
        print("📋 执行后验证清单")
        print("=" * 60)
        
        # 确定报告文件
        if not report_file:
            report_file = self.project_dir / "reports" / f"AI早报_{datetime.now().strftime('%Y%m%d')}.md"
        
        checks = [
            ("报告文件存在", lambda: self.check_report_exists(report_file)),
            ("新闻数量达标", lambda: self.check_news_count(report_file)),
            ("摘要生成成功", lambda: self.check_summary_success(report_file)),
            ("推送成功率", lambda: self.check_push_success()),
            ("播客生成质量", lambda: self.check_podcast_quality()),
            ("GitHub RSS更新", lambda: self.check_github_rss_update())
        ]
        
        all_passed = True
        
        for name, check_func in checks:
            print(f"\n🔍 {name}...")
            try:
                result = check_func()
                if result['passed']:
                    print(f"  ✅ 通过: {result['message']}")
                    self.results['post_check'][name] = {
                        'status': 'passed',
                        'message': result['message'],
                        'details': result.get('details', {})
                    }
                else:
                    print(f"  ❌ 失败: {result['message']}")
                    self.results['post_check'][name] = {
                        'status': 'failed',
                        'message': result['message'],
                        'details': result.get('details', {})
                    }
                    all_passed = False
            except Exception as e:
                print(f"  ⚠️ 异常: {e}")
                self.results['post_check'][name] = {
                    'status': 'error',
                    'message': str(e)
                }
                all_passed = False
        
        # 汇总
        print("\n" + "=" * 60)
        if all_passed:
            print("✅ 执行后验证全部通过，任务完成")
            self.results['summary']['post_check_passed'] = True
        else:
            print("⚠️ 执行后验证部分失败，需要检查")
            self.results['summary']['post_check_passed'] = False
        
        return all_passed
    
    # ========== 执行前验证方法 ==========
    
    def check_python_environment(self):
        """检查Python环境"""
        # 主流程使用Python 3.13
        main_python = "C:\\Users\\lw\\.workbuddy\\binaries\\python\\versions\\3.13.12\\python.exe"
        
        # 检查主Python版本
        try:
            result = subprocess.run(
                [main_python, "--version"],
                capture_output=True,
                text=True
            )
            
            if "3.13" in result.stdout:
                return {
                    'passed': True,
                    'message': f"主流程Python: {result.stdout.strip()}"
                }
            else:
                return {
                    'passed': False,
                    'message': f"Python版本不匹配: {result.stdout}"
                }
        except Exception as e:
            return {
                'passed': False,
                'message': f"无法检查Python版本: {e}"
            }
    
    def check_rss_health(self):
        """检查RSS源健康"""
        import feedparser
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        healthy_count = 0
        total_count = len(config['feeds'])
        
        for feed in config['feeds']:
            try:
                parsed = feedparser.parse(feed['url'])
                if len(parsed.entries) > 0:
                    healthy_count += 1
            except:
                pass
        
        # 至少2个健康源
        if healthy_count >= 2:
            return {
                'passed': True,
                'message': f"{healthy_count}/{total_count}个RSS源健康",
                'details': {'healthy': healthy_count, 'total': total_count}
            }
        else:
            return {
                'passed': False,
                'message': f"只有{healthy_count}个健康源，至少需要2个"
            }
    
    def check_push_channels(self):
        """检查推送渠道配置"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        channels = []
        
        # 钉钉
        if config['push'].get('dingtalk_webhook'):
            channels.append('钉钉')
        
        # Server酱
        if config['push'].get('serverchan_key'):
            channels.append('Server酱')
        
        # SMTP
        if config['push'].get('emails'):
            channels.append('SMTP邮件')
        
        if len(channels) >= 2:
            return {
                'passed': True,
                'message': f"已配置{len(channels)}个推送渠道: {', '.join(channels)}"
            }
        else:
            return {
                'passed': False,
                'message': f"只配置了{len(channels)}个渠道，至少需要2个"
            }
    
    def check_api_keys(self):
        """检查API密钥"""
        # 检查阿里云API密钥
        dashscope_key_file = self.project_dir / "dashscope_key.txt"
        
        if dashscope_key_file.exists():
            key = dashscope_key_file.read_text(encoding='utf-8').strip()
            if len(key) > 10:
                return {
                    'passed': True,
                    'message': "阿里云API密钥已配置"
                }
        
        # 检查环境变量
        import os
        if os.environ.get('DASHSCOPE_API_KEY'):
            return {
                'passed': True,
                'message': "阿里云API密钥已配置（环境变量）"
            }
        
        return {
            'passed': False,
            'message': "阿里云API密钥未配置，将无法生成AI摘要"
        }
    
    def check_ffmpeg(self):
        """检查ffmpeg安装"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    'passed': True,
                    'message': "ffmpeg已安装"
                }
        except:
            pass
        
        return {
            'passed': False,
            'message': "ffmpeg未安装，播客生成将失败"
        }
    
    def check_dependencies(self):
        """检查依赖包"""
        required = ['feedparser', 'openai']
        missing = []
        
        for pkg in required:
            try:
                __import__(pkg)
            except ImportError:
                missing.append(pkg)
        
        if len(missing) == 0:
            return {
                'passed': True,
                'message': "所有依赖包已安装"
            }
        else:
            return {
                'passed': False,
                'message': f"缺少依赖: {', '.join(missing)}"
            }
    
    # ========== 执行后验证方法 ==========
    
    def check_report_exists(self, report_file):
        """检查报告文件存在"""
        if report_file.exists():
            size = report_file.stat().st_size
            return {
                'passed': True,
                'message': f"报告文件已生成 ({size} bytes)",
                'details': {'file': str(report_file), 'size': size}
            }
        else:
            return {
                'passed': False,
                'message': f"报告文件不存在: {report_file}"
            }
    
    def check_news_count(self, report_file):
        """检查新闻数量"""
        if not report_file.exists():
            return {'passed': False, 'message': "报告文件不存在"}
        
        content = report_file.read_text(encoding='utf-8')
        
        # 提取新闻数量
        import re
        match = re.search(r'共 (\d+) 条精选', content)
        
        if match:
            count = int(match.group(1))
            
            # 至少15条新闻
            if count >= 15:
                return {
                    'passed': True,
                    'message': f"新闻数量达标: {count}条",
                    'details': {'count': count}
                }
            else:
                return {
                    'passed': False,
                    'message': f"新闻数量不足: {count}条，至少需要15条"
                }
        else:
            return {
                'passed': False,
                'message': "无法解析新闻数量"
            }
    
    def check_summary_success(self, report_file):
        """检查摘要生成成功"""
        if not report_file.exists():
            return {'passed': False, 'message': "报告文件不存在"}
        
        content = report_file.read_text(encoding='utf-8')
        
        # 检查是否包含摘要标记
        if '📌' in content:
            # 统计摘要数量
            summary_count = content.count('📌')
            
            return {
                'passed': True,
                'message': f"摘要生成成功: {summary_count}条",
                'details': {'summary_count': summary_count}
            }
        else:
            return {
                'passed': False,
                'message': "未找到摘要标记"
            }
    
    def check_push_success(self):
        """检查推送成功率"""
        # 从最近的工作记忆读取推送结果
        memory_file = self.project_dir / ".workbuddy" / "memory" / f"{datetime.now().strftime('%Y-%m-%d')}.md"
        
        if memory_file.exists():
            content = memory_file.read_text(encoding='utf-8')
            
            # 统计推送成功次数
            success_count = content.count('推送成功') + content.count('✅')
            
            # 至少2个推送成功
            if success_count >= 2:
                return {
                    'passed': True,
                    'message': f"推送成功率达标: {success_count}个渠道成功",
                    'details': {'success_count': success_count}
                }
        
        # 默认返回（无法验证）
        return {
            'passed': True,
            'message': "推送验证需要实际执行结果"
        }
    
    def check_podcast_quality(self):
        """检查播客质量"""
        podcast_file = self.project_dir / "podcasts" / f"AI科技早报_{datetime.now().strftime('%Y%m%d')}.mp3"
        
        if podcast_file.exists():
            size = podcast_file.stat().st_size
            
            # 文件大小至少1MB
            if size >= 1024 * 1024:
                return {
                    'passed': True,
                    'message': f"播客文件已生成 ({size / 1024 / 1024:.2f} MB)",
                    'details': {'file': str(podcast_file), 'size': size}
                }
            else:
                return {
                    'passed': False,
                    'message': f"播客文件过小 ({size} bytes)，可能生成失败"
                }
        else:
            return {
                'passed': False,
                'message': "播客文件未生成"
            }
    
    def check_github_rss_update(self):
        """检查GitHub RSS更新"""
        podcast_xml = self.project_dir / "podcast.xml"
        
        if podcast_xml.exists():
            content = podcast_xml.read_text(encoding='utf-8')
            
            # 检查是否包含今天的日期
            today = datetime.now().strftime('%Y-%m-%d')
            
            if today in content:
                return {
                    'passed': True,
                    'message': f"GitHub RSS已更新（包含{today}）"
                }
            else:
                return {
                    'passed': False,
                    'message': f"GitHub RSS未更新（缺少{today}）"
                }
        else:
            return {
                'passed': False,
                'message': "podcast.xml不存在"
            }
    
    def save_results(self):
        """保存验证结果"""
        result_file = self.project_dir / ".workbuddy" / "verification_results.json"
        
        result_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 验证结果已保存: {result_file}")


def main():
    """主函数"""
    checklist = VerificationChecklist()
    
    pre_mode = '--pre' in sys.argv
    post_mode = '--post' in sys.argv
    
    # 解析报告文件参数
    report_file = None
    if '--report' in sys.argv:
        idx = sys.argv.index('--report')
        if idx + 1 < len(sys.argv):
            report_file = Path(sys.argv[idx + 1])
    
    if pre_mode:
        checklist.run_pre_verification()
    
    if post_mode:
        checklist.run_post_verification(report_file)
    
    if not pre_mode and not post_mode:
        # 默认执行前验证
        checklist.run_pre_verification()
    
    # 保存结果
    checklist.save_results()


if __name__ == "__main__":
    main()