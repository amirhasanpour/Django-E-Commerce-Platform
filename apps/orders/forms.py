from django import forms
from .models import PaymentType



class OrderForm(forms.Form):
    name = forms.CharField(label="",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
                           error_messages={'required': 'این فیلد نمی تواند خالی بماند'})
    
    family = forms.CharField(label="",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
                           error_messages={'required': 'این فیلد نمی تواند خالی بماند'})
    
    email = forms.CharField(label="",
                           widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
                           required=False)
    
    phone_number = forms.CharField(label="",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تلفن'}),
                           required=False)
    
    address = forms.CharField(label="",
                           widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'آدرس', 'rows': 2}),
                           error_messages={'required': 'این فیلد نمی تواند خالی بماند'})
    
    description = forms.CharField(label="",
                           widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'توضیحات سفارش', 'rows': 4}),
                           required=False)
    
    # payment_type = forms.ChoiceField(choices=[(item.pk, item) for item in PaymentType.objects.all()],
    #                                 widget=forms.RadioSelect())
    
    