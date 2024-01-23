from django.urls import path
from .views import EhomePageView, EaboutPageView, ShopProducts, ProductDetail, ProductSizes

urlpatterns = [
    path('', EhomePageView.as_view(), name="eshop_home"),
    path('about/', EaboutPageView.as_view(), name="eshop_about"),
    path('products/', ShopProducts.as_view(), name="eshop_products"),
    path('products/<str:item>/', ProductDetail.as_view(), name="eshop_product"),
    path('sizes/<str:size>/', ProductSizes.as_view(), name="eshop_size"),
]