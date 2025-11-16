from django.urls import path
from .views import home, get_all_categories, detail_category

# Created your main.urls here.

urlpatterns = [
    path('', home, name='home'),
    path('category/', get_all_categories, name='category'),
    path('category/<int:pk>/', detail_category, name='detail'),
]
