'''
Get Customer Numbers
'''

from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.webdriver.remote.webdriver import WebElement
import random
from selenium.webdriver.common.action_chains import ActionChains

class Scrapper(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.data = []
        self.pin :WebElement = None
        self.road_name: WebElement = None
        self.building_name: WebElement = None

    def __del__(self):
        self.driver.close()

    def run(self):
        self.driver.get("")
        self.driver.implicitly_wait(10)
        self._fetch_again()

        try:
            self.pin_len = len(self.pin.options)
            #iterate over the pin
            for pin_index in range(1, self.pin_len):
                self.pin.select_by_index(pin_index)
                print(f'Pin selected {pin_index}')
                time.sleep(random.randint(1,5)) # IMP
                self._fetch_again()
                self.road_name_len = len(self.road_name.options)
                for road_index in range(2, self.road_name_len):
                    self.road_name.select_by_index(road_index)
                    print(f'Road Name selected {road_index}')
                    time.sleep(random.randint(1,5))# IMP
                    self._fetch_again()
                    self.building_name_len = len(self.building_name.options)
                    for building_index in range(2, self.building_name_len):
                        self.building_name.select_by_index(building_index)
                        print(f'Building Name selected {building_index}')
                        time.sleep(random.randint(1,5))# IMP
                        self._fetch_again()
                        self._check_no_records()
                        self._get_table_details()

                    filename=f'data_{pin_index}_{road_index}.csv'
                    self._export_file(filename)
        except Exception as e:
            print(f'Exception Occured : {e}')
            self._fetch_again()

    def _check_no_records(self):
        try:
            error_element = WebDriverWait(self.driver, 5).until(method=EC.presence_of_element_located((By.ID, "btnerrok")))
            if error_element:
                action = ActionChains(self.driver)
                action.click(on_element = error_element)
                action.perform()
                time.sleep(random.randint(1,9))
                self._fetch_again()
        except:
            pass
    def _fetch_again(self):
        self.pin = Select(WebDriverWait(self.driver, 10).until(method=EC.presence_of_element_located((By.ID, "ddlPin"))))
        self.road_name = Select(WebDriverWait(self.driver, 10).until(method=EC.presence_of_element_located((By.ID, "ddlRoadName"))))
        self.building_name = Select(WebDriverWait(self.driver, 10).until(method=EC.presence_of_element_located((By.ID, "ddlBuildingName"))))

    def _get_table_details(self):
        rows = self.driver.find_elements(by=By.TAG_NAME, value='tr')
        for i in range(1, len(rows)):
            data = rows[i].text.split(" ")
            pin = self.pin.first_selected_option.text
            road_name = self.road_name.first_selected_option.text
            building_name = self.building_name.first_selected_option.text
            acc_no = data[0]
            cust_name = " ".join(data[1:])
            #acc_no =row.find_element(by=By.XPATH, value='//td[1]').text
            #acc_no = WebDriverWait(row, 10).until(method=EC.presence_of_element_located((By.XPATH, "//td[1]")))
            #cust_name =row.find_element(by=By.XPATH, value='//td[2]').text
            #cust_name = WebDriverWait(row, 10).until(method=EC.presence_of_element_located((By.XPATH, "//td[2]")))
            print(f'{pin} {road_name} {building_name} {acc_no} {cust_name}')
            line = {
                "pin": pin,
                'road_name': road_name,
                'building_name': building_name,
                "account_no": acc_no,
                "customer_name": cust_name,
            }
            self.data.append(line)

    def _export_file(self, filename):
        df = pd.DataFrame(self.data)
        df.to_csv(filename)
        print(f'Exporting the file... {filename}')
        self.data = []

def get_road_count():
    df = pd.read_csv('data_pin_count.csv')
    read_count = df["road_count"].to_list()

def main():
   b = Scrapper()
   b.run()

if __name__ == "__main__":
    main()