from selenium  import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import  By
from selenium.webdriver.support import expected_conditions as ec
import time
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
wait=WebDriverWait(driver,10)
def taobao_login():
    driver = webdriver.Chrome(chrome_options=chrome_options)
    try:

        driver.get("https://www.taobao.com")
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="J_QRCodeLogin"]/div[5]/a[1]').click()
        time.sleep(1)
        #淘宝登录会检测navigator变量，登录前执行一段js修改变量
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false,});")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys("18549813253")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys("jjx6ll1win1first")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
    finally:
        driver.quit()


