from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
from os import getcwd, mkdir, path, system, remove
options = ChromeOptions()
options.add_argument(f"user-data-dir={getcwd()}\chromeProfile")
options.add_argument("--log-level=3")
options.headless = False
browser = Chrome(executable_path=r"driver/chromedriver.exe",options=options)
browser.set_window_position(0,0)
browser.set_window_size(1024,768)
browser.get("https://www.instagram.com/bilgehankalay/")
browser.save_screenshot("deneme")
a = input("test")
#/html/body/div[6]/div/div/div[2]/ul/div/li[2]/div/div[2]/div[2]/div
#/html/body/div[6]/div/div/div[2]/ul/div/li[2]/div/div[2]/div[2]/div
#/html/body/div[6]/div/div/div[2]/ul/div/li[2]/div/div[2]/div[2]/div
#/html/body/div[6]/div/div/div[2]/ul/div/li[2]/div/div[2]/div[2]/div
#/html/body/div[6]/div/div/div[2]/ul/div/li[17]/div/div[1]/div[2]/div[2]
#/html/body/div[6]/div/div/div[2]/ul/div/li[24]/div/div[1]/div[2]/div[2]
#/html/body/div[6]/div/div/div[2]/ul/div/li[2]/div/div[1]/div[2]/div[2]
#/html/body/div[6]/div/div/div[2]/ul/div/li[200]/div/div[1]/div[2]/div[2]