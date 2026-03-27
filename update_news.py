import os
import requests
import json
from datetime import datetime

def get_ai_content():
    # 获取你在 GitHub Secrets 中配置的 Key
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # 【核心修正】锁定你浏览器验证成功的 v1beta 接口和 gemini-2.0-flash 模型
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    # 获取当前日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 你的定制化需求：AI 动态 + 卫龙持股建议
    prompt = (
        f"今天是{today}。请整理并输出以下内容：\n"
        f"1. 国内 AI 行业重大动态 10 条；\n"
        f"2. 国外 AI 行业重大动态 10 条；\n"
        f"3. 针对卫龙(09985.HK)2025年报建议派息0.17元的持股分析及建议。\n"
        f"请直接输出正文，保持排版整洁。"
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        # 增加超时处理，防止网络波动
        response = requests.post(url, json=payload, timeout=30)
        result = response.json()
        
        # 提取 AI 生成的文字
        if 'candidates' in result:
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            # 如果万一报错，会将详细的 Google 报错信息显示在网页上，方便定位
            return f"获取内容失败。API 报错详情：{json.dumps(result, ensure_ascii=False)}"
    except Exception as e:
        return f"网络连接异常: {str(e)}"

def generate_full_html(ai_text):
    """将获取到的文字包装成精美的网页"""
    today_str = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    # 将换行符转换为网页可识别的换行标签
    formatted_text = ai_text.replace("\n", "<br>")
    
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI 资讯每日精选</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="p-4 md:p-8 bg-slate-50 min-h-screen">
        <div class="max-w-4xl mx-auto bg-white p-6 md:p-10 rounded-2xl shadow-xl border border-slate-100">
            <header class="mb-8 border-b pb-6">
                <h1 class="text-3xl font-extrabold text-slate-800">AI 资讯每日精选</h1>
                <p class="text-slate-500 mt-2 font-medium text-sm">更新时间：{today_str}</p>
            </header>
            
            <article class="prose prose-slate max-w-none text-slate-700 leading-relaxed space-y-4">
                {formatted_text}
            </article>
            
            <footer class="mt-12 pt-6 border-t text-center">
                <p class="text-xs text-slate-400">由 Gemini 2.0 Flash 自动化驱动</p>
            </footer>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    # 执行内容获取
    content = get_ai_content()
    # 写入文件
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generate_full_html(content))
    print("✅ 任务已完成，请在浏览器查看 index.html")
