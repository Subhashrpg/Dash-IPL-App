from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

url = "https://m.cricbuzz.com/cricket-series/5945/indian-premier-league-2023/matches"

# double match held so second match
left_matches = [3, 4, 10, 11, 17, 18, 22, 24, 25, 31, 32, 35, 38, 39, 45, 46, 52, 53]
driver.get(url)
time.sleep(2)

for i in range(2,59):
    driver.find_element(by=By.XPATH, value=f"/html/body/div/main/div[2]/div[1]/div/div/div[{i}]/div/div/div/a/span").click()

    # left matches element 
    # driver.find_element(by=By.XPATH, value= f"/html/body/div/main/div[2]/div[1]/div/div/div[{i}]/div/div/div[2]/a/span").click()

    driver.find_element(by=By.XPATH, value='//*[@id="main-nav"]/a[4]').click()
    html = driver.page_source
    time.sleep(1)

    with open(rf"D:\Subhash\Projects\python\page_sources\page{i}.html", "w", encoding="utf-8") as f:
        f.write(html)

    driver.get(url)
    time.sleep(.5)
