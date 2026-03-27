import os
import google.generativeai as genai
from datetime import datetime

# 1. 配置 Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_ai_content():
    # 增加搜索指令，确保包含最新的卫龙信息
    prompt = f"今天是{datetime.now().strftime('%Y-%m-%d')}。请整理AI动态（国内10条/国外10条），包含NVDA/MSFT股价简析，以及卫龙(09985.HK)2025年报派息分析。请直接输出HTML片段（div/li），不要有代码块符号。"
    try:
        response = model.generate_content(prompt)
        # 清理 AI 可能带出的 ```html 这种标记
        content = response.text.replace("```html", "").replace("```", "").strip()
        return content
    except Exception as e:
        return f"<p>资讯生成失败: {str(e)}</p>"

def update_web_page(new_content):
    if not os.path.exists("index.html"):
        print("警告：未找到 index.html，正在创建新文件...")
        content = "<html><body></body></html>"
    else:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

    placeholder = ""
    
    # 核心逻辑：如果找不到占位符，就强行在文件开头插入一个
    if placeholder not in content:
        print("未在 HTML 中找到占位符，正在自动注入...")
        content = placeholder + content

    # 替换内容
    parts = content.split(placeholder)
    updated_content = parts[0] + placeholder + "\n" + new_content + "\n" + parts[1]

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    print("正在获取资讯并更新网页...")
    news_html = get_ai_content()
    update_web_page(news_html)
    print("✅ 网页更新成功！")
