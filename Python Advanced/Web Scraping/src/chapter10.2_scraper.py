from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def waitForLoad(driver):
    elem = driver.find_element("tag name", "html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(0.5)
        try:
            elem == driver.find_element("tag name", "html")
        except StaleElementReferenceException:
            return


chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式运行
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（可选）
chrome_options.add_argument("--no-sandbox")  # 在某些情况下以 root 身份运行时需要
chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误

driver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://pythonscraping.com/pages/javascript/ajaxDemo1.html")
waitForLoad(driver)
print(driver.page_source)
