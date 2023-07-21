from data import urls
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import csv
from selenium.webdriver.common.by import By


url = 'https://epk.kantiana.ru/interactive_detail?report_option=74a7abc8-1056-11ee-80b7-005056970631&scenario=c3710616-545c-11ed-895c-005056970631&scenarioN=%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%20%D0%BF%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0%D1%8E%D1%89%D0%B8%D1%85%202023%20(%D0%BC%D0%B0%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D1%83%D1%80%D0%B0)&level_education=28724740-4989-11eb-7d9a-005056970631&form_education=2214ebb4-4989-11eb-7d9a-005056970631&basis_admission=221173da-4989-11eb-7d9a-005056970631|false&faculty=b810f498-ba74-11ec-804c-005056970631&direction=4b3ad692-6523-11eb-7d9a-005056970631&profile=d1e6e756-5470-11ed-895c-005056970631'


def selenium_dowload_page(url):
    driver = webdriver.Chrome()

    try:
        driver.get(url=url)
        time.sleep(5)
        element = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/main/div/div[3]/div[2]/div/div[3]/div[1]/div/div')
        element.click()
        element_next = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[4]')
        element_next.click()
       
        with open("index.html", "w") as f:
            f.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def table_value(name):
    with open("index.html") as file:
        src = file.read()


    soup = BeautifulSoup(src, 'lxml')
    temp = []
    value = soup.find('tbody')
    span = value.find_all('span')

    for i in span:
        temp.append(i.text.split())

    step = 7
    output_lists = [temp[i:i+step] for i in range(0, len(temp), step)]

    merged_list = []
    for main_list in output_lists:
        temp_list = []
        for sublist in main_list:
            if len(sublist) == 2:
                temp_list.append([sublist[0] + ' ' + sublist[1]])
            else:
                temp_list.append(sublist)
        merged_list.append(temp_list)
  

    with open(f'/home/trytestme/my-app/pythonproject/data/{name}'+'_table.csv', 'w', encoding='utf-8' ) as file:
        writer = csv.writer(file)

        writer.writerow(
            (
            '#',
            'СНИЛС',
            'Диплом',
            'Оригинал',
            'ИД',
            'Общага',
            'Способ подачи'
            )
        )

    with open(f'/home/trytestme/my-app/pythonproject/data/{name}'+'_table.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in merged_list:
            writer.writerow([item for sublist in row for item in sublist])

    
    
    
for name in urls:
    selenium_dowload_page(urls[name])
    table_value(name)
    