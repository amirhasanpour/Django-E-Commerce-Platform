from django.db import models
from apps.orders.models import Order
from apps.accounts.models import Customer
from django.utils import timezone



class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش', related_name='payment_order')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='مشتری', related_name='payment_customer')
    register_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ پرداخت')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش پرداخت')
    amount = models.IntegerField(verbose_name='مبلغ پرداخت')
    description = models.TextField(verbose_name='توضیحات پرداخت')
    is_finally = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    status_code = models.IntegerField(null=True, blank=True, verbose_name='کد وضعیت درگاه پرداخت')
    ref_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='شماره پیگیری پرداخت')
    
    def __str__(self) -> str:
        return f"{self.order} {self.customer} {self.ref_id}"
    
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'
