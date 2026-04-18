"""
淘宝竞品监控录制示例

使用方法：
1. 运行此脚本
2. 执行一次淘宝搜索操作
3. 按Ctrl+C停止
4. 之后每天回放即可
"""

from playwright.sync_api import sync_playwright
import json
from pathlib import Path
from datetime import datetime


class TaobaoRecorder:
    """淘宝竞品监控录制器"""
    
    def __init__(self):
        self.project_name = "taobao_competitor"
        self.output_dir = Path(f"./recordings/{self.project_name}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.operations = []
    
    def record_operation(self, op_type, selector=None, value=None, url=None):
        """录制操作"""
        self.operations.append({
            "type": op_type,
            "selector": selector,
            "value": value,
            "url": url,
            "timestamp": datetime.now().isoformat()
        })
        print(f"📝 录制: {op_type} -> {selector or url}")
    
    def save_cookies(self, context):
        """保存登录状态"""
        cookies = context.cookies()
        cookie_file = self.output_dir / "cookies.json"
        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print(f"💾 Cookie已保存: {cookie_file}")
        return cookies
    
    def generate_script(self):
        """生成回放脚本"""
        script = f'''"""
淘宝竞品监控脚本
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
操作数: {len(self.operations)}

使用方法: python taobao_competitor_playback.py
"""

from playwright.sync_api import sync_playwright
import json
from pathlib import Path
from datetime import datetime

COOKIE_FILE = Path(__file__).parent / "cookies.json"
OUTPUT_DIR = Path(__file__).parent / "screenshots"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_cookies():
    """加载Cookie"""
    if COOKIE_FILE.exists():
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def playback():
    """执行监控"""
    print("🚀 开始淘宝竞品监控...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={{"width": 1920, "height": 1080}},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        # 加载Cookie
        cookies = load_cookies()
        if cookies:
            context.add_cookies(cookies)
            print("✅ Cookie已加载")
        
        page = context.new_page()
'''
        
        for i, op in enumerate(self.operations):
            if op["type"] == "goto":
                script += f'''
        page.goto("{op["url"]}")'''
            elif op["type"] == "click":
                script += f'''
        page.click("{op["selector"]}")'''
            elif op["type"] == "fill":
                safe_value = (op["value"] or "").replace('"', '\\"')
                script += f'''
        page.fill("{op["selector"]}", "{safe_value}")'''
            elif op["type"] == "screenshot":
                script += f'''
        page.screenshot(
            path=str(OUTPUT_DIR / "competitor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png"),
            full_page=True
        )'''
        
        script += '''
        
        # 关闭
        browser.close()
        print("✅ 监控完成")

if __name__ == "__main__":
    playback()
'''
        
        # 保存脚本
        script_file = self.output_dir / f"{self.project_name}_playback.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        # 保存操作记录
        ops_file = self.output_dir / f"{self.project_name}_ops.json"
        with open(ops_file, 'w', encoding='utf-8') as f:
            json.dump(self.operations, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 脚本已生成: {script_file}")
        return str(script_file)


def manual_recording():
    """手动录制模式"""
    print("=" * 50)
    print("淘宝竞品监控录制器")
    print("=" * 50)
    print("请在浏览器中执行操作")
    print("操作会被记录并生成可回放的脚本")
    print()
    
    recorder = TaobaoRecorder()
    
    # 示例：手动添加操作
    # 实际使用时，可以通过CDP实时录制
    
    # 1. 打开淘宝
    recorder.record_operation("goto", url="https://www.taobao.com")
    
    # 2. 点击搜索框
    recorder.record_operation("click", selector="#q")
    
    # 3. 输入关键词
    recorder.record_operation("fill", selector="#q", value="不锈钢蒸架")
    
    # 4. 点击搜索按钮
    recorder.record_operation("click", selector=".btn-search")
    
    # 5. 截图
    recorder.record_operation("screenshot")
    
    # 生成脚本
    script_file = recorder.generate_script()
    
    print()
    print("=" * 50)
    print("录制完成！")
    print(f"脚本位置: {{script_file}}")
    print()
    print("使用方法:")
    print("1. 首次运行需要登录淘宝")
    print("2. 之后运行会自动加载Cookie免登录")
    print("3. 每天定时回放即可")
    print("=" * 50)


if __name__ == "__main__":
    manual_recording()
