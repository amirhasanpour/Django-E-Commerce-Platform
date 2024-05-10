from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterUserForm, VerifyRegisterForm
import utils
from .models import CustomUser
from django.contrib import messages


class RegisterUserView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request, "accounts_app/register.html", {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            active_code = utils.create_random_code(5)
            CustomUser.objects.create_user(
                mobile_number = data['mobile_number'],
                active_code = active_code,
                password = data['password1']
            )
            utils.send_sms(data['mobile_number'], f'کد فعالسازی حساب کاربری شما {active_code} می باشد')
            request.session['user_session'] = {
                'active_code': str(active_code),
                'mobile_number': data['mobile_number'],
            }
            messages.success(request, 'کد فعال سازی ارسال شد', 'success')
            return redirect('accounts:verify')
        messages.error(request, 'اطلاعات ارسالی نامعتبر است', 'error')
        
        
class VerifyRegisterCodeView(View):
    def get(self, request, *args, **kwargs):
        form = VerifyRegisterForm()
        return render(request, "accounts_app/verify_register_code.html", {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = VerifyRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            if data['active_code'] == user_session['active_code']:
                user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                user.is_active = True
                user.active_code = utils.create_random_code(5)
                user.save()
                messages.success(request, 'ثبت نام با موفقیت انجام شد', 'success')
                return redirect('main:index')
            else:
                messages.error(request, 'کد فعالسازی وارد شده اشتباه می باشد', 'danger')
                return render(request, "accounts_app/verify_register_code.html", {'form': form})
        messages.error(request, 'اطلاعات ارسالی نامعتبر است', 'danger')
        return render(request, "accounts_app/verify_register_code.html", {'form': form})
        
        
        
        
