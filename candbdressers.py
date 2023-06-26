from requests_html import HTMLSession
import time
import random
import pandas as pd

url="https://www.crateandbarrel.com/furniture/dressers-chests/1"
session=HTMLSession()
r=session.get(url)
r.html.render(sleep=2)
product_cards = r.html.find('.card.product-card')
# Extract the links from the product cards
links = [card.find('a', first=True).absolute_links.pop() for card in product_cards]
#need manufacturer, price, dimensions, style, material, and a picture.

for items in links:
    r=session.get(items)
    r.html.render(timeout=10)

    price=r.html.find('span.regPrice', first=True).text

    dim_name=r.html.find('div.details-dimensions',first=True).text
    split_index= dim_name.rindex(" ")
    name= dim_name[:split_index]
    dimensions= dim_name[split_index + 1:]

    sku=r.html.find('span.sku-number', first=True).text

    #material is in a different spot in each product but within the first 2 bullet points of each description
    text=r.html.find('ul.details-list',first=True)
    material=[]
    material_1=text.find('li')[0].text
    material_2=text.find('li')[1].text
    material.append([material_1,material_2])

    longform_desc=r.html.find('div.details-description',first=True).text

    bullet_desc=r.html.find('ul.details-list',first=True).text

    button=r.html.find('div.main-carousel-item',first=True)
    main_image=button.find('img')[1].attrs["src"]
    all_product_thumbnail=r.html.find('div.product-carousel-thumbnail',first=True)
    products=all_product_thumbnail.find("div")
    links=[]
    for product in products:
        img_element = product.find("img", first=True)
        if img_element:
            image_thumbnail = img_element.attrs["src"]
            image_thumbnail= image_thumbnail.split("Crate/")[1]
            id= image_thumbnail.split("$")[0]
            image_link=f"https://cb.scene7.com/is/image/Crate/{id}/"
            links.append(image_link)
            all_images = list(set(links))
    time.sleep(random.randrange(30, 40))

df_candb = {'Name': [name], "SKU":[sku], 'Dimensions': [dimensions], "Price":[price], "Material": [material], "Main_Picture": [main_image], "All_pictures": [all_images], "Key_Features": [bullet_desc], "Long_Description":[longform_desc]}
df = pd.DataFrame(df_candb)
print(df.head())
