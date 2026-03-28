import os
import requests
import json
import time
from datetime import datetime

def get_ai_content():
    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = (
        f"今天是{today}。请整理并输出以下内容：\n"
        f"1. 国内 AI 行业重大动态 10 条；\n"
        f"2. 国外 AI 行业重大动态 10 条；\n"
        f"3. 针对卫龙(09985.HK)2025年报建议派息0.17元的持股分析及建议。\n"
        f"请直接输出正文，保持排版整洁，不要包含 Markdown 标签。"
    )
    
    # 核心改进：增加安全设置，防止因为内容敏感被拦截导致误报配额错误
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    # 尝试 3 次，增加等待时长
    wait_times = [60, 120, 180] # 第一次失败等 1 分钟，第二次等 2 分钟
    
    for attempt in range(3):
        try:
            print(f"正在发起请求 (第 {attempt + 1} 次尝试)...")
            response = requests.post(url, json=payload, timeout=60) # 增加超时时间到 60s
            result = response.json()
            
            if response.status_code == 200:
                if 'candidates' in result and result['candidates'][0].get('content'):
                    print("✅ 内容抓取成功！")
                    return result['candidates'][0]['content']['parts'][0]['text'].strip()
                else:
                    # 有时候 200 OK 但 candidate 为空，是因为被安全策略拦截了
                    return "内容生成被安全策略拦截，请尝试修改 Prompt。"
            
            elif response.status_code == 429:
                wait_time = wait_times[attempt]
                print(f"⚠️ 触发配额限制，休息 {wait_time} 秒后重试...")
                time.sleep(wait_time) 
                continue
            
            else:
                error_msg = result.get('error', {}).get('message', '未知错误')
                print(f"服务器返回错误: {error_msg}")
                # 即使是其他错误，也建议重试一下，万一是网络抖动
                time.sleep(10)
                continue
                
        except Exception as e:
            print(f"❌ 网络异常: {e}")
            time.sleep(10)
            continue
            
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
