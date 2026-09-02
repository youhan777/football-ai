import os
import requests
from openai import OpenAI

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY غير موجود")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY غير موجود")

# جلب أحدث أخبار كرة القدم
url = "https://newsapi.org/v2/everything"

params = {
    "q": "football OR soccer",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 5,
    "apiKey": NEWS_API_KEY
}

response = requests.get(url, params=params)
data = response.json()

if not data.get("articles"):
    raise Exception("لم يتم العثور على أخبار")

article = data["articles"][0]

title = article.get("title", "")
description = article.get("description", "")
source = article.get("source", {}).get("name", "")

news_text = f"""
العنوان: {title}
الوصف: {description}
المصدر: {source}
"""

# استخدام الذكاء الاصطناعي لصناعة منشور عربي
client = OpenAI(api_key=OPENAI_API_KEY)

prompt = f"""
أنت مسؤول صفحة احترافية لأخبار كرة القدم على إنستغرام.

حوّل الخبر التالي إلى منشور عربي قصير واحترافي وجذاب.

ضع عنوانًا قويًا، ثم ملخصًا قصيرًا.
أضف 3 إلى 5 هاشتاغات مناسبة.
لا تخترع أي معلومات غير موجودة في الخبر.

الخبر:
{news_text}
"""

result = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

post = result.output_text

print("\n" + "=" * 50)
print("NEW FOOTBALL POST")
print("=" * 50)
print(post)
print("=" * 50)
