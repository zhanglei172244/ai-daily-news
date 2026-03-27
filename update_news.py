import os
import google.generativeai as genai
from datetime import datetime

# 1. 配置 Gemini AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def get_ai_insight():
    # 这里你可以接入 RSS 订阅源，或者简单让 Gemini 搜索最新资讯
    prompt = "请帮我搜集2026年3月26日全球AI相关的10条国内动态、10条国外动态，并分析AI相关股票的买卖建议。请直接以HTML格式输出内容。"
    response = model.generate_content(prompt)
    return response.text

def update_html(content):
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # 这里使用简单的字符串替换，将 AI 生成的内容填入 HTML 模板
    # 实际操作中可以用 BeautifulSoup 等库进行精准替换
    new_html = html.replace("", content)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)

if __name__ == "__main__":
    content = get_ai_insight()
    update_html(content)
