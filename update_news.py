import os
import google.generativeai as genai
from datetime import datetime

# 1. 配置 API 密钥
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# --- 关键修改：强制指定使用 v1 接口 ---
from google.generativeai import types
# -----------------------------------

def get_ai_content():
    # 既然已经升级了库，我们直接用最标准的名称
    model_name = 'gemini-1.5-flash'
    
    today = datetime.now().strftime('%Y-%m-%d')
    # ... 剩下的代码保持不变 ...
    prompt = f"今天是{today}。请整理AI动态（国内/国外各10条），包含NVDA股价分析，以及卫龙(09985.HK)2025年报派息0.17元的分析。直接输出内容，不要代码块。"

    for name in model_names:
        try:
            print(f"尝试使用模型: {name}...")
            model = genai.GenerativeModel(name)
            response = model.generate_content(prompt)
            if response.text:
                return response.text.replace("```html", "").replace("```", "").strip()
        except Exception as e:
            # 修改这一行，把具体的错误原因打印到网页上！
            print(f"❌ 模型 {name} 失败详情: {str(e)}")
            error_detail = str(e) # 记录下最后一次报错的细节
            continue
            
    return f"资讯获取失败。原因详情: {error_detail}" # 把这个详情显示在网页上

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
