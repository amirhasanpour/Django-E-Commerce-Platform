from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductGroup, FeatureValue, Brand
from django.db.models import Q, Count, Min, Max
from django.views import View
from django.http import JsonResponse
from .filters import ProductFilter
from django.core.paginator import Paginator
from .compare import CompareProduct
from django.http import HttpResponse


#----------------------------------------------------------------------------------------------



def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))



#----------------------------------------------------------------------------------------------



# Cheapest products
def get_cheapest_products(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('price')[:5]
    product_groups = get_root_group()
    context = {
        'products': products,
        'product_groups': product_groups,
    }
    return render(request, 'products_app/partials/cheapest_products.html', context)



#----------------------------------------------------------------------------------------------



# Last products
def get_last_products(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('-published_date')[:5]
    product_groups = get_root_group()
    context = {
        'products': products,
        'product_groups': product_groups,
    }
    return render(request, 'products_app/partials/last_products.html', context)



#----------------------------------------------------------------------------------------------



# Popular groups
def get_popular_product_groups(request, *args, **kwargs):
    product_groups = ProductGroup.objects.filter(Q(is_active=True)\
        & ~Q(group_parent=None)).annotate(count=Count('products_of_groups'))\
            .order_by('-count')[:6]
    context = {
        'product_groups': product_groups,
    }
    return render(request, 'products_app/partials/popular_product_groups.html', context)



#----------------------------------------------------------------------------------------------



# Product details
class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if product.is_active:
            return render(request, 'products_app/product_detail.html', {'product': product})
        
        
        
#----------------------------------------------------------------------------------------------
        
        

# Related products   
def get_related_products(request, *args, **kwargs):
    current_product = get_object_or_404(Product, slug=kwargs['slug'])
    related_products = []
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))
    return render(request, 'products_app/partials/related_products.html', {'related_products': related_products})



#----------------------------------------------------------------------------------------------



# Count of thr products in groups
class ProductGroupsView(View):
    def get(self, request):
        product_groups = ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_groups'))\
            .order_by('-count')
        return render(request, 'products_app/product_groups.html', {'product_groups': product_groups})
    
    
    
#----------------------------------------------------------------------------------------------



# Show the products of group
class ProductsByGroupView(View):
    def get(self, request, *args, **kwargs):
        slug=kwargs['slug']
        current_group = get_object_or_404(ProductGroup, slug=slug)
        products_of_group = Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))
        
        res_aggre = products_of_group.aggregate(min=Min('price'), max=Max('price'))
        
        # price filter
        filter = ProductFilter(request.GET, queryset=products_of_group)
        products_of_group = filter.qs
        
        # brand filter
        brand_filter = request.GET.getlist('brand')
        if brand_filter:
            products_of_group = products_of_group.filter(brand__id__in=brand_filter)
            
        # feature filter
        feature_filter = request.GET.getlist('feature')
        if feature_filter:
            products_of_group = products_of_group.filter(product_features__filter_value__id__in=feature_filter).distinct()
            
        # sort type
        sort_type = request.GET.get('sort_type')
        if not sort_type:
            sort_type = "0"
        if sort_type == "1":
            products_of_group = products_of_group.order_by('price')
        elif sort_type == "2":
            products_of_group = products_of_group.order_by('-price')
            
        group_slug = slug
        product_per_page = 2                                                   # the number of product in each page
        paginator = Paginator(products_of_group, product_per_page)
        page_number = request.GET.get('page')                                  # get the number of current page
        page_obj = paginator.get_page(page_number)                             # the list of the products after pagination for showing in current page
        product_count = products_of_group.count()                              # all of the available products in current group
        
        # list of the numbers for creating drop-down menue, for set number of products in each page, by user
        show_count_product = []
        i = product_per_page
        while i < product_count:
            show_count_product.append(i)
            i *= 2
        show_count_product.append(i)
        
        
        context = {
            'products_of_group': products_of_group,
            'current_group': current_group,
            'res_aggre': res_aggre,
            'group_slug': group_slug,
            'page_obj': page_obj,
            'product_count': product_count,
            'filter': filter,
            'sort_type': sort_type,
            'show_count_product': show_count_product,
        }
        
        return render(request, 'products_app/products_of_group.html', context)
    
    
    
#----------------------------------------------------------------------------------------------
    
    
    
# Two sync dropdown in admin panel
def get_filter_value_for_feature(request):
    if request.method == 'GET':
        feature_id = request.GET.get("feature_id")
        print('*'*50)
        print(feature_id)
        print('*'*50)
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        print(feature_values)
        res = {fv.value_title:fv.id for fv in feature_values}
        print(res)
        return JsonResponse(data=res, safe=False)
    
    
    
#----------------------------------------------------------------------------------------------
    
    
    
# Product group list for filtering
def get_product_groups(request):
    product_groups = ProductGroup.objects.annotate(count=Count('products_of_groups'))\
        .filter(Q(is_active=True) & ~Q(count=0))\
        .order_by('-count')
    return render(request, 'products_app/partials/product_groups.html', {'product_groups': product_groups})



#----------------------------------------------------------------------------------------------



# List of brands for filtering
def get_brands(request, *args, **kwargs):
        product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
        brand_list_id = product_group.products_of_groups.filter(is_active=True).values('brand_id')
        brands = Brand.objects.filter(pk__in=brand_list_id)\
            .annotate(count=Count('brands'))\
            .filter(~Q(count=0))\
            .order_by('-count')
        
        return render(request, 'products_app/partials/brands.html', {'brands': brands})
    
    
    
#----------------------------------------------------------------------------------------------
    
    
    
# Feature values for a special product group for filtering
def get_features_for_filter(request, *args, **kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    feature_list = product_group.features_of_groups.all()
    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature]=feature.feature_values.all()
    return render(request, 'products_app/partials/feature_filter.html', {'feature_dict': feature_dict})



#----------------------------------------------------------------------------------------------



# get the compare products
class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        compare_list = CompareProduct(request)
        return render(request, 'products_app/compare_list.html', {'compare_list': compare_list})
    


#----------------------------------------------------------------------------------------------



# show the compare products in compare table
def compare_table(request):
    compareList = CompareProduct(request)
    
    products = []
    for productId in compareList.compare_product:
        product = Product.objects.get(id=productId)
        products.append(product)
        
    features = []
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)
                
    context = {
        'products': products,
        'features': features,
    }
    
    return render(request, 'products_app/partials/compare_table.html', context)



#----------------------------------------------------------------------------------------------



# count of the products in compare list
def status_of_compare_list(request):
    compareList = CompareProduct(request)
    return HttpResponse(compareList.count)


#----------------------------------------------------------------------------------------------



# add product to compare list
def add_to_compare_list(request):
    productId = request.GET.get('productId')
    compareList = CompareProduct(request)
    compareList.add_to_compare_product(productId)
    return HttpResponse('کالا به لیست مقایسه اضافه شد')



#----------------------------------------------------------------------------------------------



# delete product from compare list
def delete_from_compare_list(request):
    productId = request.GET.get('productId')
    compareList = CompareProduct(request)
    compareList.delete_from_compare_product(productId)
    return redirect('products:compare_table')
