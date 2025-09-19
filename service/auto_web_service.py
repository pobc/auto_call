from selenium import webdriver

driver_path = r'C:\Users\jiang\PycharmProjects\xianyu_spider\service\geckodriver.exe'

driver = webdriver.firefox(driver_path)
driver.get('www.baidu.com')
print(driver.title)

driver.quit()