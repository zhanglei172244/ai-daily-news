import os
from datetime import datetime
from google import genai

def get_ai_content():
    # 使用全新的官方客户端
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请整理：1.国内AI动态10条；2.国外AI动态10条；3.卫龙(09985.HK)2025年报派息0.17元的持股建议。直接输出文字，不要HTML标签。"
    
    try:
        # 这个新库会自动选择最稳妥的 v1 接口
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"资讯获取失败。错误详情: {str(e)}"

def generate_full_html(ai_text):
    today_str = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    formatted_text = ai_text.replace("\n", "<br>")
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI 资讯日报 - {today_str}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>body {{ background-color: #f3f4f6; font-family: sans-serif; }} .content-box {{ white-space: pre-wrap; line-height: 1.8; }}</style>
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
