#!/usr/bin/python
from selenium import webdriver

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
driver.get("https://lms.iiitb.ac.in/moodle/login/index.php")
username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")

username.send_keys("mt2016009")
password.send_keys("10987@X86s")

driver.find_element_by_id("loginbtn").submit()
#driver.close()
