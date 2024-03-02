from typing import Any
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .models import Item, SIZE_CHOICES
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from templates.shared import top_links, team_site
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormView
from django.views.decorators.http import require_POST
from.forms import OrderModelForm
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


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
            "navs": mark_safe(top_links(reverse("eshop_home"), ["eshop"])),
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
            "navs": mark_safe(top_links(reverse("eshop_about"), ["eshop"])),
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
            "navs": mark_safe(top_links(reverse("eshop_products"), ["eshop"])),
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
            "summary":f"All Our products matching {filter} '{value}':",
            "navs": mark_safe(top_links(reverse("eshop_filtered", args=[filter, value]), ["eshop"])),
            "foot": mark_safe(team_site()),
            }
        return context

class OrderForm(LoginRequiredMixin, FormView):
    template_name = "order.html"
    form_class = OrderModelForm
    interest = ""
    login_url = reverse_lazy('login')  # Set the URL to redirect to for login

    def handle_no_permission(self):
        """Redirects users to the login page if they are not authenticated."""
        return redirect(self.login_url)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        # print(print("\nGET:\n", request, "\n\n", args, "\n\n", kwargs))
        self.interest = request.GET.get("item_id")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        print("\nPOST:\n", request, "\n\n", args, "\n\n", kwargs)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("HERE we go...")
        # Reinitialize the form to ensure it's aware of the dynamic changes
        form.__init__(self.request.POST)
        try:
            # delete from items table
            item = form.cleaned_data['item']
            description = form.cleaned_data['description']
            size = form.cleaned_data['size']
            number = form.cleaned_data['number']
            print("WILL TRY TO DELETE:", (item, description, size, number))
            for _ in range(number):
                delete = Item.objects.filter(item=item, description=description, size=size).first()
                print("WILL DELETE:", delete, (item, description, size))
                delete.delete()
                print("DELETED:", delete)
        except (Exception) as e:
            # something went wrong
            print(e)
            return HttpResponseRedirect("nosuccess")
        else:
            #success
            object = form.save(False)
            object.user = self.request.user
            object.save()
            return HttpResponseRedirect("success")
    
    def get_initial(self):
        initial = super().get_initial()
        if self.interest:
            item = Item.objects.get(id=self.interest)
            initial = item.__dict__
        user = self.request.user
        initial['email'] = user.email

        return initial

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_style"] = "eshop/style.css"
        context["top_header"] = "Your Order:"
        context["content_text"] = "Place your order for the best merchandise stuff ever."
        context["navs"] = mark_safe(top_links(reverse("order"), ["eshop"]))
        context["foot"] = mark_safe(team_site())
        return context

@require_POST
def get_item_details(request):
    '''Update fields in the order form.'''
    item_name = request.POST.get('item_name')
    item_descr = request.POST.get('item_descr')
    item_size = request.POST.get('item_size')
    descriptions = [desc[0] for desc in Item.objects.filter(item=item_name).values_list('description').distinct().order_by('description')]
    if not item_descr in descriptions:
        item_descr = descriptions[0]
    sizes = list(Item.objects.filter(item=item_name, description=item_descr).values_list("size").distinct())
    if not item_size in sizes:
        item_size = sizes[0][0]
    sizes = [size[0] for size in sizes]
    numbers = Item.objects.filter(item=item_name, description=item_descr, size=item_size).count()
    return JsonResponse({'descriptions': descriptions, 'sizes': sizes, 'numbers': numbers})


class SuccessView(TemplateView):
    template_name = "simple.html"
    def get_context_data(self):
        context = {
            "extra_style":"eshop/style.css",
            "top_header":"Thanks!",
            "content_text":"Your order has been successfully placed.",
            "navs": mark_safe(top_links(reverse("success"), ["eshop"])),
            "foot": mark_safe(team_site())
            }
        return context

class NoSuccessView(TemplateView):
    template_name = "simple.html"
    def get_context_data(self):
        context = {
            "extra_style":"eshop/style.css",
            "top_header":"Whoops, so SORRY!",
            "content_text":"Your order could not be placed, you'll have to try again.",
            "navs": mark_safe(top_links(reverse("success"), ["eshop"])),
            "foot": mark_safe(team_site())
            }
        return context