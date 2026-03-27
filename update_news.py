import os
import google.generativeai as genai
from datetime import datetime

# 1. 强制配置 API 密钥
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_ai_content():
    # 策略：循环尝试不同的模型名称，直到有一个成功为止
    # 这样可以完美避开不同地区、不同账号对模型名称定义的差异
    model_names = ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-1.5-flash']
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请整理AI动态（国内/国外各10条），包含NVDA股价分析，以及卫龙(09985.HK)2025年报派息0.17元的分析。直接输出内容，不要代码块。"

    for name in model_names:
        try:
            print(f"尝试使用模型: {name}...")
            model = genai.GenerativeModel(name)
            response = model.generate_content(prompt)
            # 只要成功获取到内容，立刻返回
            if response.text:
                print(f"✅ 成功通过 {name} 获取内容")
                return response.text.replace("```html", "").replace("```", "").strip()
        except Exception as e:
            print(f"❌ 模型 {name} 失败: {str(e)}")
            continue
            
    return "资讯获取失败：所有备选模型均不可用。请检查 API Key 权限。"

def generate_full_html(ai_text):
    today_str = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S') # 加上秒，确保内容永远在变
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
    print("✅ 任务最终完成！")
