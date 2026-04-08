from django.shortcuts import render
from .models import Product
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

def index(request):
    search = request.GET.get('search', '')

    query = SearchQuery(search)
    # vector = SearchVector('title', 'description', 'category', 'sku')
    vector = (
        SearchVector('title', weight='A') +
        SearchVector('description', weight='B') +
        SearchVector('category', weight='C') +
        SearchVector('sku', weight='D')
    )
    rank = SearchRank(vector, query)

    if search:
        products = Product.objects.annotate(
            rank=rank
        ).filter(rank__gte=0.05).exclude(rank__isnull=True).order_by('-rank')
    else:
        products = Product.objects.all()
    
    return render(request, 'index.html', {'products': products, 'search': search})