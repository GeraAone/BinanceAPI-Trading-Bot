from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

from bs4 import BeautifulSoup

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
timeout = 5

driver.get('https://www.binance.com/ru/trade/BTC_USDT?theme=dark&type=spot')
sleep(2)
element_present = EC.presence_of_element_located((By.ID, 'onetrust-reject-all-handler'))
WebDriverWait(driver, timeout).until(element_present)
cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
cookie_button.click()
sleep(2)

element_present = EC.presence_of_element_located((By.CLASS_NAME, 'icon-box'))
WebDriverWait(driver, timeout).until(element_present)
divs_list = driver.find_elements(By.CLASS_NAME, 'icon-box')
ans = divs_list[0]
for item in divs_list:
    if item.get_attribute('tooltip') == 'Настройки':
        ans = item
# sleep(3)
driver.execute_script("window.scrollTo(0, 200)")
ans.click()

element_present = EC.presence_of_element_located((By.CLASS_NAME, 'css-12xrcx8'))
WebDriverWait(driver, timeout).until(element_present)
indicators_list = driver.find_elements(By.CLASS_NAME, 'css-12xrcx8')#finding MA, EMA
# print('indicators_list len = ', len(indicators_list))
indicators_list[0].click()
sleep(1)

element_present = EC.presence_of_element_located((By.CLASS_NAME, 'css-fm7hk'))
WebDriverWait(driver, timeout).until(element_present)
divs_list = driver.find_elements(By.CLASS_NAME, 'css-fm7hk')
# print('divs_list len = ', len(divs_list))
values = [13, 21, 55]
for i in range(3):
    # divs_list[i].clear()
    divs_list[i].send_keys(Keys.CONTROL, "a")
    divs_list[i].send_keys(Keys.DELETE)
    divs_list[i].send_keys(str(values[i]))

xpath = ['/html/body/div[5]/div[1]/div/div/div[2]/div[1]/div/div[3]/div/label/div']
for i in range(len(xpath)):
    element_present = EC.presence_of_element_located((By.XPATH, xpath[i]))
    WebDriverWait(driver, timeout).until(element_present)
    checkbox = driver.find_elements(By.XPATH, xpath[i])
    if len(checkbox) == 0:
        print("couldn't find elem")
    elif not checkbox[0].is_selected():
        checkbox[0].click()


indicators_list[1].click()
sleep(1)
xpath = ['/html/body/div[5]/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[3]/label/div[1]']
xpath.append('/html/body/div[5]/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[5]/label/div[1]')
for i in range(len(xpath)):
    element_present = EC.presence_of_element_located((By.XPATH, xpath[i]))
    WebDriverWait(driver, timeout).until(element_present)
    checkbox = driver.find_element(By.XPATH, xpath[i])
    input_ = driver.find_element(By.CLASS_NAME, 'css-p19g2b')
    if input_.get_attribute('checked'):
        checkbox.click()

element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/input'))
WebDriverWait(driver, timeout).until(element_present)
input_ = driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/input')
input_.send_keys(Keys.CONTROL, "a")
input_.send_keys(Keys.DELETE)
input_.send_keys(str(8))

element_present = EC.presence_of_element_located((By.CLASS_NAME, 'css-1dmh4cv'))
WebDriverWait(driver, timeout).until(element_present)
save_button = driver.find_element(By.CLASS_NAME, 'css-1dmh4cv')
save_button.click()

sleep(2)
#time interval change
time_xpath = '/html/body/div[1]/div[3]/div/div[3]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div'
element_present = EC.presence_of_element_located((By.XPATH, time_xpath))
WebDriverWait(driver, timeout).until(element_present)
time_interval_choose = driver.find_element(By.XPATH, time_xpath)
hover = ActionChains(driver).move_to_element(time_interval_choose)
hover.perform()

sleep(2)
# element_present = EC.presence_of_element_located((By.CLASS_NAME, 'interval-option css-1mq8x9p'))
# WebDriverWait(driver, timeout).until(element_present)
# divs_list = driver.find_element(By.CLASS_NAME, 'interval-option css-1mq8x9p')
time_choosen = driver.find_element(By.XPATH, "//div[@class='css-10s0bbk']//label[@class='interval-option css-1mq8x9p']")
ActionChains(driver).move_to_element(time_choosen).click(time_choosen).perform()
sleep(3)
#нужный график выбран, осталось парсить значения индикаторов

while True:
    try:
        green, yellow, red, blue = 0, 0, 0, 0
        indicators = [0, 0, 0, 0]
        keys = ['MA[0]Series', 'MA[1]Series', 'MA[2]Series', 'EMA[0]Series']
        for i in range(len(keys)):
            need_box = [x for x in driver.find_elements(By.CLASS_NAME, 'default-label-box') if x.get_attribute('key') == keys[i]]
            if need_box != []:
                indicators[i] = need_box[0].text
        print('green = ', indicators[0], 'yellow = ', indicators[1], 'red = ', indicators[2], 'blue = ', indicators[3], sep=', ')
        if indicators[2] <= min(indicators):
            print('Покупка!!!')
        elif indicators[2] >= max(indicators):
            print('Продажа!!!')
        sleep(5)
    except KeyboardInterrupt:
        driver.quit()
        break