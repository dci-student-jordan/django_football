from django.shortcuts import HttpResponse, redirect
from django.urls import reverse
from .models import Item
from django.db.models import Count
from django.db import connection, reset_queries
from django.views.generic.base import TemplateView
from templates.shared import top_links, team_site
from django.utils.safestring import mark_safe

# Create your views here.

def url_for_size(size):
    return f"<a href={reverse('eshop_size', args=[size])}>{size}</a>"


class EhomePageView(TemplateView):
    template_name = "simple.html"
    def get_context_data(self):
        context = {
            "extra_style":"eshop/style.css",
            "top_header":"Welcome to our favorite team's eshop!",
            "content_text":"Here you can find the best merchandise stuff ever.",
            "navs": mark_safe(top_links(reverse("eshop_home"), "eshop")),
            "foot": mark_safe(team_site())
            }
        return context
        
    
class EaboutPageView(TemplateView):
    template_name = "simple.html"
    def get_context_data(self):
        context = {
            "extra_style":"eshop/style.css",
            "top_header":"About our favorite team's eshop",
            "content_text":"Support our favorite team and... BUY!",
            "navs": mark_safe(top_links(reverse("eshop_about"), "eshop")),
            "foot": mark_safe(team_site())
            }
        return context


class ShopProducts(TemplateView):
    template_name = "products.html"
    def get_context_data(self):
        products = Item.objects.values("item").annotate(count=Count('item'))
        context = {
            "extra_style":"eshop/style.css",
            "products": products,
            "navs": mark_safe(top_links(reverse("eshop_products"), "eshop")),
            "foot": mark_safe(team_site()),
            }
        return context

class ProductDetail(TemplateView):
    template_name = "product_detail.html"
    def get_context_data(self, item):
        products = Item.objects.filter(item=item)
        name = item+('s' if not item[-1] == 's' else '')
        context = {
            "extra_style":"eshop/style.css",
            "products": products,
            "header_name":name,
            "navs": mark_safe(top_links(reverse("eshop_product", args=[name]), "eshop")),
            "foot": mark_safe(team_site()),
            }
        return context

class ProductSizes(TemplateView):
    template_name = "product_sizes.html"
    def get_context_data(self, size):
        products = Item.objects.filter(size=size)
        context = {
            "extra_style":"eshop/style.css",
            "products": products,
            "size":size,
            "navs": mark_safe(top_links(reverse("eshop_size", args=[size]), "eshop")),
            "foot": mark_safe(team_site()),
            }
        return context
