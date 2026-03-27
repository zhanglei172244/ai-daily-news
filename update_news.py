import os
import google.generativeai as genai
from datetime import datetime

# 1. 配置 Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_ai_content():
    # 这里的指令要求 AI 必须返回纯粹的内容，我会用代码给它套上精美的皮肤
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"今天是{today}。请作为财经分析师整理：1.国内AI动态10条；2.国外AI动态10条；3.NVDA/MSFT/AAPL股价建议；4.卫龙(09985.HK)2025年报派息0.17元的深度简析。请直接分段输出内容，不要包含HTML标签，不要有代码块符号。"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"资讯获取失败: {str(e)}"

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
