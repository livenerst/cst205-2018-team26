import requests
from bs4 import BeautifulSoup
import os

r = requests.get("http://pythonforengineers.com/pythonforengineersbook/")
data = r.text
soup = BeautifulSoup(data, "lxml")

for link in soup.findAll('img'):
    image = link.get('src')
    # image = "http:" + image

    q_mark = image.find('?')
    image = image[:q_mark]
    image_name = os.path.split(image)[1]
    # print(image, image_name)

    r2 = requests.get(image)
    with open(image_name, "wb") as f:
        f.write(r2.content)
