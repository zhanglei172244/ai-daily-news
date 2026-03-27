import os
import google.generativeai as genai
from datetime import datetime

# 1. 配置 Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# 修复 404 报错：手动指定更稳定的模型名称
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_ai_content():
    prompt = """
    请作为一名专业的财经与科技分析师，完成以下任务：
    1. 搜索并整理2026年3月26日最新的AI资讯：国内10条，国外10条。
    2. 提供AI相关股票（NVDA, MSFT, AAPL等）的买卖建议。
    3. 特别包含：卫龙(09985.HK)2025年报深度解读，包括每股0.17元的派息分析和持股建议。
    4. 输出要求：只输出 HTML 代码片段，使用 <div> 和 <li> 标签，不要包含 <html> 或 <body>。
    """
    try:
        # 使用最通用的生成方法
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"<div class='p-4 text-red-500'>内容抓取失败: {str(e)}</div>"

def update_web_page(new_content):
    # 读取原始模板
    if not os.path.exists("index.html"):
        print("未找到 index.html 文件")
        return

    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 替换占位符
    placeholder = ""
    if placeholder in content:
        # 清除可能存在的旧 AI 内容，保持模板干净
        # 这种逻辑会保留头部和尾部，只替换中间部分
        parts = content.split(placeholder)
        updated_content = parts[0] + placeholder + "\n" + new_content + "\n" + parts[1]
    else:
        # 如果没找到占位符，直接追加（保底方案）
        updated_content = content + "\n" + new_content

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    print("正在获取最新 AI 资讯和卫龙年报分析...")
    news_html = get_ai_content()
    update_web_page(news_html)
    print("网页内容已更新。")
