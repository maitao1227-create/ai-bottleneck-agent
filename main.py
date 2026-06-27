import os
import xml.etree.ElementTree as ET
import requests

# ==================== 1. 基础配置 ====================
# 如果你使用中转或者官方OpenAI，在这里配置。本地测试建议先确保网络通畅
API_KEY = os.environ.get("OPENAI_API_KEY", "你的_OPENAI_API_KEY")
BASE_URL = "https://api.openai.com/v1/chat/completions"  # 如果用了中转可以改这里


def fetch_bottleneck_news():
    """
    步骤 1: 抓取宏观与产业技术动态
    使用 Google RSS 搜索包含 'shortage' (短缺) 或 'bottleneck' (瓶颈) 的 AI 产业新闻
    """
    print("📡 正在获取最新的产业瓶颈线索...")
    url = "https://news.google.com/rss/search?q=AI+industry+bottleneck+OR+shortage&hl=en-US&gl=US&ceid=US:en"

    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"❌ 无法获取新闻，状态码: {response.status_code}")
            return []

        # 解析 RSS XML
        root = ET.fromstring(response.content)
        news_list = []
        for item in root.findall(".//item")[:5]:  # 先取前5条做测试
            title = item.find("title").text
            link = item.find("link").text
            news_list.append({"title": title, "link": link})
        return news_list
    except Exception as e:
        print(f"❌ 网络请求发生错误: {e}")
        return []


def analyze_bottleneck(news_title):
    """
    步骤 2 & 3: 投研 Agent 核心逻辑
    让大模型充当“瓶颈分析师”，推导产业链卡点和潜在股票
    """
    if not API_KEY or API_KEY == "你的_OPENAI_API_KEY":
        print("⚠️ 未配置 API Key，跳过 AI 分析阶段。")
        return

    print(f"\n🧠 正在深度剖析线索: {news_title}")

    prompt = f"""
你是一名资深的“产业链瓶颈”投资专家（推崇寻找行业不可或缺的卡位节点）。
请针对以下新闻线索，进行深度的投研逻辑推导：

新闻线索：{news_title}

请按以下框架分析：
1. 【瓶颈识别】：该线索反映了AI或科技产业链上的哪个“瓶颈”或“卡脖子”环节？
2. 【上下游传导】：如果这个瓶颈持续，哪个下游行业最受制于人？哪个环节掌握了定价权？
3. 【卡位标的】：在 A股、港股 或 美股中，有哪些上市公司真正拥有解决该瓶颈的核心技术/资产（寻找真正的“隐形冠军”或垄断者）？
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4o-mini",  # 先用便宜的模型测试流程
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,  # 降低随机性，让投研逻辑更严谨
    }

    try:
        res = requests.post(BASE_URL, json=data, headers=headers, timeout=30)
        result = res.json()
        analysis = result["choices"][0]["message"]["content"]
        print("-" * 50)
        print(analysis)
        print("-" * 50)
    except Exception as e:
        print(f"❌ 调用 AI 接口失败: {e}")


# ==================== 主程序入口 ====================
if __name__ == "__main__":
    # 1. 抓取数据
    news = fetch_bottleneck_news()

    if news:
        print(f"✅ 成功抓取到 {len(news)} 条潜在瓶颈线索。\n")
        # 2. 拿第一条线索让 Agent 跑一次闭环测试
        analyze_bottleneck(news[0]["title"])
    else:
        print("❌ 未获取到有效线索，请检查本地网络是否能直连 Google RSS。")
