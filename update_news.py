import os
import requests
import json
import time
from datetime import datetime

def get_ai_content():
    # 从 GitHub Secrets 获取 Key
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # 锁定验证成功的 v1beta 接口和 2.0-flash 模型
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = (
        f"今天是{today}。请整理并输出以下内容：\n"
        f"1. 国内 AI 行业重大动态 10 条；\n"
        f"2. 国外 AI 行业重大动态 10 条；\n"
        f"3. 针对卫龙(09985.HK)2025年报建议派息0.17元的持股分析及建议。\n"
        f"请直接输出正文，保持排版整洁，不要包含 Markdown 标签。"
    )
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    # 尝试 3 次，应对 429 (RESOURCE_EXHAUSTED) 配额限制
    for attempt in range(3):
        try:
            print(f"正在发起请求 (第 {attempt + 1} 次尝试)...")
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()
            
            # 状态码 200 表示成功
            if response.status_code == 200 and 'candidates' in result:
                print("✅ 内容抓取成功！")
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # 状态码 429 表示频率太快，需要休息
            elif response.status_code == 429:
                print(f"⚠️ 触发配额限制，休息 30 秒后重试...")
                time.sleep(30) 
                continue
            
            else:
                # 其他错误则直接返回错误信息
                error_msg = result.get('error', {}).get('message', '未知错误')
                return f"获取失败。状态码：{response.status_code}，详情：{error_msg}"
                
        except Exception as e:
            print(f"❌ 网络异常: {e}")
            if attempt < 2:
                time.sleep(5)
                continue
            return f"网络异常，请检查 GitHub 环境: {str(e)}"
            
    return "抱歉，由于 Google API 免费层配额限制，今日连续 3 次尝试均失败。请过 1 小时后再手动触发。"

def generate_full_html(ai_text):
    """生成精美的 HTML 页面"""
    today_str = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    # 处理换行，让网页显示更自然
    formatted_text = ai_text.replace("\n", "<br>")
    
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI 资讯日报</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #f8fafc; color: #1e293b; }}
            .content-area {{ line-height: 1.8; }}
        </style>
    </head>
    <body class="p-4 md:p-10">
        <div class="max-w-4xl mx-auto bg-white p-8 md:p-12 rounded-3xl shadow-2xl border border-slate-100">
            <header class="mb-10 border-b border-slate-100 pb-8">
                <div class="flex items-center justify-between">
                    <h1 class="text-3xl font-black text-slate-900 tracking-tight">AI 资讯每日精选</h1>
                    <span class="bg-blue-100 text-blue-700 text-xs px-3 py-1 rounded-full font-bold">LIVE</span>
                </div>
                <p class="text-slate-400 mt-3 font-medium">生成时间：{today_str}</p>
            </header>
            
            <main class="content-area text-slate-700 space-y-6 text-lg">
                {formatted_text}
            </main>
            
            <footer class="mt-16 pt-8 border-t border-slate-50 text-center">
                <p class="text-sm text-slate-300 font-light">由 Gemini 2.0 Flash 智能模型驱动 · 自动化报纸系统</p>
            </footer>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    content = get_ai_content()
    # 强制使用 utf-8 编码写入文件，防止中文乱码
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generate_full_html(content))
    print("✅ 脚本运行结束")
