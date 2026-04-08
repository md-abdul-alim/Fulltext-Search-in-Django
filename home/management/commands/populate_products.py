from django.core.management.base import BaseCommand
import requests
from home.models import Product

class Command(BaseCommand):
    help = 'Populate products from dummyjson API'

    def handle(self, *args, **options):
        url = "https://dummyjson.com/products?limit=2000"
        response = requests.get(url)
        data = response.json()
        print('data length: ', len(data['products']))
        for item in data['products']:
            product, created = Product.objects.get_or_create(
                title=item['title'],
                defaults={
                    'description': item['description'],
                    'price': item['price'],
                    'discountPercentage': item['discountPercentage'],
                    'rating': item['rating'],
                    'stock': item['stock'],
                    'sku': item['sku'],
                    'category': item['category'],
                    'thumbnail': item['thumbnail']
                }
            )

            if created:
                self.stdout.write(f"Created product: {item['title']}")
            else:
                self.stdout.write(f"Product already exists: {item['title']}")

        self.stdout.write(self.style.SUCCESS('Successfully populated products'))