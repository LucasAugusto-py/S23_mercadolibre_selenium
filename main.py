import sqlalchemy
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

url = "https://listado.mercadolibre.com.ar/s23#D[A:s23,L:undefined]"
driver = webdriver.Chrome()
driver.get(url)

s23 = {
    'title':[],
    'price':[],
    'memory':[],
    'color':[]
}
while True:
    links_s23 = driver.find_elements(By.XPATH, '//a[@class="ui-search-item__group__element shops__items-group-details ui-search-link"]')
    links_s23_string = []
    for i in links_s23:
        links_s23_string.append(i.get_attribute("href"))

    for i in links_s23_string:
        driver.get(i)
        try:
            title = driver.find_element(By.XPATH, "//h1[@class='ui-pdp-title']").text
            s23['title'].append(title)
        except:
            print("Error: title")
            s23['title'].append(None)
        try:
            price = driver.find_element(By.XPATH, "//span[@class='andes-money-amount__fraction']").text
            s23['price'].append(price)
        except:
            print("Error: price")
            s23['price'].append(None)
        try:
            memory = driver.find_element(By.XPATH, "//span[@class='ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--SEMIBOLD' and (contains(text(), 'GB') or contains(text(),'TB'))]").text
            s23['memory'].append(memory)
        except:
            print("Error: memory")
            s23['memory'].append(None)
        try:
            color = driver.find_element(By.XPATH, "//span[contains(@id,'picker-label-COLOR')]").text
            s23['color'].append(color)
        except:
            print("Error: color")
            s23['color'].append(None)
        driver.back()
        sleep(2)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    try:
        button = driver.find_element(By.XPATH, "//span[@class='andes-pagination__arrow-title' and contains(text(), 'Siguiente')]")
        button.click()
    except:
        break

memory = driver.find_element(By.XPATH, "//span[@class='ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--SEMIBOLD' and (contains(text(), 'GB') or contains(text(),'TB'))]").text

s23 = pd.DataFrame(s23)

with open("Driver\password.txt", "r") as f:
    content = f.read()

url = f'mysql+pymysql://root:{content}@localhost:3306/demo'

engine = sqlalchemy.create_engine(url)

s23.to_sql('mytable', con=engine, if_exists='replace', index=False)