from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('cheapest_products/', views.get_cheapest_products, name='cheapest_products'),
    path('last_products/', views.get_last_products, name='last_products'),
    path('popular_product_groups/', views.get_popular_product_groups, name='popular_product_groups'),
    path('product_details/<slug:slug>/', views.ProductDetailView.as_view(), name='product_details'),
    path('related_products/<slug:slug>/', views.get_related_products, name='related_products'),
    path('product_groups/', views.ProductGroupsView.as_view(), name='product_groups'),
    path('products_of_group/<slug:slug>/', views.ProductsByGroupView.as_view(), name='products_of_group'),
]