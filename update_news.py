import os
import google.generativeai as genai
from datetime import datetime

# 强制配置
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_ai_content():
    # 重点：只保留这一个目前兼容性最强的模型全称
    model_name = 'gemini-1.5-flash-latest'
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请整理：1.国内AI动态10条；2.国外AI动态10条；3.卫龙(09985.HK)2025年报派息0.17元的持股建议。直接输出文字内容。"
    
    try:
        print(f"正在尝试使用最优模型: {model_name}")
        # 强制指定版本为 v1，绕过报错的 v1beta
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        # 如果还是报错，我们最后尝试一次最原始的 gemini-pro
        if "404" in error_msg:
            try:
                print("尝试备选方案...")
                model = genai.GenerativeModel('gemini-pro')
                return model.generate_content(prompt).text
            except:
                pass
        return f"获取失败。详情: {error_msg}"
    return "未获取到内容"

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
                <p class="text-slate-400 mt-2">更新日期：{today_str}</p>
            </header>
            <main class="p-6 md:p-10 content-box text-slate-700">{formatted_text}</main>
            <footer class="bg-slate-50 p-6 text-center text-slate-400 text-sm">由 Gemini AI 自动化生成</footer>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    content = get_ai_content()
    html_page = generate_full_html(content)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_page)
