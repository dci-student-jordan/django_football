from django.urls import reverse


def shop_link():
    url=reverse("eshop_home")
    return f"""</br>
                <h5><a href={url}>Wanna buy from our online Shop?</a></h5>
                """

def top_links(exclude_request, app):
    """Navigation links excluding the calling page."""
    urls = []
    prefix=""
    if "team" in app:
        if len(app) > 1:
            prefix = "Team: "
        for url in [
            (reverse("home_page"), prefix+"Home"),
            (reverse("about_page"), prefix+"About"),
            (reverse("team_page"), prefix+"Team"),
            (reverse("scores_page"), prefix+"Goals per player"),
            (reverse("seasons_page"), prefix+"Seasons"),
            (reverse("games_page"), prefix+"Games"),
        ]:
            urls.append(url)
    if "eshop" in app:
        if len(app) > 1:
            prefix = "eShop: "
        for url in [
            (reverse("eshop_home"), prefix+"Home"),
            (reverse("eshop_about"), prefix+"About"),
            (reverse("eshop_products"), prefix+"Products"),
        ]:
            urls.append(url)
    returnded_urls = ""
    for url in [url for url in urls if not url[0] == exclude_request]:
        returnded_urls += f'<li><a href={url[0]} class="dropdown-item btn-lg">{url[1]}</a></li>'
    return returnded_urls


def team_site():
    url=reverse("home_page")
    return f"""</br>
                <h5><a href={url}>Our favorite Team</a></h5>
                """
