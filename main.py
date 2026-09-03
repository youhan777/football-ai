import os
import requests
from huggingface_hub import InferenceClient

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY غير موجود")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN غير موجود")

# جلب أحدث أخبار كرة القدم
response = requests.get(
    "https://newsapi.org/v2/everything",
    params={
        "q": "football OR soccer",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY,
    },
    timeout=30,
)

response.raise_for_status()
data = response.json()

articles = data.get("articles", [])

if not articles:
    raise Exception("لم يتم العثور على أخبار")

article = articles[0]

title = article.get("title", "")
description = article.get("description", "")
source = article.get("source", {}).get("name", "")

news_text = f"""
العنوان: {title}
الوصف: {description}
المصدر: {source}
"""

# الذكاء الاصطناعي عبر Hugging Face
client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)

prompt = f"""
أنت محرر محترف لصفحة أخبار كرة القدم.

حوّل الخبر التالي إلى منشور عربي قصير واحترافي وجذاب لإنستغرام.

المطلوب:
- عنوان قصير وجذاب.
- ملخص للخبر في 2 أو 3 جمل.
- لا تخترع أي معلومة.
- أضف 4 هاشتاغات مناسبة.

الخبر:
{news_text}
"""

result = client.chat.completions.create(
  model="Qwen/Qwen2.5-7B-Instruct-1M",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    max_tokens=300,
)

post = result.choices[0].message.content

print("=" * 50)
print("FOOTBALL AI POST")
print("=" * 50)
print(post)
print("=" * 50)
