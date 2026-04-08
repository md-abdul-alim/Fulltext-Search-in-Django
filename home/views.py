from django.shortcuts import render
from .models import Product
from django.contrib.postgres.search import SearchVector

def index(request):
    search = request.GET.get('search', '')

    if search:
        products = Product.objects.annotate(
            search=SearchVector('title', 'description', 'category')
        ).filter(search=search)
    else:
        products = Product.objects.all()
    
    return render(request, 'index.html', {'products': products, 'search': search})