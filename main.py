

from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os


def start_search():
    search = input("What to you want to search for? Enter search terms: ")
    params = {"q": search}
    dir_name = search.replace(" ", "_").lower()

    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    r = requests.get("http://www.bing.com/images/search", params=params)

    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.findAll("a", {"class": "thumb"})

    for item in links:
        try:
            img_obj = requests.get(item.attrs["href"])
            print("Getting", img_obj)
            title = item.attrs["href"].split("/")[-1]

            try:
                img = Image.open(BytesIO(img_obj.content))
                img.save("./" + dir_name + "/" + title, img.format)
            except OSError:
                print("Could not recognize or save file.")
        except requests.exceptions.TooManyRedirects:
            print("Redirects error.")

    start_search()


start_search()
