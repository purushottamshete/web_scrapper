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
from multiprocessing import Process
import time

class Scrapper(object):
    def __init__(self):
        self.driver = None
        self.data = []
        self.pin :WebElement = None
        self.road_name: WebElement = None
        self.building_name: WebElement = None

    def __del__(self):
        #self.driver.close()
        pass

    def run(self, pin_index):
        self.driver = webdriver.Chrome()
        self.driver.get("")
        self.driver.implicitly_wait(10)
        self._fetch_again()

        try:
            pin=None
            self.pin.select_by_index(pin_index)
            #print(f'Pin selected {pin_index}')
            time.sleep(random.randint(1,5)) # IMP
            self._fetch_again()
            # self.arr[pin_index] = str(pin)
            self.road_name_len = len(self.road_name.options)
            for road_index in range(2, self.road_name_len):
                
                self.road_name.select_by_index(road_index)
                #print(f'Road Name selected {road_index}')
                time.sleep(random.randint(1,5))# IMP
                self._fetch_again()
                pin = self.pin.first_selected_option.text
                road_name = self.road_name.first_selected_option.text
                self.building_name_len = len(self.building_name.options)
                
                #print(f'{pin} {self.road_name_len} ')
                line = {
                    "pin": pin,
                    'road_name': road_name ,
                    'count': self.building_name_len,
                }
                self.data.append(line)

            filename=f'data_{pin}_count_mp.csv'
            self._export_file(filename)
        except Exception as e:
            print(f'Exception Occured : {e}')
            self._fetch_again()

    def _fetch_again(self):
        self.pin = Select(WebDriverWait(self.driver, 10).until(method=EC.presence_of_element_located((By.ID, "ddlPin"))))
        self.road_name = Select(WebDriverWait(self.driver, 10).until(method=EC.presence_of_element_located((By.ID, "ddlRoadName"))))
        self.building_name = Select(WebDriverWait(self.driver, 10).until(method=EC.presence_of_element_located((By.ID, "ddlBuildingName"))))


    def _export_file(self, filename):
        df = pd.DataFrame(self.data)
        df.to_csv(filename)
        print(f'Exporting the file... {filename}')
        self.data = []

def main():
    #b = Scrapper()
    start  =time.time()
    processes = []
    for i in range(1,39):
        processes.append(Process(target=Scrapper().run, args=(i,)))

    for i in range(0, 10):
        processes[i].start()

    for i in range(0, 10):
        processes[i].join()

    for i in range(10, 20):
        processes[i].start()

    for i in range(10, 20):
        processes[i].join()

    for i in range(20, 30):
        processes[i].start()

    for i in range(20, 30):
        processes[i].join()

    for i in range(30, 38):
        processes[i].start()

    for i in range(30, 38):
        processes[i].join()
    end  =time.time()
    print(f'time taken to execute {end-start} sec')

if __name__ == "__main__":
    main()