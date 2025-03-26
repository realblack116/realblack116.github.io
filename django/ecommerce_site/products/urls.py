from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    # ✅ 이 줄 추가
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
