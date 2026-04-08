from django.db.models import Q, Subquery, OuterRef
from home.models import Product
import requests

url = "https://dummyjson.com/products?limit=300"
response = requests.get(url)
data = response.json()

for item in data['products']:
    title = item['title']
    description = item['description']
    price = item['price']
    discountPercentage = item['discountPercentage']
    rating = item['rating']
    stock = item['stock']
    brand = item['brand']
    category = item['category']
    thumbnail = item['thumbnail']

    product, created = Product.objects.get_or_create(
        title=title,
        defaults={
            'description': description,
            'price': price,
            'discountPercentage': discountPercentage,
            'rating': rating,
            'stock': stock,
            'brand': brand,
            'category': category,
            'thumbnail': thumbnail
        }
    )

    if created:
        print(f"Created product: {title}")
    else:
        print(f"Product already exists: {title}")