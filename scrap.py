import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from slugify import slugify


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

SHOPEE_HOME = 'https://shopee.co.id'



driver.get(SHOPEE_HOME)

try:
    pop_up_btn = driver.find_element_by_css_selector("div.shopee-popup__close-btn")
    pop_up_btn.click()
except: 
    print('no pop up')

driver.implicitly_wait(10)
driver.save_screenshot("tes.png")
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
categories_link = soup.find_all("a", class_="home-category-list__category-grid")
categories_label = soup.find_all('div', class_="vvKCN3")


categories = {}

for index in range(len(categories_link)):
    label = categories_label[index].text
    key = slugify(label)
    link = f"{SHOPEE_HOME}{categories_link[index]['href']}"

    print(f"go to {label} page")
    driver.get(link)
    driver.implicitly_wait(10)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    sub_categories_link = soup.find_all("a", class_="shopee-category-list__sub-category")
    sub_categories = [a.text for a in sub_categories_link]


    categories[key] = { "link": link, "label": label, "sub_categories": sub_categories }


with open('categories.json', 'w') as outfile:
    json.dump(categories, outfile, indent=4)
# shopee-category-list__sub-category


driver.quit()



