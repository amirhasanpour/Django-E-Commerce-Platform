from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator



class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا', related_name='comments_product')
    commenting_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر نظر دهنده', related_name='comments_user1')
    approving_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کاربر تایید کننده نظر', related_name='comments_user2')
    comment_text = models.TextField(verbose_name='متن نظر')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت نظر')
    comment_parent = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='والد نطر', related_name='comment_child')
    
    def __str__(self) -> str:
        return f"{self.product} - {self.commenting_user}"
    
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
