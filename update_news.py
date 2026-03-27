import os
import google.generativeai as genai
from datetime import datetime

# 1. 配置 API 密钥
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_ai_content():
    # 改动点：在这里加上 "models/" 前缀，这是最新版库的强制要求
    model_names = ['models/gemini-1.5-flash', 'models/gemini-pro']
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请整理：1.国内AI动态10条；2.国外AI动态10条；3.卫龙(09985.HK)2025年报派息0.17元的持股建议。直接输出文字，不要HTML标签。"
    
    error_detail = ""
    for name in model_names:
        try:
            print(f"正在通过 {name} 获取内容...")
            model = genai.GenerativeModel(name)
            # 只要库是最新的，这个 generate_content 就会自动走 v1 接口
            response = model.generate_content(prompt)
            if response.text:
                return response.text.replace("```html", "").replace("```", "").strip()
        except Exception as e:
            error_detail = str(e)
            print(f"❌ {name} 尝试失败: {error_detail}")
            continue
            
    return f"资讯获取失败。详情: {error_detail}"

def generate_full_html(ai_text):
    # 保持秒数更新，解决 Git 提交报错问题
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
            <div style="display:none">{today_str}</div>
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
    print("✅ 任务完成！")
