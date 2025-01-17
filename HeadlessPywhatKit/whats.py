import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pathlib
from selenium import webdriver

class WhatsApp:
    def __init__(self,headless:bool=True):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        if headless:
            chrome_options.add_argument("--headless")#will open headless means allow us to work without showing website
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux i686; rv:77.0) Gecko/20100101 Firefox/77.0")
        path = str(pathlib.Path('../chrome-data').resolve())
        chrome_options.add_argument(fr"user-data-dir={path}")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.login()

    def login(self):
        driver = self.driver
        try:
            driver.get('https://web.whatsapp.com/')
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div['
                                                          '2]/div/canvas')))
            WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/div/span')))
            print('qr found')
            ok = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/canvas')
            print(ok.screenshot("qr_code.png"))
            self.driver = driver
        except Exception as e:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/div/div[3]/header/div[2]/div/span/div[4]/div')))
            self.driver = driver
            return True

    def get_pending_chats(self):
        driver = self.driver
        driver.get('https://web.whatsapp.com/')
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[1]/div/button')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[3]/div/div[1]/div/button')
        element.click()
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div')
        print(element)
        self.driver = driver
        time.sleep(2)

    def send_user_message(self, phone: str, message: str):
        driver = self.driver
        phone = phone.replace(" ", "")
        driver.get(f'https://web.whatsapp.com/send?phone={phone}&text={message}')
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div['
                           '2]/button')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div['
                                      '2]/div['
                                      '2]/button')
        element.click()
        self.driver = driver
        time.sleep(2)

    def send_document(self, phone: str, file_list: list[str] = None,filename:str = None,foldername:str = None):
        driver = self.driver
        phone = phone.replace(" ", "")
        driver.get(f'https://web.whatsapp.com/send?phone={phone}')
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div['
                                      '1]/div['
                                      '2]/div/div')
        element.click()
        print('window opened')
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div['
                           '2]/div/span/div/div/ul/li[4]/button/input')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div['
                                      '1]/div['
                                      '2]/div/span/div/div/ul/li[4]/button/input')
        print("file menu opened")
        if foldername:
            file_list = [x for x in pathlib.Path(foldername).iterdir() if not x.is_dir()]
        if filename:
            element.send_keys(str(pathlib.Path(filename)))
        else:
            for i in file_list:
                element.send_keys(str(pathlib.Path(i)))
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div['
                                      '2]/div/div[2]/div[2]/div/div')
        element.click()
        self.driver = driver
        time.sleep(10)

    def send_image(self, phone: str, filename: str):
        driver = self.driver
        phone = phone.replace(" ", "")
        driver.get(f'https://web.whatsapp.com/send?phone={phone}')
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div['
                                      '1]/div['
                                      '2]/div/div')
        element.click()
        path_of_file = pathlib.Path(filename)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div['
                           '2]/div/span/div/div/ul/li[1]/button/input')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div['
                                      '1]/div['
                                      '2]/div/span/div/div/ul/li[1]/button/input')
        element.send_keys(str(path_of_file.resolve()))
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div['
                                      '2]/div/div['
                                      '2]/div[2]/div/div')
        element.click()
        self.driver = driver
        time.sleep(7)

    def __del__(self):
        driver = self.driver
        driver.close()
        self.driver = driver
