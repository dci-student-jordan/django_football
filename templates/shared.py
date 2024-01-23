from django.urls import reverse


def shop_link():
    url=reverse("eshop_home")
    return f"""</br>
                <h3>Wanna buy from our online Shop?</h3>
                <a href={url}>e-Shop</a>"""

def top_links(exclude_request, app):
    """Navigation links excluding the calling page."""
    if app == "team":
        urls =[
            (reverse("home_page"), "Home"),
            (reverse("about_page"), f"About"),
            (reverse("team_page"), f"Team"),
            (reverse("scores_page"), f"Goals per player"),
            (reverse("seasons_page"), f"Seasons")
        ]
    elif app == "eshop":
        urls =[

            (reverse("eshop_home"), "Home"),
            (reverse("eshop_about"), f"About"),
            (reverse("eshop_products"), f"Products"),
        ]
    returnded_urls = ""
    for url in [url for url in urls if not url[0] == exclude_request]:
        returnded_urls += f"<a href={url[0]}>{url[1]}</a></br>"
    return returnded_urls


def team_site():
    url=reverse("home_page")
    return f"""</br>
                <h3>Our favorite Team:</h3>
                <a href={url}>homepage</a>"""
