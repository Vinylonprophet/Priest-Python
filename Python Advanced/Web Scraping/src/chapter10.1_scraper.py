from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式运行
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（可选）
chrome_options.add_argument("--no-sandbox")  # 在某些情况下以 root 身份运行时需要
chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误

driver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://pythonscraping.com/pages/javascript/ajaxDemo.html")

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, "loadedButton"))
    )
finally:
    print(driver.find_element("id", "content").text)
    driver.quit()
