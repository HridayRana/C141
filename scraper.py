from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

# Webdriver
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

star_data = []

# Define Exoplanet Data Scrapping Method
def scrape():

    for i in range(0,10):
        print(f'Scrapping page {i+1} ...' )
        
        # BeautifulSoup Object     
        soup = BeautifulSoup(browser.page_source, "html.parser")

        # Loop to find element using XPATH
        for tr_tag in soup.find_all("tr", attrs={"class", "refList"}):

            td_tags = tr_tag.find_all("td")
           
            temp_list = []

            for index, td_tag in enumerate(td_tags):

                if index == 0:                   
                    temp_list.append(td_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(td_tag.contents[0])
                    except:
                        temp_list.append("")

            star_data.append(temp_list)


            Star_names = []
            Distance = []
            Mass = []
            Radius = []
            Lum = []

            for i in range(1,len(temp_list)):
                Star_names.append(temp_list[i],[1])
                Distance.append(temp_list[i],[3])
                Mass.append(temp_list[i],[5])
                Radius.append(temp_list[i],[6])
                Lum.append(temp_list[i],[7])
                

        # Find al elements on the page and click to move to the next page
        browser.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

# Calling Method    
scrape()

# Define Header
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]

# Define pandas DataFrame   
planet_df_1 = pd.DataFrame(star_data, columns=headers)

# Convert to CSV
planet_df_1.to_csv('scraped_data.csv',index=True, index_label="id")
