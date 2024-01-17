from django.urls import path
from .views import eshopHome, about, e_products, product, e_sizes

urlpatterns = [
    path('', eshopHome, name="eshop_home"),
    path('about/', about, name="eshop_about"),
    path('products/', e_products, name="eshop_products"),
    path('products/<str:item>/', product, name="eshop_product"),
    path('sizes/<str:size>/', e_sizes, name="eshop_size"),
]