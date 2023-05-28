from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import json

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

data = {}

for page in range(1, 10):
    if page == 1:
        url = "https://www.russiadiscovery.ru/tours"
        driver.get(url)
        blocks = driver.find_element(By.CLASS_NAME, 'd-catalog__cards')
        posts = blocks.find_elements(By.CLASS_NAME, 'd-catalog__card')
        for post in posts:
            a_tag = post.find_element(By.CLASS_NAME, 'd-catalog__card-body').find_element(By.CLASS_NAME,
                                                                     'd-catalog__card-info').find_element(By.TAG_NAME, 'a')
            title_link = a_tag.get_attribute('href')
            title = a_tag.find_element(By.TAG_NAME, 'div').get_attribute('innerText')
            price = post.find_element(By.CLASS_NAME, 'd-catalog__card-footer').find_element(By.CLASS_NAME,
                                                                                            'd-catalog__card-price-row').find_element(By.CLASS_NAME, 'd-catalog__card-currentprice').get_attribute('innerText')
            data[title] = {
                'url': title_link,
                'price': price,
            }
    else:
        url = f"https://www.russiadiscovery.ru/tours/page/{page}/"
        driver.get(url)
        blocks = driver.find_element(By.CLASS_NAME, 'd-catalog__cards')
        posts = blocks.find_elements(By.CLASS_NAME, 'd-catalog__card')
        for post in posts:
            a_tag = post.find_element(By.CLASS_NAME, 'd-catalog__card-body').find_element(By.CLASS_NAME,
                                                                     'd-catalog__card-info').find_element(By.TAG_NAME, 'a')
            title_link = a_tag.get_attribute('href')
            title = a_tag.find_element(By.TAG_NAME, 'div').get_attribute('innerText')
            price = post.find_element(By.CLASS_NAME, 'd-catalog__card-footer').find_element(By.CLASS_NAME,
                                                                                            'd-catalog__card-price-row').find_element(By.CLASS_NAME, 'd-catalog__card-currentprice').get_attribute('innerText')
            data[title] = {
                'url': title_link,
                'price': price,
            }


for post_url in data.values():
    driver.get(post_url['url'])
    main_div = driver.find_element(By.CLASS_NAME, 'd-tour__form-row')
    tour_group = main_div.find_element(By.CLASS_NAME, 'd-tour__form-group-val').get_attribute('innerText').strip()
    post_url['group'] = tour_group
    post_url['photos'] = []
    elements = driver.find_elements(By.CSS_SELECTOR, '[data-name="gallery"]')
    for el in elements:
        if len(post_url['photos']) < 5:
            post_url['photos'].append(el.get_attribute('src'))
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

