import os
import requests
import json
from datetime import datetime

def get_ai_content():
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # 尝试清单：先试 1.5-flash，再试 1.0-pro (最稳兼容版)
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-pro"
    ]
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请整理：1.国内AI动态10条；2.国外AI动态10条；3.卫龙(09985.HK)2025年报派息0.17元的持股建议。直接输出文字。"

    for model in models_to_try:
        # 尝试 v1 接口
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            print(f"正在尝试模型: {model} ...")
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()
            
            if 'candidates' in result:
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                print(f"模型 {model} 暂不可用，尝试下一个...")
                continue
        except Exception as e:
            print(f"请求 {model} 异常: {e}")
            continue
            
    return "资讯获取失败。请检查：1.API Key是否正确；2.Google AI Studio中是否开启了该模型权限。"

def generate_full_html(ai_text):
    today_str = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
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
            <footer class="bg-slate-50 p-6 text-center text-slate-400 text-sm border-t">由 Gemini AI 自动化生成</footer>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    content = get_ai_content()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generate_full_html(content))
    print("✅ 尝试完成！")
