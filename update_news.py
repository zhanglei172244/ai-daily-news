import os
import sys
import subprocess
from datetime import datetime

# --- 1. 暴力补丁：强制在运行瞬间环境脱胎换骨 ---
def force_update_env():
    try:
        # 尝试清理旧库并安装最新版官方新库
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "google-generativeai"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai", "--force-reinstall"])
        print("✅ 环境暴力升级成功！")
    except Exception as e:
        print(f"⚠️ 环境升级异常（可能已是最新）: {e}")

# 执行升级
force_update_env()

# 升级后导入真正的官方新库
from google import genai

def get_ai_content():
    # 使用全新的 Client 模式，它默认只走 v1 正式接口
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请整理：1.国内AI动态10条；2.国外AI动态10条；3.卫龙(09985.HK)2025年报派息0.17元的持股建议。直接输出文字内容。"
    
    try:
        print("正在通过新版 API 请求资讯...")
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        if response.text:
            return response.text.strip()
    except Exception as e:
        return f"获取失败。报错：{str(e)}"
    return "未获取到有效内容"

def generate_full_html(ai_text):
    # 增加时间戳，确保每次内容都有变化，Git 才会允许提交
    today_str = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    formatted_text = ai_text.replace("\n", "<br>")
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8"><title>AI 资讯日报 - {today_str}</title>
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
    print("✅ 任务最终完成！")
