import json

# 模拟新闻（后面会换成真实数据）
news = [
    "NVIDIA earnings beat expectations driven by AI demand",
    "AI datacenter expansion increases demand for HBM memory",
    "TSMC reports advanced node capacity remains tight"
]

def extract_theme(text):
    text = text.lower()
    if "ai" in text:
        return "AI demand"
    if "earnings" in text:
        return "earnings"
    if "tsmc" in text or "capacity" in text:
        return "chip supply"
    return "other"

def find_bottleneck(theme):
    if theme == "AI demand":
        return "GPU / HBM / 先进制程产能"
    if theme == "chip supply":
        return "半导体产能紧张"
    return "未知"

def map_stocks(bottleneck):
    if "GPU" in bottleneck:
        return ["NVDA", "AMD", "AVGO"]
    if "HBM" in bottleneck:
        return ["MU", "SK Hynix"]
    if "半导体" in bottleneck:
        return ["TSM", "ASML"]
    return []

def main():
    themes = [extract_theme(n) for n in news]
    theme = max(set(themes), key=themes.count)

    bottleneck = find_bottleneck(theme)
    stocks = map_stocks(bottleneck)

    result = {
        "市场状态": "risk_on",
        "主题": theme,
        "瓶颈": bottleneck,
        "推荐股票": stocks
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
