from django.urls import path
from .views import EhomePageView, EaboutPageView, ShopProducts, ProductFiltered

urlpatterns = [
    path('', EhomePageView.as_view(), name="eshop_home"),
    path('about/', EaboutPageView.as_view(), name="eshop_about"),
    path('products/', ShopProducts.as_view(), name="eshop_products"),
    path('products/<str:filter>/<str:value>/', ProductFiltered.as_view(), name="eshop_filtered"),
]