'''
Get Customer Numbers
'''


from time import sleep
#from selenium import webdriver
import asyncio
from arsenic import get_session, browsers, services, Session, start_session , stop_session
from arsenic.session import Element
# from selenium.webdriver.chrome.options import Options 
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
import time

class Scrapper(object):
    def __init__(self):
        #self.driver = None
        self.data = []
        self.pin :Element= None
        self.road_name: Element= None
        self.building_name: Element= None

        self.service = services.Chromedriver(binary='/usr/local/bin/chromedriver')
        self.browser = browsers.Chrome()
        # self.browser.capabilities = {
        #     "goog:chromeOptions": {"args": ["--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]}
        # }
        
    def __del__(self):
        next(start_session(self.service, self.browser))

    async def run(self, pin_index: int):
        self.session = await start_session(self.service, self.browser)
        await self.session.get("")
        await self._fetch_again()

        try:
            pin=None
            self.pin.select_by_value(f'400001')
            #print(f'Pin selected {pin_index}')
            time.sleep(random.randint(1,5)) # IMP
            self._fetch_again()
            # self.arr[pin_index] = str(pin)
            self.road_name_len = len(self.road_name.options)
            for road_index in range(2, self.road_name_len):
                
                self.road_name.get_element(f'option[index={road_index}]')
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

            filename=f'data_{pin}_count.csv'
            self._export_file(filename)
        except Exception as e:
            print(f'Exception Occured : {e}')
            self._fetch_again()

    async def _fetch_again(self):
        self.pin = await self.session.wait_for_element(10, "#ddlPin")
        self.road_name = await self.session.wait_for_element(10, "#ddlRoadName")
        self.building_name = await self.session.wait_for_element(10, "#ddlBuildingName")
      

    def _export_file(self, filename):
        df = pd.DataFrame(self.data)
        df.to_csv(filename)
        print(f'Exporting the file... {filename}')
        self.data = []

async def main():
    limit = asyncio.Semaphore(10)
    start  =time.time()
    # for i in range(1,39):
    #     async with limit:
    await Scrapper().run(1)
    end =time.time()
    print(f'time taken to execute {end-start} sec')

if __name__ == "__main__":
    asyncio.run(main())