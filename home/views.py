from django.shortcuts import render
from django.db.models import Q
from .models import Product
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

SEARCH_TYPES = {
        "plain": "plainto_tsquery",
        "phrase": "phraseto_tsquery",
        "raw": "to_tsquery",
        "websearch": "websearch_to_tsquery",
    }

def index(request):
    search = request.GET.get('search', '')

    # query = SearchQuery(search, search_type='websearch')
    query = SearchQuery(search)
    # vector = SearchVector('title', 'description', 'category', 'sku')
    vector = (
        SearchVector('title', weight='A') +
        SearchVector('description', weight='B') +
        SearchVector('category', weight='C') +
        SearchVector('sku', weight='D')
    )
    rank = SearchRank(vector, query)
    similarity = TrigramSimilarity('title', search) + TrigramSimilarity('description', search) + TrigramSimilarity('category', search) + TrigramSimilarity('sku', search)

    if search:
        products = Product.objects.annotate(
            rank=rank,
            similarity=similarity
        ).filter(Q(rank__gte=0.3) | Q(similarity__gte=0.3)).exclude(rank__isnull=True).distinct().order_by('-rank', '-similarity')
    else:
        products = Product.objects.all()

    if request.GET.get('category'):
        products = products.filter(category__icontains=request.GET['category'])

    if request.GET.get('min_price') and request.GET.get('max_price'):

        min_price = float(request.GET['min_price'].split('$')[1])
        max_price = float(request.GET['max_price'].split('$')[1])
        products = products.filter(price__gte=min_price, price__lte=max_price).order_by('price')

    categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
    
    return render(request, 'index.html', {
        'products': products, 
        'search': search, 
        'categories': categories
        }
    )