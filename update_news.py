import os
import requests
import json
from datetime import datetime

def get_ai_content():
    api_key = os.environ.get("GEMINI_API_KEY")
    # 强制锁定 v1 正式接口路径，彻底绕过 v1beta
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请整理：1.国内AI动态10条；2.国外AI动态10条；3.卫龙(09985.HK)2025年报派息0.17元的持股建议。直接输出文字，不要HTML标签。"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    headers = {'Content-Type': 'application/json'}

    try:
        print("正在通过最原始的 HTTP 方式访问 v1 接口...")
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()
        
        # 即使报错，也会打印出详细的 JSON 信息，方便我们最后排查
        if 'candidates' in result:
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            return f"获取失败。服务器返回：{json.dumps(result)}"
    except Exception as e:
        return f"网络连接异常: {str(e)}"

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
    html_page = generate_full_html(content)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_page)
    print("✅ 尝试完成！")
