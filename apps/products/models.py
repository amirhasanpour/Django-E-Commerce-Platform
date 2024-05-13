from django.db import models
from utils import FileUpload
from django.utils import timezone


class Brand(models.Model):
    brand_title = models.CharField(max_length=100, verbose_name='نام برند')
    file_upload = FileUpload('images', 'brand')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر برند کالا')
    slug = models.SlugField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return self.brand_title
    
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'
        
        
        
class ProductGroup(models.Model):
    group_title = models.CharField(max_length=100, verbose_name='عنوان گروه کالا')
    file_upload = FileUpload('images', 'product_group')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر گروه کالا')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات گروه کالا')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='وضعیت فعال / غیرفعال')
    group_parent = models.ForeignKey("ProductGroup", on_delete=models.CASCADE, verbose_name='والد گروه کالا', blank=True, null=True, related_name='groups')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateField(auto_now=True, verbose_name='تاریخ آخرین بروزرسانی')
    slug = models.SlugField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return self.group_title
    
    class Meta:
        verbose_name = 'گروه کالا'
        verbose_name_plural = 'گروه های کالا'
        
        
        
class Feature(models.Model):
    feature_name = models.CharField(max_length=100, verbose_name='نام ویژگی')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا', related_name='features_of_groups')
    
    def __str__(self) -> str:
        return self.feature_name
    
    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'
        
        
        
class Product(models.Model):
    product_name = models.CharField(max_length=500, verbose_name='نام کالا')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات کالا')
    file_upload = FileUpload('images', 'product')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر کالا')
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت کالا')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا', related_name='products_of_groups')
    features = models.ManyToManyField(Feature, through='ProductFeature')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='برند کالا', null=True, related_name='brands')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='وضعیت فعال / غیرفعال')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateField(auto_now=True, verbose_name='تاریخ آخرین بروزرسانی')
    slug = models.SlugField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return self.product_name
    
    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالا ها'
        
        
        
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name='ویژگی')
    value = models.CharField(max_length=100, verbose_name='مقدار ویژگی کالا')
    
    def __str__(self) -> str:
        return f"{self.product} - {self.feature} : {self.value}"
    
    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی های محصولات'
        
        
        
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا')
    file_upload = FileUpload('images', 'product_gallery')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصاویر کالا')
    
    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'
    
    
    
    
