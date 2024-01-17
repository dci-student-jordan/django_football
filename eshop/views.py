from django.shortcuts import HttpResponse, redirect
from django.urls import reverse
from .models import Item

# Create your views here.

def team_site():
    url=reverse("home_page")
    return f"""</br>
                <h3>Our favorite Team:</h3>
                <a href={url}>homepage</a>"""


def url_for_size(size):
    return f"<a href={reverse('eshop_size', args=[size])}>{size}</a>"

def eshopHome(request):
    url1=reverse("eshop_about")
    url2=reverse("eshop_products")
    page = f"""
     <!DOCTYPE html>
        <html>
            <body>

                <h1>Welcome to the e-Shop of our favorite Team!</h1>
                <a href={url1}>about</a><br>
                <a href={url2}>Products</a>
                {team_site()}
            </body>
        </html> 
    """
    return HttpResponse(page)

def about(request):
    url1=reverse("eshop_home")
    page = f"""
     <!DOCTYPE html>
        <html>
            <body>

                <h1>About e-Shop</h1>
                <a href={url1}>e-Shop home</a>
                <p>CONTACT</p>
                {team_site()}
            </body>
        </html> 
    """
    return HttpResponse(page)

def e_products(request):
    """List all products counted as links to product-page"""
    url1=reverse("eshop_home")
    url2=reverse("eshop_about")
    products = Item.objects.values_list("item", flat=True)
    page_part1 = f"""
     <!DOCTYPE html>
        <html>
            <body>

                <a href={url1}>e-Shop home</a><br>
                <a href={url2}>about e-Shop</a>
                <h1>Here are our products:</h1>
                <h3>For sorted by size chose here:</h3>
                <p>{url_for_size('XS')} | {url_for_size('S')} | {url_for_size('M')} | {url_for_size('L')} | {url_for_size('XL')}</p>
                <ul>"""
    
    for product in list(products.distinct()):
        num_prod = Item.objects.filter(item=product).count()
        product_url = reverse("eshop_product", args=[product])
        page_part1 += f"""<li>
                            <h3><a href={product_url}>{product}</a></h3>
                            <p>Available: {num_prod}</p>
                        </li>"""
    
    page_part2 = f"""
                </ul>
                {team_site()}
            </body>
        </html> 
    """
    return HttpResponse(page_part1+page_part2)

def product(request, item):
    url = reverse("eshop_home")
    url2 = reverse("eshop_products")
    shop_items = Item.objects.filter(item=item)
    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{item}</title>
    </head>
    <body>
    <a href = "{url}">eShop Home</a></br>
    <a href = "{url2}">Products</a>
    <h1>Available {item}{'s' if not item[-1] == 's' else ''}:</h1><ol>"""
    index = 1
    for itm in shop_items:
        page += f"""
        <li>
            <h3>{item} {index}:</h3>
            <p>DESCRIPTION: {itm.description}</p>
            <p>SIZE: {url_for_size(itm.size)}</p>
            <p>PRICE: {itm.price}</p>
        </li>"""
        index += 1
    page += f"""</ol>
    {team_site()}
    </body>
    </html>
    """
    return HttpResponse(page)

def e_sizes(request, size):
    url = reverse("eshop_home")
    url2 = reverse("eshop_products")
    shop_items = Item.objects.filter(size=size)
    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{size}</title>
    </head>
    <body>
    <a href = "{url}">eShop Home</a></br>
    <a href = "{url2}">Products</a>
    <h1>Available Products of size {size}:</h1><ol>"""
    for itm in shop_items:
        page += f"""
        <li>
            <h3>{itm.item}:</h3>
            <p>DESCRIPTION: {itm.description}</p>
            <p>PRICE: {itm.price}</p>
        </li>"""
    page += f"""</ol>
    {team_site()}
    </body>
    </html>
    """
    return HttpResponse(page)