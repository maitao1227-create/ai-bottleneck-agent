import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": "你是一位AI产业投资研究员。"
        },
        {
            "role": "user",
            "content": "请告诉我一句话：AI产业未来最大的瓶颈是什么？"
        }
    ]
)

print(response.choices[0].message.content)
