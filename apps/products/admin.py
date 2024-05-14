from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ManyToManyField
from django.db.models.query import QuerySet
from django.forms.models import ModelMultipleChoiceField
from django.http import HttpRequest, HttpResponse
from .models import Brand, ProductGroup, Product, Feature, ProductFeature
from django.db.models.aggregates import Count
from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description, order_field


# =============================================================================================   


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_title',)
    list_filter = ('brand_title',)
    search_fields = ('brand_title',)
    ordering = ('brand_title',)


# =============================================================================================   


def de_active_product_group(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f"تعداد {res} گروه غیر فعال شد"
    modeladmin.message_user(request, message)
    
#----------------------------------------------------------------------------------------------
    
def active_product_group(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f"تعداد {res} گروه فعال شد"
    modeladmin.message_user(request, message)
    
#----------------------------------------------------------------------------------------------
    
def export_json(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/json')
    serializers.serialize("json", queryset, stream=response)
    return response

#----------------------------------------------------------------------------------------------

class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = ProductGroup
    extra = 1
    
#----------------------------------------------------------------------------------------------

class GroupFilter(SimpleListFilter):
    title = 'گروه محصولات'
    parameter_name = 'group'
    
    def lookups(self, request, model_admin):
        sub_groups = ProductGroup.objects.filter(~Q(group_parent=None))
        groups = set([item.group_parent for item in sub_groups])
        return [(item.id, item.group_title) for item in groups]
    
    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset
    
#----------------------------------------------------------------------------------------------
    
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('group_title', 'is_active', 'group_parent', 'slug', 'register_date', 'update_date', 'count_sub_group', 'count_product_of_group')
    list_filter = (GroupFilter,)
    search_fields = ('group_title',)
    ordering = ('group_parent', 'group_title',)
    inlines = [ProductGroupInstanceInlineAdmin]
    actions = [de_active_product_group, active_product_group, export_json]
    list_editable = ['is_active']
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductGroupAdmin, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(sub_group=Count('groups'))
        qs = qs.annotate(product_of_group=Count('products_of_groups'))
        return qs
    
    @short_description('تعداد زیر گروه ها')
    @order_field('sub_group')   
    def count_sub_group(self, obj):
        return obj.sub_group
    
    @short_description('تعداد کالا های گروه')
    @order_field('product_of_group')
    def count_product_of_group(self, obj):
        return obj.product_of_group
    
    active_product_group.short_description = 'فعال کردن گروه'
    de_active_product_group.short_description = 'غیر فعال کردن گروه'
    export_json.short_description = 'گرفتن خروجی json'
    
    
# =============================================================================================
   

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name',)
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',) 
    
    
# =============================================================================================


def de_active_product(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f"تعداد {res} کالا غیر فعال شد"
    modeladmin.message_user(request, message)
    
#----------------------------------------------------------------------------------------------
    
def active_product(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f"تعداد {res} کالا فعال شد"
    modeladmin.message_user(request, message)
    
#----------------------------------------------------------------------------------------------
    
class ProductFeatureInstanceInlineAdmin(admin.TabularInline):
    model = ProductFeature
    extra = 1
    
#----------------------------------------------------------------------------------------------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'display_products_groups', 'price', 'brand', 'is_active', 'update_date', 'slug',)
    list_filter = (('brand__brand_title', DropdownFilter), ('product_group__group_title',DropdownFilter),)
    search_fields = ('product_name',)
    ordering = ('update_date', 'product_name',)
    inlines = [ProductFeatureInstanceInlineAdmin]
    actions = [de_active_product, active_product]
    list_editable = ['is_active']
    
    active_product.short_description = 'فعال کردن کالا'
    de_active_product.short_description = 'غیر فعال کردن کالا'
    
    def display_products_groups(self, obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])
    
    display_products_groups.short_description = 'گروه های کالا'
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs["queryset"] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    fieldsets=(
        ('اطلاعات محصول', {'fields':(
            'product_name',
            'image_name',
            'brand',
            ('product_group', 'is_active',),
            'price',
            'description',
            'slug',
            )}),
        ('تاریخ وزمان', {'fields': (
            'published_date',
            )}),
    )
