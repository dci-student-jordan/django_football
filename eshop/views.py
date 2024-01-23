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
    

class ProductFiltered(TemplateView):
    template_name = "product_filtered.html"
    def get_context_data(self, filter, value):
        if filter != 'price':
            args = {filter: value}
            products = Item.objects.filter(**args)
        else:
            products = Item.objects.filter(price__lte=value).order_by("-price")
        context = {
            "extra_style":"eshop/style.css",
            "products": products,
            "blocked":[filter],
            "header_text": f"{filter}: {value}",
            "summary":f"All Our products matching '{value}':",
            "navs": mark_safe(top_links(reverse("eshop_filtered", args=[filter, value]), "eshop")),
            "foot": mark_safe(team_site()),
            }
        return context
