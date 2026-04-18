# Browser Recorder - 浏览器操作录制Skill

> 录制浏览器操作 → 生成Playwright脚本 → 零成本回放

## 核心原理

```
传统AI操作                    录制回放
用户操作 → AI推理 → 执行    用户操作 → 录制 → 回放（0 Token）
   慢 + 贵 + 幻觉          快 + 0成本 + 确定
```

## 功能

### 1. 录制模式 (record)
- 启动Chrome CDP
- 记录所有操作：点击、输入、滚动、截图
- 自动提取元素选择器（CSS/XPath）
- 生成可回放的Python脚本

### 2. 回放模式 (playback)
- 执行录制的脚本
- 0 Token消耗
- 可定时执行

### 3. Cookie管理 (cookie)
- 保存登录状态
- 自动注入Cookie
- 绕过验证码

## 使用场景

| 场景 | 说明 |
|------|------|
| 数据抓取 | 每天固定操作，录制一次，每天回放 |
| 表单填写 | 固定格式表单，录制一次，批量回放 |
| 竞品监控 | 登录→搜索→截图，录制后自动执行 |

## 使用方法

### 录制操作
```
用户：录制淘宝商品搜索
AI：启动录制模式，开始记录你的操作
用户：搜索关键词、筛选条件、滚动页面
AI：停止录制，生成playwright脚本
```

### 回放执行
```
用户：回放昨天的操作
AI：执行脚本，自动完成所有操作
```

## 技术实现

### 录制流程
```
1. 启动Chrome (--remote-debugging-port=9222)
2. 注入录制脚本
3. 监听用户操作
4. 记录选择器 + 操作类型
5. 生成Python代码
```

### 回放流程
```
1. 加载Cookie
2. 执行录制的脚本
3. 截图保存
4. 可选：发送钉钉通知
```

## 脚本格式

```python
from playwright.sync_api import sync_playwright

def playback():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        # 加载Cookie
        context.add_cookies(cookies)
        
        page = context.new_page()
        page.goto("https://example.com")
        # 录制的操作
        page.click("selector")
        page.fill("input", "text")
        page.screenshot(path="result.png")
        
        browser.close()

if __name__ == "__main__":
    playback()
```

## 与电商运营的结合

| Skill | 结合方式 |
|-------|----------|
| 淘宝抓取 | 录制登录→搜索→翻页→抓数据 |
| 竞品监控 | 录制登录→查看竞品页面→截图 |
| 千牛巡店 | 录制登录→查看物流→退款→截图 |

## 优势

- ✅ 零Token成本（录制一次，永久回放）
- ✅ 速度快（无需AI推理）
- ✅ 结果确定（无幻觉）
- ✅ 可定时执行
- ✅ 支持复杂操作
- ✅ 自动保存Cookie（免登录）

## 使用流程

```
1. 【录制】启动Chrome CDP，打开目标网站
2. 【操作】执行一次完整操作（登录→搜索→翻页→截图）
3. 【生成】AI生成Playwright脚本
4. 【回放】每天定时回放，0成本执行
```

## 文件结构

```
browser-recorder/
├── SKILL.md                     # 本文件
├── recorder.py                  # 录制核心逻辑
├── templates/
│   └── playwright_template.py   # 回放脚本模板
└── examples/
    └── taobao_monitor.py       # 淘宝监控示例
```

## 更新日志

- v1.0 (2026-04-18): 初始版本，核心录制/回放功能
