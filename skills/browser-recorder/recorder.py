"""
Browser Recorder - 浏览器操作录制器

录制浏览器操作 → 生成Playwright脚本 → 零成本回放
"""

import json
import os
from datetime import datetime
from pathlib import Path


class BrowserRecorder:
    """浏览器操作录制器"""
    
    def __init__(self, project_name="recording"):
        self.project_name = project_name
        self.operations = []
        self.cookies = []
        self.output_dir = Path(f"./recordings/{project_name}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def start_recording(self):
        """开始录制"""
        self.operations = []
        self.start_time = datetime.now()
        print(f"🎬 开始录制: {self.project_name}")
        print("按 Ctrl+C 或说 '停止录制' 结束")
    
    def record_click(self, selector, x, y):
        """记录点击操作"""
        self.operations.append({
            "type": "click",
            "selector": selector,
            "position": {"x": x, "y": y},
            "timestamp": datetime.now().isoformat()
        })
    
    def record_fill(self, selector, text):
        """记录输入操作"""
        self.operations.append({
            "type": "fill",
            "selector": selector,
            "text": text,
            "timestamp": datetime.now().isoformat()
        })
    
    def record_navigate(self, url):
        """记录导航"""
        self.operations.append({
            "type": "goto",
            "url": url,
            "timestamp": datetime.now().isoformat()
        })
    
    def record_screenshot(self, name="screenshot"):
        """记录截图"""
        self.operations.append({
            "type": "screenshot",
            "name": name,
            "timestamp": datetime.now().isoformat()
        })
    
    def save_cookies(self, cookies):
        """保存Cookie"""
        self.cookies = cookies
        cookie_file = self.output_dir / "cookies.json"
        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print(f"💾 Cookie已保存: {cookie_file}")
    
    def stop_recording(self):
        """停止录制并生成脚本"""
        print("🎬 停止录制")
        
        # 生成脚本
        script = self.generate_script()
        
        # 保存
        script_file = self.output_dir / f"{self.project_name}.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        # 保存操作记录
        ops_file = self.output_dir / f"{self.project_name}_ops.json"
        with open(ops_file, 'w', encoding='utf-8') as f:
            json.dump(self.operations, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 脚本已生成: {script_file}")
        return str(script_file)
    
    def generate_script(self):
        """生成Playwright脚本"""
        template = '''"""
{project_name} - 自动回放脚本
生成时间: {timestamp}
操作数: {op_count}
"""

from playwright.sync_api import sync_playwright
import json
from pathlib import Path

# Cookie文件路径
COOKIE_FILE = Path(__file__).parent / "cookies.json"

def load_cookies():
    """加载Cookie"""
    if COOKIE_FILE.exists():
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def playback():
    """执行录制的操作"""
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={{"width": 1920, "height": 1080}}
        )
        
        # 加载Cookie（如果存在）
        cookies = load_cookies()
        if cookies:
            context.add_cookies(cookies)
        
        page = context.new_page()
        
{operations}
        
        # 保存截图
        output_dir = Path(__file__).parent / "screenshots"
        output_dir.mkdir(exist_ok=True)
        page.screenshot(path=str(output_dir / "{project_name}_{timestamp}.png"), full_page=True)
        
        browser.close()
        print("✅ 回放完成")

if __name__ == "__main__":
    playback()
'''
        
        # 生成操作代码
        operations_code = []
        for i, op in enumerate(self.operations):
            if op["type"] == "goto":
                operations_code.append(f'        page.goto("{op["url"]}")  # {op["timestamp"]}')
            elif op["type"] == "click":
                operations_code.append(f'        page.click("{op["selector"]}")  # {op["timestamp"]}')
            elif op["type"] == "fill":
                safe_text = op["text"].replace('"', '\\"')
                operations_code.append(f'        page.fill("{op["selector"]}", "{safe_text}")  # {op["timestamp"]}')
            elif op["type"] == "screenshot":
                operations_code.append(f'        page.screenshot(path="screenshot_{i}.png")  # {op["timestamp"]}')
        
        return template.format(
            project_name=self.project_name,
            timestamp=datetime.now().strftime("%Y%m%d_%H%M%S"),
            op_count=len(self.operations),
            operations="\n".join(operations_code) if operations_code else "        # 无操作记录"
        )
    
    def playback(self, script_file=None):
        """回放录制的脚本"""
        if script_file is None:
            script_file = self.output_dir / f"{self.project_name}.py"
        
        print(f"▶️ 开始回放: {script_file}")
        os.system(f'python "{script_file}"')


# 使用示例
if __name__ == "__main__":
    # 创建录制器
    recorder = BrowserRecorder("taobao_search")
    
    # 开始录制
    recorder.start_recording()
    
    # ... 用户执行操作 ...
    # recorder.record_click("#search-input", 100, 50)
    # recorder.record_fill("#search-input", "不锈钢蒸架")
    # recorder.record_click("#search-button")
    
    # 停止录制并生成脚本
    recorder.stop_recording()
    
    # 回放
    # recorder.playback()
