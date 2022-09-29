import time
import os
import pandas as pd
import urllib.request
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By

amount_page = int(input('amount select page table: '))
root_dir = os.path.dirname(__file__)
assets = os.path.join(root_dir, 'assets')
path = os.path.abspath('chromedriver')
options = webdriver.ChromeOptions()
prefs = {'download.default_directory': assets}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(path, chrome_options=options)
persiann_css = os.path.join(assets, 'gsmap-nrt')
concat = []

url = 'http://www.satda.tmd.go.th/monitoring/index.php?pccs-Open%20Data'
driver.get(url)
driver.implicitly_wait(5)
time.sleep(1)
sorting_year = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/thead/tr/th[1]')
sorting_year.click()

thead = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div/div/div/div/div/table/thead').text
table = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div/div/div/div/div/table')
count = 1

while count <= amount_page:
    print(f'page... {count}')
    print(thead)
    for row in range(10):
        day = f'/html/body/div[2]/div/div[3]/div/div/div/div/div/table/tbody/tr[{row + 1}]/td[3]'
        month = f'/html/body/div[2]/div/div[3]/div/div/div/div/div/table/tbody/tr[{row + 1}]/td[2]'
        year = f'/html/body/div[2]/div/div[3]/div/div/div/div/div/table/tbody/tr[{row + 1}]/td[1]'
        a = f'/html/body/div[2]/div/div[3]/div/div/div/div/div/table/tbody/tr[{row + 1}]/td[6]/a'
        tr = f'/html/body/div[2]/div/div[3]/div/div/div/div/div/table/tbody/tr[{row + 1}]'

        elem_a = table.find_element(By.XPATH, a)
        elem_tr = table.find_element(By.XPATH, tr)
        day = table.find_element(By.XPATH, day).text
        month = table.find_element(By.XPATH, month).text
        year = table.find_element(By.XPATH, year).text
        csv_href = elem_a.get_attribute('href')
        file_name = f'persiann-css2022/persiann-css-{year}-{month}-{day}.csv'
        dir_file = os.path.join(assets, file_name)
        urllib.request.urlretrieve(csv_href,
                                   filename=dir_file)
        df = pd.read_csv(dir_file)
        df['year'] = year
        df['month'] = month
        df['day'] = day
        df.to_csv(dir_file)
        print(elem_tr.text)

    print('\n')
    next_page = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div/div/div/div/div/div[5]/ul/li[9]/a')
    next_page.click()
    count += 1

for fn in os.listdir(persiann_css):
    if not fn.startswith('.'):
        path_fn = os.path.join(persiann_css, fn)
        df = pd.read_csv(path_fn)
        concat.append(df)

print('waiting progress...')

dfs = pd.concat(concat)
dfs.to_excel('sum_persiann-nrt.xlsx', engine='xlsxwriter')
driver.close()
