import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from slugify import slugify

options = webdriver.ChromeOptions()
options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)


TOKPED_KATEGORI = 'https://m.tokopedia.com/p'

driver.get(TOKPED_KATEGORI)
driver.implicitly_wait(10)

driver.save_screenshot('ss.png')


# scrollCat.scrollTop = scrollCat.scrollHeight
categoryContainer = driver.find_element_by_css_selector('ul.css-vfbzo2.efpvpt90')

cat_lists = set(driver.find_elements_by_css_selector("li.efpvpt91"))

for x in range(3, 1, -1):
    driver.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{x}", categoryContainer)
    cat_lists_after_scroll = set(driver.find_elements_by_css_selector("li.efpvpt91"))
    cat_lists |= cat_lists_after_scroll



categories = {}

for list in iter(cat_lists):
    try:
        label = list.find_element_by_tag_name('span').text
        key = slugify(label)

        list.click()
        driver.implicitly_wait(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        sub_categories = soup.find_all('h3', class_="css-1debb2x")
        categories[key] = {
            "label": label, 
            "sub_categories": [sub_cat.text for sub_cat in sub_categories]
        }
    except ValueError: 
        print(ValueError)

with open('categories-tokped.json', 'w') as outfile:
    json.dump(categories, outfile, indent=4)

driver.quit()
