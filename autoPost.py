# selenium 3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

def initial(test):
    if test:
        ##場外
        driver.get("https://forum.gamer.com.tw/post1.php?bsn=60076&sn=87519574&type=3&all=1")
    else:
        ##專版
        driver.get("https://forum.gamer.com.tw/post1.php?bsn=23805&type=1")

        select = Select(driver.find_element("name", 'nsubbsn'))
        select.select_by_value('3')

        select = Select(driver.find_element("name", 'subject'))
        select.select_by_value('2')

    if test:
        driver.find_element("id", 'editor').click()
    else:
        driver.find_element("id", 'postTips').click()

    try:
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'editor-button fe_source') and not(contains(@class, 'editor-button fe_source is-active'))]"))).click()
    except:
        pass

def post(test, title, article):

    if not test:
        ##標題
        tt = driver.find_element("name", 'title')
        pyperclip.copy(title)
        tt.send_keys(Keys.CONTROL, 'v')

    
    ##內文
    text = driver.find_element("id", 'source')
    text.clear()
    pyperclip.copy(article)
    text.send_keys(Keys.CONTROL, 'v')

    ##預覽
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'javascript:Forum.Post.preview();')]"))).click()

    ##關閉預覽
    time.sleep(0.1)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'dialogify__close')]"))).click()

    ##發文
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'javascript:Forum.Post.post();')]"))).click()

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn btn-insert btn-primary')]"))).click()

if __name__ == '__main__':
    initial(True)
    post(True, 'title', 'adsad')