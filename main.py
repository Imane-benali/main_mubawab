from bs4 import BeautifulSoup
import requests


def get_page(url):
    return requests.get(url)


def get_soup(url):
    page = get_page(url)
    return BeautifulSoup(page.content, "html.parser")


def get_regions(soup):
    regions = soup.find("div", class_="item-list").find("ul").find_all("li")
    links = []
    for region in regions:
        link = region.find("a")['href']
        if "/mpr/" in link:
            soup = get_soup(link)
            link = soup.find("div", class_="col-8 vAlignM").find_all('a')[-1]['href']
        links.append(link)
    return links


def get_nbr_pages(soup):
    pages = soup.find("div", class_="paginationDots sMargTop centered")
    if pages is None:
        return 1
    else:
        return int(pages.find_all('a')[-2].text)


def remove_white_space(text):
    return text.strip().replace("\n", '').replace('\t', '')


def get_post(soup):
    price = soup.find("h3", class_="orangeTit")
    title = remove_white_space(soup.find("h1", class_="searchTitle").text)
    surface = soup.find("span", class_="tagProp")
    if surface is None:
        surface = "No surface specified"
    else:
        surface = remove_white_space(surface.text)
    description = remove_white_space(soup.find("div", class_='col-8 floatR').select("div.blockProp p")[0].text)
    img_links = []
    try:
        ls_img = soup.find("div", class_="bottomWrapper").select("div.bottomPicture img")
        for img in ls_img:
            img_links.append(img['src'])
    except:
        pass

    if price is None:
        price = 'No price specified'
    else:
        price = remove_white_space(price.text)

    post = {
        'price': price,
        'title': title,
        'description': description,
        'surface': surface,
        'images': img_links
    }

    return post


def get_posts(soup):
    link_posts = soup.find("ul", class_="ulListing").find_all("li", class_='listingBox w100')
    posts = []
    for post in link_posts:
        soup = get_soup(post['linkref'])
        posts.append(get_post(soup))

    return posts


if __name__ == '__main__':
    urls = [
        "https://www.mubawab.ma/fr/mp/terrains-a-vendre",
        "https://www.mubawab.ma/fr/mp/terrains-a-louer"
    ]

    links = []
    all_posts = []
    for url in urls:
        soup = get_soup(url)
        links += get_regions(soup)

    for link in links:
        soup = get_soup(link)
        nbr_pages = get_nbr_pages(soup)

        for i in range(1, 2):
            soup = get_soup(link + ":p:" + str(i))
            all_posts += get_posts(soup)

    print(all_posts)

