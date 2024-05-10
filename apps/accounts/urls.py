from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('verify/', views.VerifyRegisterCodeView.as_view(), name='verify'),
]
