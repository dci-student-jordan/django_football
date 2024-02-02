from django.urls import path
from .views import EhomePageView, EaboutPageView, ShopProducts, ProductFiltered, OrderForm, SuccessView, get_item_details, NoSuccessView
from django.contrib.auth import login, logout

urlpatterns = [
    path('', EhomePageView.as_view(), name="eshop_home"),
    path('about/', EaboutPageView.as_view(), name="eshop_about"),
    path('products/', ShopProducts.as_view(), name="eshop_products"),
    path('products/<str:filter>/<str:value>/', ProductFiltered.as_view(), name="eshop_filtered"),
    path("order/", OrderForm.as_view(), name="order"),
    path('order/updated', get_item_details, name='get_item_details'),
    path("order/success/", SuccessView.as_view(), name="success"),
    path("order/nosuccess/", NoSuccessView.as_view(), name="nosuccess"),
]