from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(user, browser):
	configFilePath = r'./loginConfig.ini'

	parser = ConfigParser()
	parser.read(configFilePath)

	usernameStr = parser.get(user, 'userName')
	passwordStr = parser.get(user, 'password')

	browser.get(('https://www.worldquantvrc.com/login?next=%2Fvideos#voctp'))

	usernameField = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.ID, 'EmailAddress')))
	usernameField.send_keys(usernameStr)

	passwordField = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.ID, 'Password')))
	passwordField.send_keys(passwordStr)

	loginButton = browser.find_element_by_class_name('login-btn')
	loginButton.click()
	