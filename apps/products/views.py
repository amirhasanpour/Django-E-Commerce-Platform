from django.shortcuts import render, get_object_or_404
from .models import Product, ProductGroup
from django.db.models import Q, Count
from django.views import View



def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))



# Cheapest Products
def get_cheapest_products(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('price')[:5]
    product_groups = get_root_group()
    context = {
        'products': products,
        'product_groups': product_groups,
    }
    return render(request, 'products_app/partials/cheapest_products.html', context)



# Last Products
def get_last_products(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('-published_date')[:5]
    product_groups = get_root_group()
    context = {
        'products': products,
        'product_groups': product_groups,
    }
    return render(request, 'products_app/partials/last_products.html', context)



# Popular Groups
def get_popular_product_groups(request, *args, **kwargs):
    product_groups = ProductGroup.objects.filter(Q(is_active=True)\
        & ~Q(group_parent=None)).annotate(count=Count('products_of_groups'))\
            .order_by('-count')[:6]
    context = {
        'product_groups': product_groups,
    }
    return render(request, 'products_app/partials/popular_product_groups.html', context)



# Product Details
class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if product.is_active:
            return render(request, 'products_app/product_detail.html', {'product': product})
        
        

# Related Products   
def get_related_products(request, *args, **kwargs):
    current_product = get_object_or_404(Product, slug=kwargs['slug'])
    related_products = []
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))
    return render(request, 'products_app/partials/related_products.html', {'related_products': related_products})



# Product Groups
class ProductGroupsView(View):
    def get(self, request):
        product_groups = ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_groups'))\
            .order_by('-count')
        return render(request, 'products_app/product_groups.html', {'product_groups': product_groups})



# Show the Products of Group
class ProductsByGroupView(View):
    def get(self, request, *args, **kwargs):
        current_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
        products_of_group = Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))
        return render(request, 'products_app/products_of_group.html', {'products_of_group': products_of_group, 'current_group': current_group})
