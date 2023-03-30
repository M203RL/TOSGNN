from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webbrowser
import pyperclip
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("disable-infobars") 
# path of the chrome's profile parent directory - change this path as per your system
options.add_argument(r"user-data-dir=F:\\TOS\\News\\User Data")
# name of the directory - change this directory name as per your system
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument('--no-sandbox')
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--start-maximized")
# options.add_argument("--headless")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
# driver.set_window_size(2560, 1440)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('useAutomationExtension', False)


def initial(test):
    if test:
        ##場外
        driver.get("")
    else:
        ##專版
        driver.get("https://forum.gamer.com.tw/post1.php?bsn=23805&type=1")

        select = Select(driver.find_element("name", 'nsubbsn'))
        select.select_by_value('3')

        select = Select(driver.find_element("name", 'subject'))
        select.select_by_value('2')
    time.sleep(0.1)
    if test:
        driver.find_element("id", 'editor').click()
    else:
        driver.find_element("id", 'postTips').click()


    try:
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'editor-button fe_source') and not(contains(@class, 'editor-button fe_source is-active'))]"))).click()
    except:
        pass
    text = driver.find_element("id", 'source')
    text.clear()

##1.15s
def post(test, title, article):
    # ts = time.time()
    if not test:
        ##標題
        tt = driver.find_element("name", 'title')
        pyperclip.copy(title)
        tt.send_keys(Keys.CONTROL, 'v')

    
    
    ##內文
    text = driver.find_element("id", 'source')
    pyperclip.copy(article)
    text.send_keys(Keys.CONTROL, 'v')
    
    # ##預覽
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="javascript:Forum.Post.preview();"]'))).click()

    # # ##關閉預覽
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="dialogify__close"]'))).click()
    
    ##發文
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="javascript:Forum.Post.post();"]'))).click()
    target = driver.find_element(By.CSS_SELECTOR, 'a[href="javascript:Forum.Post.post();"]')
    target.click()
    

    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="btn btn-insert btn-primary"]'))).click()
    # driver.get_screenshot_as_file("screenshot.png")
    target = driver.find_element(By.CSS_SELECTOR, 'button[class="btn btn-insert btn-primary"]')
    target.click()
    # tf = time.time()
    # dt = round(tf - ts, 2)
    # print('Total Time: ' + str(dt) + 's')
    get_url = driver.current_url
    if test:
        while get_url == "":
            get_url = driver.current_url
            time.sleep(0.01)
    if not test:
        while get_url == "https://forum.gamer.com.tw/post1.php?bsn=23805&type=1":
            get_url = driver.current_url
            time.sleep(0.01)
    
    webbrowser.open(get_url,1)
    # driver.close()
    # driver.quit()

if __name__ == '__main__':
    ts = time.time()
    initial(True)
    post(True, 'title', 'adsad')
    tf = time.time()
    dt = round(tf - ts, 2)
    print('Total Time: ' + str(dt) + 's')
