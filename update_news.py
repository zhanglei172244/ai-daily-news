import os
import sys
import subprocess

# --- 暴力补丁：如果库版本不对，脚本自发升级 ---
try:
    import google.generativeai as genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai==0.8.3"])
    import google.generativeai as genai
# ---------------------------------------

from datetime import datetime

# 配置 API 密钥
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_ai_content():
    # 显式指定最新模型的全名
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro']
    
    # ... 后面的逻辑保持不变 ...
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请整理：1.国内AI动态10条；2.国外AI动态10条；3.卫龙(09985.HK)2025年报派息0.17元的持股建议。直接输出文字，不要HTML标签。"
    
    error_detail = ""
    for name in model_names:
        try:
            print(f"正在尝试模型: {name}...")
            # 关键：显式通过 model_name 参数传入
            model = genai.GenerativeModel(model_name=name) 
            response = model.generate_content(prompt)
            if response.text:
                return response.text.strip()
        except Exception as e:
            # 这里会捕获具体的错误详情
            error_detail = str(e)
            print(f"❌ {name} 失败详情: {error_detail}")
            continue
            
    return f"获取失败。最后一次报错详情: {error_detail}"

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
