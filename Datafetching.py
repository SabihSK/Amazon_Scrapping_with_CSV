from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np

url = 'https://www.amazon.in/s?k=playstation+5&crid=1Q9LA091O7CGT&sprefix=play%2Caps%2C540&ref=nb_sb_ss_ts-doa-p_1_4'

Headers = ({'user agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36' ,'Accept language' : 'en-us , en:q = 0.5'})

amazonwebpage = requests.get(url, headers = Headers)
print(amazonwebpage.status_code)

soup = BeautifulSoup(amazonwebpage.content,  'html.parser')

def get_title(soup):
    try :
        product_title = soup.find('span' , attrs ={'id': "productTitle"})

        title_value = product_title.text

        title_string = title_value.strip()
    
    except AttributeError:
        title_string = ''

    return title_string

def get_price(soup):
    try :
        product_price = soup.find('span' , attrs ={ 'class': 'a-price-whole'})

        Product_pricee = product_price.text

        product_actual_price = Product_pricee.strip()

    except AttributeError:
        try :
            product_price = soup.find('span' , attrs = { 'id ': 'priceblock_dealprice'}).string.strip()
        except :
            product_actual_price = ''
    
    return product_actual_price

def get_imgs(soup, product_title):
    try:
        Product_img = soup.find('img', {'alt': product_title})
        if Product_img:
            Prod_img = Product_img.get('src')
            return Prod_img
    except AttributeError:
        print('This image could not be found')


def get_Description(soup):
    try:
        Product_Des = soup.find('ul', class_ = 'a-unordered-list a-vertical a-spacing-mini' )
        if Product_Des:
            Product_Des = Product_Des.text.strip()
        else:
            Product_Des = ''
    except AttributeError:
        Product_Des = ''

    return Product_Des
    
        


# print(soup.prett:ify)
links_lists = []

links = soup.find_all('a', attrs = {'class': "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

for links in links:
    links_lists.append(links.get('href'))


dct = {'Title' : [] , 'Price' : [], 'Links': [], 'Product_Img': [], 'Product_Description': []}
# print(links)
for link in links_lists:

    product_links = 'https://amazon.in'+ link
    new_amzwebpage = requests.get(product_links, headers = Headers )

    new_soup = BeautifulSoup(new_amzwebpage.content,'html.parser' )
    Product_title = get_title(new_soup)


    dct['Title'].append(get_title(new_soup))
    dct['Price'].append(get_price(new_soup))
    dct['Links'].append(product_links)
    dct['Product_Img'].append(get_imgs(new_soup,Product_title))
    dct['Product_Description'].append(get_Description(new_soup))

    amzdataframe = pd.DataFrame.from_dict(dct)
    amzdataframe['Title'].replace('', np.nan ,inplace = True)
    amzdataframe = amzdataframe.dropna(subset= ['Title'])
    amzdataframe.to_csv('AMZ DATA Scraping.csv', header = True , index = False )



# print(new_soup.prettify)
# product_title = new_soup.find('span' , attrs ={'id': "productTitle"})
# print(product_title.text.strip())
# product_price = new_soup.find('span' , attrs ={ 'class': 'a-price-whole'})
# print( product_price.text.strip())
# print(product_links)
print(amzdataframe)
print ('THIS PROGRAM IS RUNNING')

