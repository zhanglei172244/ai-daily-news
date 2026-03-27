import os
import requests
import json
from datetime import datetime

def get_ai_content():
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # 策略清单：尝试所有可能的 [接口版本, 模型名称] 组合
    strategies = [
        ("v1", "gemini-1.5-flash"),
        ("v1beta", "gemini-1.5-flash"),
        ("v1", "gemini-pro"),
        ("v1beta", "gemini-pro")
    ]
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请整理：1.国内AI动态10条；2.国外AI动态10条；3.卫龙(09985.HK)2025年报派息0.17元的持股建议。直接输出文字。"

    for version, model in strategies:
        url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            print(f"尝试组合: {version} / {model} ...")
            response = requests.post(url, json=payload, timeout=20)
            result = response.json()
            
            if 'candidates' in result:
                print(f"🎉 成功！找到通畅路径: {version}/{model}")
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                print(f"❌ 路径 {version}/{model} 报错: {result.get('error', {}).get('message', '未知错误')}")
        except Exception as e:
            print(f"⚠️ 网络请求异常 ({version}/{model}): {e}")
            
    return "资讯获取失败。建议检查 Google AI Studio 的 API Key 状态。"

def generate_full_html(ai_text):
    today_str = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    # 简单的格式化处理
    formatted_text = ai_text.replace("\n", "<br>")
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8"><title>AI 资讯日报 - {today_str}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>body {{ background-color: #f3f4f6; }} .content-box {{ white-space: pre-wrap; line-height: 1.8; }}</style>
    </head>
    <body class="p-4 md:p-8">
        <div class="max-w-4xl mx-auto bg-white shadow-xl rounded-2xl overflow-hidden">
            <header class="bg-slate-900 text-white p-6">
                <h1 class="text-2xl font-bold">AI 资讯每日精选</h1>
                <p class="text-slate-400 mt-2">更新时间：{today_str}</p>
            </header>
            <main class="p-6 md:p-10 content-box text-slate-700">{formatted_text}</main>
            <footer class="bg-slate-50 p-6 text-center text-slate-400 text-sm border-t">由 Gemini AI 自动抓取更新</footer>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    content = get_ai_content()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generate_full_html(content))
    print("✅ 脚本运行结束")
