"""
Playwright回放脚本模板

复制此模板，根据实际录制操作修改
"""

from playwright.sync_api import sync_playwright
import json
from pathlib import Path
from datetime import datetime


class PlaybackTemplate:
    """回放模板基类"""
    
    def __init__(self, name):
        self.name = name
        self.cookie_file = Path(__file__).parent.parent / "cookies.json"
        self.output_dir = Path(__file__).parent.parent / "screenshots"
        self.output_dir.mkdir(exist_ok=True, parents=True)
    
    def load_cookies(self, context):
        """加载Cookie"""
        if self.cookie_file.exists():
            with open(self.cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
                print(f"✅ 已加载 {len(cookies)} 条Cookie")
    
    def save_cookies(self, context):
        """保存Cookie"""
        cookies = context.cookies()
        with open(self.cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print(f"💾 已保存 {len(cookies)} 条Cookie")
    
    def take_screenshot(self, page, prefix="screenshot"):
        """截图"""
        filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = self.output_dir / filename
        page.screenshot(path=str(path), full_page=True)
        print(f"📸 截图已保存: {path}")
        return str(path)
    
    def run(self):
        """执行回放"""
        raise NotImplementedError("子类必须实现run方法")


# ==================== 具体实现示例 ====================

class TaobaoSearchPlayback(PlaybackTemplate):
    """淘宝搜索回放"""
    
    def __init__(self):
        super().__init__("taobao_search")
        self.search_keyword = "不锈钢蒸架"  # 可配置
    
    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )
            
            # 加载Cookie
            self.load_cookies(context)
            
            page = context.new_page()
            
            # 1. 打开淘宝
            page.goto("https://www.taobao.com")
            page.wait_for_load_state("networkidle")
            
            # 2. 输入搜索词
            page.fill("#q", self.search_keyword)
            
            # 3. 点击搜索
            page.click(".btn-search")
            page.wait_for_load_state("networkidle")
            
            # 4. 截图
            self.take_screenshot(page, "taobao_search")
            
            browser.close()
            print("✅ 执行完成")


class CompetitorMonitorPlayback(PlaybackTemplate):
    """竞品监控回放"""
    
    def __init__(self):
        super().__init__("competitor_monitor")
        self.competitor_urls = [
            "https://item.taobao.com/item.htm?id=xxx",
            "https://detail.tmall.com/item.htm?id=yyy",
        ]
    
    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )
            
            self.load_cookies(context)
            page = context.new_page()
            
            results = []
            for i, url in enumerate(self.competitor_urls):
                print(f"📦 监控第 {i+1}/{len(self.competitor_urls)} 个商品")
                page.goto(url)
                page.wait_for_load_state("networkidle")
                
                # 提取价格
                try:
                    price = page.text_content(".price")
                    sales = page.text_content(".sales")
                    results.append({
                        "url": url,
                        "price": price,
                        "sales": sales,
                        "time": datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"⚠️ 提取失败: {e}")
                
                # 截图
                self.take_screenshot(page, f"competitor_{i+1}")
            
            # 保存结果
            result_file = self.output_dir / f"monitor_results_{datetime.now().strftime('%Y%m%d')}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"📊 监控结果已保存: {result_file}")
            
            browser.close()
            print("✅ 监控完成")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "taobao":
            TaobaoSearchPlayback().run()
        elif mode == "competitor":
            CompetitorMonitorPlayback().run()
        else:
            print("用法: python playwright_template.py [taobao|competitor]")
    else:
        print("用法: python playwright_template.py [taobao|competitor]")
