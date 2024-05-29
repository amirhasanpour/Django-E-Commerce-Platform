from django.db import models
from apps.accounts.models import Customer
from apps.products.models import Product
from django.utils import timezone
from uuid import uuid4



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='مشتری')
    register_date = models.DateField(default=timezone.now, verbose_name='تاریخ درج سفارش')
    update_date = models.DateField(auto_now=True, verbose_name='تاریخ ویرایش سفارش')
    is_finaly = models.BooleanField(default=False, verbose_name='نهایی شده')
    order_code = models.UUIDField(unique=True, default=uuid4, editable=False, verbose_name='کد تولیدی برای سفارش')
    discount = models.IntegerField(blank=True, null=True, default=None, verbose_name='تخفیف روی فاکتور')
    
    def __str__(self) -> str:
        return f"{self.customer}\t{self.id}\t{self.is_finaly}"
    
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        
        
        
class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش', related_name='orders_details1')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا', related_name='orders_details2')
    qty = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت کالا در فاکتور')
    
    def __str__(self) -> str:
        return f"{self.order}\t{self.product}\t{self.qty}\t{self.price}"
