from django.urls import path
from .views import home, get_all_categories, detail_category, ProductView, ProductDetail

# Created your main.urls here.

urlpatterns = [
    path('', home, name='home'),
    path('category/', get_all_categories, name='category'),
    path('category/<int:pk>/', detail_category, name='category_detail'),
    path('product/', ProductView.as_view(), name='product'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
]
