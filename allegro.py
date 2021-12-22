import pyautogui as pui
from selenium import webdriver

driver = webdriver.Chrome()


def site_search(item):
    driver.get('https://allegro.pl')
    driver.maximize_window()
    pui.sleep(1)
    pui.typewrite(item)
    pui.press('enter')
    # time.sleep(2)
    # driver.find_element(By.XPATH, '//button[text()="Ok, zgadzam się"]').click()
    # driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/header/div/div/div[1]/div/form/input').send_keys(item)
    # driver.find_element(By.XPATH, '//button[text()="szukaj"]').click()


if __name__ == '__main__':
    site_search('3080ti')
