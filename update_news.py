import os
import google.generativeai as genai
from datetime import datetime

# 1. 配置 Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def get_ai_content():
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请整理：1.国内AI动态10条；2.国外AI动态10条；3.卫龙(09985.HK)2025年报派息0.17元的持股建议。直接输出文字，不要包含HTML标签或代码块符号。"
    try:
        # 强制指定版本（如果 SDK 较旧，这行能起作用）
        response = model.generate_content(prompt)
        text = response.text
        # 过滤掉 AI 可能自带的 markdown 标记
        clean_text = text.replace("```html", "").replace("```", "").strip()
        return clean_text
    except Exception as e:
        return f"资讯获取失败，请检查 API 配置或稍后再试。错误信息: {str(e)}"

def generate_full_html(ai_text):
    # 这是我为你重新设计的响应式精美模板
    today_str = datetime.now().strftime('%Y年%m月%d日')
    
    # 将 AI 的纯文本简单处理成 HTML 段落
    formatted_text = ai_text.replace("\n", "<br>")
    
    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI 资讯日报 - {today_str}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #f3f4f6; font-family: sans-serif; }}
            .content-box {{ white-space: pre-wrap; line-height: 1.8; }}
        </style>
    </head>
    <body class="p-4 md:p-8">
        <div class="max-w-4xl mx-auto bg-white shadow-xl rounded-2xl overflow-hidden">
            <header class="bg-slate-900 text-white p-6">
                <h1 class="text-2xl font-bold">AI 资讯每日精选</h1>
                <p class="text-slate-400 mt-2">更新时间：{today_str}</p>
            </header>
            <main class="p-6 md:p-10 content-box text-slate-700">
                {formatted_text}
            </main>
            <footer class="bg-slate-50 p-6 text-center text-slate-400 text-sm border-t">
                数据由 Gemini AI 驱动生成 · 仅供参考
            </footer>
        </div>
    </body>
    </html>
    """
    return full_html

if __name__ == "__main__":
    print("正在通过 Gemini 获取今日最新资讯...")
    raw_ai_text = get_ai_content()
    
    print("正在生成全量网页文件...")
    final_html = generate_full_html(raw_ai_text)
    
    # 直接覆盖写入 index.html，不玩替换，简单粗暴最有效
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print("✅ 任务完成！index.html 已重新生成。")
