#!/usr/bin/python
from selenium import webdriver
import sys

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
driver.get("https://lms.iiitb.ac.in/moodle/login/index.php")
username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")

username.send_keys("mt2016009")
password.send_keys("10987@X86s")

driver.find_element_by_id("loginbtn").submit()
link = driver.find_element_by_link_text('My courses')
link.click()

sub = sys.argv[1]
if (sub == "mp"):
	link = driver.find_element_by_link_text('2017 - DS/NC/ESD 863 Machine Perception')
	link.click()
	try:
		if(sys.argv[2]=="video"):
			link = driver.find_element_by_link_text('Impratus Lecture Capture')
			try:
				link.click()
			except:
				pass
	except:
		print "no option"
elif(sub == "fbda"):
	link = driver.find_element_by_link_text('2017 - CS/DS 812 Foundations for Big Data Algorithms')
	link.click()
	try:
		if(sys.argv[2]=="video"):
			link = driver.find_element_by_link_text('Impratus Lecture Capture')
			try:
				link.click()
			except:
				pass
	except:
		print "no option"
elif(sub == "ds"):
	link = driver.find_element_by_link_text('2016 Term I CS 501 Data Structures & Algorithms')
	link.click()
	try:
		if(sys.argv[2]=="video"):
			link = driver.find_element_by_link_text('Impratus Lecture Capture')
			try:
				link.click()
			except:
				pass
	except:
		print "no option"
else:
	link = driver.find_element_by_link_text('2017 - DS/NC 821 Automatic Speech Recognition')
	link.click()
	try:
		if(sys.argv[2]=="video"):
			link = driver.find_element_by_link_text('Impratus Lecture Capture')
			try:
				link.click()	
			except:
				pass
	except:
		print "no option"


#driver.close()
