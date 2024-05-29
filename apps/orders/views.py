from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Customer
from .models import Order, OrderDetails, PaymentType
from .forms import OrderForm


class ShopCartView(View):
    def get(self, request, *args, **kwargs):
        shop_cart = ShopCart(request)
        return render(request, 'orders_app/shop_cart.html', {'shop_cart': shop_cart})
    
    
    
def show_shop_cart(request):
    shop_cart = ShopCart(request)
    total_price= shop_cart.calc_total_price()
    delivery = 25000
    if total_price > 1000000:
        delivery = 0
    tax = int(0.03 * total_price)
    order_final_price = total_price + delivery + tax
    context = {
        'shop_cart': shop_cart,
        'shop_cart_count': shop_cart.count,
        'total_price': total_price,
        'delivery': delivery,
        'tax': tax,
        'order_final_price': order_final_price,
    }
    return render(request, 'orders_app/partials/show_shop_cart.html', context)
    
    
    
def add_to_shop_cart(request):
    product_id = request.GET.get('product_id')
    qty = request.GET.get('qty')
    shop_cart = ShopCart(request)
    product = get_object_or_404(Product, id=product_id)
    shop_cart.add_to_shop_cart(product, qty)
    return HttpResponse(shop_cart.count)



def delete_from_shop_cart(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    shop_cart = ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect('orders:show_shop_cart')



def update_shop_cart(request):
    product_id_list = request.GET.getlist('product_id_list[]')
    qty_list = request.GET.getlist('qty_list[]')
    shop_cart = ShopCart(request)
    shop_cart.update_shop_cart(product_id_list, qty_list)
    return redirect('orders:show_shop_cart')



def status_of_shop_cart(request):
    shop_cart = ShopCart(request)
    return HttpResponse(shop_cart.count)



class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        if not customer:
            customer = Customer.objects.create(user=request.user)
        
        order = Order.objects.create(customer=customer, payment_type=get_object_or_404(PaymentType, id=1))
        
        shop_cart = ShopCart(request)
        
        for item in shop_cart:
            OrderDetails.objects.create(
                order = order,
                product = item['product'],
                price = item['price'],
                qty = item['qty']
            )
            
        return redirect('orders:checkout_order', order.id)
    
    
    
class CheckoutOrderView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        shop_cart = ShopCart(request)
        order = get_object_or_404(Order, id=order_id)
        
        total_price= shop_cart.calc_total_price()
        delivery = 25000
        if total_price > 1000000:
            delivery = 0
        tax = int(0.03 * total_price)
        order_final_price = total_price + delivery + tax
        
        data = {
            'name': user.name,
            'family': user.family,
            'email': user.email,
            'phone_number': customer.phone_number,
            'address': customer.address,
            'description': order.description,
            'payment_type': order.payment_type,
        }
        
        form = OrderForm(data)
        
        context = {
            'shop_cart': shop_cart,
            'total_price': total_price,
            'delivery': delivery,
            'tax': tax,
            'order_final_price': order_final_price,
            'form': form,
        }
        
        return render(request, 'orders_app/checkout.html', context)
        
