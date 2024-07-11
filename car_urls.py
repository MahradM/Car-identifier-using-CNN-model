import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import mysql.connector 

#Using mysql to store all car urls
print("connecting to database...")
cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='car_image')
print("conected!")

cursor = cnx.cursor()

query = 'INSERT INTO van_cars(name,url) VALUES(%s,%s)'

#Conecting to the webpage
page = webdriver.Firefox()
page.get('https://bama.ir/car?body=van')
time.sleep(10)

num = 500 #Collect 500 sample of all urls
while num != 0:
    page.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN) #Storing the ads, Should be modify base on webpage html code
    time.sleep(0.1)
    num -= 1

car_data = []

elements = page.find_elements(By.TAG_NAME, 'img')

for element in elements:
    url = element.get_attribute("src")
    name = element.get_attribute("alt")
    if url and url.startswith("http"):
        car_data.append({
            'name': name,
            'url' : url
        })

for car in car_data:
    cursor.execute(query ,(car['name'], car['url']))
    cnx.commit()

page.quit()
